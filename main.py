""" web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"

THis is the main script to generate a web logbook from a diving logbook database.
"""
import shutil
import yaml
import argparse
from pathlib import Path
from dl6_db import get_dl6_db, DL6DB, dl6_tables, index_dl6_db, mdb_clean, tripMapBounds, xcheck_Logbook
from gallery_db import add_gallery2logbook
from gen_details import html_all_details
from pylist2js import pylist_to_js_array
import os

def run(infile: str, outdirectory: str, gallery_db: str, gallery_use: bool = False, gallery_type: str = "none") -> None:
    """Run the web logbook generation process.
    args:
        infile: Path to the input logbook database file.
        outdirectory: Directory where output files will be saved.
        gallery_db: Path to the gallery database file.
        gallery_use: Boolean indicating whether to use the gallery.
        gallery_type: Type of gallery to use (e.g., "database").
    """
    print(f"Running with {infile=}, {outdirectory=}")
    
    # open database and fetch data
    database_file: str = infile

    db_type = "sql"
    dl6db = DL6DB(database_file, db_type)
    dl6db.tables_keys = dl6_tables
    db_OK = get_dl6_db(dl6db)
    if db_OK == True:
        index_dl6_db(dl6db)
        xcheck_Logbook(dl6db)
        tripMapBounds(dl6db)
    else:
        print("DB read failed, quit")    
        quit()

    # create output directory if it doesn't exist
    Path(f'{outdirectory}{os.sep}json').mkdir(parents=True, exist_ok=True)
    Path(f'{outdirectory}{os.sep}html').mkdir(parents=True, exist_ok=True)

    ### gallery
    if gallery_use == True:
        if gallery_type != "database":
            print("Currently only 'database' gallery type is supported. Disabling gallery use.")
            gallery_use = False 
        else:
            print(f"Using gallery database: {gallery_db}")
            from gallery_db import Gallery, get_gallery
            # gallery_db from yaml config
            gallery = Gallery(gallery_db)
            get_gallery(gallery)
            add_gallery2logbook(dl6db, gallery)
            
            #dl6db.gallery_idlist = [item["ID"] for item in dl6db.gallery.g]
            gallery_outfile = f"{outdirectory}{os.sep}json{os.sep}gallery.json"
            pylist_to_js_array(gallery.g, gallery_outfile, keys=["ID", "Url", "Date", "Sitename"])
            print(f'Wrote {gallery_outfile}')

    tables = [
        {"name": "Logbook",   "cols": [ "Number","Divedate","Entrytime","Place","Divetime","Depth", "Buddy"]},
        {"name": "Trip",      "cols": [ "ID","TripName","StartDate","EndDate"]},
        {"name": "Place",     "cols": ["ID", "Place", "Lat", "Lon"] },
        {"name": "Buddy",     "cols": ["ID", "FirstName", "LastName"] },
        {"name": "Equipment", "cols": ["ID", "Object"] },
        {"name": "Brevets",   "cols": ["ID", "Brevet", "Org"] },
    ]

    for table in tables:   
        outfilename = f"{outdirectory}{os.sep}json{os.sep}{table['name']}_summary.json"
        pylist_to_js_array(dl6db.tD[table["name"]], outfilename, 
                    keys= table["cols"] if len(table["cols"]) > 0 else None)
        print(f'Wrote {outfilename}')

    tables = ["Place", "Trip", "Buddy", "Equipment", "Brevets", "Logbook"]
    html_all_details(dl6db, tables, outdirectory, gallery_use)  
    
    # write config.js
    gallery_use_str = "true" if gallery_use else "false"
    config_js_content = f"""const GALLERY_USE = {gallery_use_str};\n
    """
    with open(f"{outdirectory}{os.sep}config.js", "w", encoding="utf-8") as f:
        f.write(config_js_content)
    
    
    # copy static files
    static_files = [
        "logbook.html",
        "about.html",
        "favicon.ico",
        ##"config.js", # dynamically generated
        "leaflet.js",
        "sitemap.js",                
        "divinglog.js",
        "gen_html_table.js",
        "leaflet.css",
        "viewdive.css",
        "MapPinPlace.png",
    ]
    for filename in static_files:
        source_path = Path(f".{os.sep}{filename}")
        destination_path = Path(f"{outdirectory}{os.sep}{filename}")
        if source_path.exists():
            shutil.copy2(source_path, destination_path)
            print(f'Copied {source_path} to {destination_path}')
        else:
            print(f'Static file not found: {source_path}')  
    print("All done.")



def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(description="Web logbook generator")
    parser.add_argument(
        "-c", "--config",
        default="config.yaml",
        help="Path to YAML config file (default: config.yaml)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="web-logbook 1.0.0"
    )

    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        parser.error(f"Config file not found: {config_path}")
        quit()
    else:
        print(f"Using config file: {config_path}")    

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    infile = config.get("logbook_file", "logbook.sql")
    outdirectory = config.get("out_directory", "output")
    gallery_use = config.get("gallery_use", False)
    gallery_type = config.get("gallery_type", "none")
    gallery_db = config.get("gallery_db", "gallery.db")
    
    run(infile, outdirectory, gallery_db, gallery_use, gallery_type)
    


if __name__ == "__main__":
    """ Entry point of the script.
    """
    main()