""" web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"

This Module Handles the gallery.db database
"""
import sqlite3 
from dl6_db import DL6DB, fetch_allof_table, create_connection
from gen_details import fix_encoding

class Gallery(object):
    """Object Gallery stores the DivingLog6 gallery.db tables
    Args:
        file: file name of the database
    Attributes:
        g: List of Gallery table rows as dicts
        index: dict of Gallery table rows by ID
        v: List of Videos table rows as dicts
        v_index: dict of Videos table rows by ID
    """
    def __init__(self, file: str) -> None:
        self.file = file 
        self.g = []
        self.index = {}
        self.v = []
        self.v_index = {}
        
def get_gallery(gallery: Gallery):
    """get the gallery and videos tables from the gallery.db database
    Args:
        gallery: Gallery object
    Returns:
        success: bool
    """
    connection: sqlite3.Connection | None
    connection = create_connection(gallery.file, "sql")
    if connection != None:
        with connection:
            gallery.g = fetch_allof_table("sql", connection, "Gallery", "ID")
            gallery.v = fetch_allof_table("sql", connection, "Videos", "ID")
        for row in gallery.g:
            index = int(row["ID"])
            gallery.index[index] = row
        for row in gallery.v:
            index = int(row["ID"])
            gallery.v_index[index] = row

        return True
    else:
        print("DB connection failed")    
        return False      
    return

def add_gallery2logbook(dl6db: DL6DB, gallery: Gallery):
    """add gallery info to the dl6db Logbook entries
    Args:
        dl6db: DL6DB object
        gallery: Gallery object
    Returns:
        None
    """
    for item in gallery.g:
        dive_number = int(item["ID"])
        if dive_number in dl6db.index["Logbook"]:
            dl6db.index["Logbook"][dive_number]["HasMedia"] = True
            dl6db.index["Logbook"][dive_number]["Url"] = gallery.index[dive_number]["Url"]
    for dive in dl6db.tD["Logbook"]:
        if "HasMedia" not in dive.keys():
            dive["HasMedia"] = False
    return

def add_galleries(dl6db: DL6DB, gallery: Gallery):
    """add gallery info from Logbook UserDefined table to the dl6db Logbook entries
    Args:
        dl6db: DL6DB object
    """    
    if "UserDefined" not in dl6db.tD.keys():
        print("No UserDefined table in DL6DB, cannot add galleries")
        return
    if "GalleryUrl" not in dl6db.tD["UserDefined"][0].keys():
        print("No GalleryUrl field in UserDefined table, cannot add galleries")
        return
    for item in dl6db.tD["UserDefined"]:
        log_id = int(item["LogID"])
        if log_id in dl6db.LogID:
            if item["GalleryUrl"] != None and item["GalleryUrl"] != "":
                dl6db.LogID[log_id]["HasMedia"] = True
                dl6db.LogID[log_id]["Url"] = item["GalleryUrl"] 
                fix_url = fix_encoding(item["GalleryUrl"] )
                gitem = {
                    "ID": dl6db.LogID[log_id]["Number"],
                    "Url": fix_url,
                    "Date": dl6db.LogID[log_id]["Divedate"],
                    "Sitename": dl6db.LogID[log_id]["Place"]
                }
                gallery.g.append(gitem)
                gallery.index[int(gitem["ID"])] = gitem
            else:
                dl6db.LogID[log_id]["HasMedia"] = False
        else:
            continue    
            
    for dive in dl6db.tD["Logbook"]:
        if "HasMedia" not in dive.keys():
            dive["HasMedia"] = False
    return    
        
    