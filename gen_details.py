import base64
import os
import re
from dl6_db import DL6DB
from gallery_db import Gallery
from gen_svg import gen_profile_svg


def printDBdata(in_data):
  html = "<div class= 'flex2'>"

  for key, value in in_data.items():
    if key == "Comments": continue
    if key.startswith("Profile"): continue
    if key.startswith("Scan"): continue
    if key == "Url": 
        value = f'<a href="{value}" target="_blank">media gallery</a>'
    if value == None:
        value = "<null>"

    html += f"""<fieldset class='fset' id= 'dlog_{key}'>
    <legend class="field_legend">{key}</legend>
    <span class='diveViewField'>{value}</span>
    </fieldset>"""
  
  html += "</div>"
  return html


def hyperlink_urls(text):
    # Regex pattern to match URLs
    url_pattern = re.compile(r'(https?://[^\s]+)')
    
    # Replace each URL with the HTML anchor tag
    return url_pattern.sub(
        lambda match: f'<a href="{match.group(0)}" target="_blank" rel="noopener noreferrer">{match.group(0)}</a>',
        text
    )


def printComments(in_data):
    html = "<div class= 'flex3'>"
    if in_data["Comments"] == None:
        comment_txt = "<b>No comments</b>"
    else:   
        comment_txt = in_data["Comments"] #.replace('\n', '<br>\n')
    comment_txt = hyperlink_urls(comment_txt)
        
    html += f"""<fieldset><legend class="field_legend">Comments</legend>
    <span style="white-space: pre-line;">{comment_txt}</span></fieldset></div>"""
  
    return html

def html_all_details(dl6db: DL6DB, tables: list, outdirectory: str, gallery_use: bool = False) -> None:
    """Generate HTML detail files for all places and buddies in the database.
    args:
        dl6db: DL6DB object containing the database details. 
        tables: List of table names to generate HTML for.   
        outdirectory: Directory where HTML files will be saved.
    """
    for table in tables:
        # map table name to function suffix (Logbook -> dive)
        suffix = "dive" if table == "Logbook" else table.lower()
        func_name = f"html_{suffix}"
        func = globals().get(func_name)

        if not callable(func):
            print(f"Skipping {table}: function {func_name} not found")
            continue

        for item in dl6db.tD.get(table, []):
            if table == "Logbook": 
                func(item, dl6db, outdirectory, gallery_use) 
            else:
                func(item, dl6db, outdirectory)
        print(f'\nGenerated HTML for all {table} entries {len(dl6db.tD[table])}.')     

def divelist(dl6db: DL6DB, table: str, number: int) -> str:
    """Return HTML list of dives associated with a given table and number.
    args:
        dl6db: DL6DB object containing the database details.    
        table: Table name (e.g., "Place", "Buddy", "Trip").
        number: ID number in the specified table.
    """
    dlist_html = f"<h3>Dives for this {table}</h3><ol>" 
    if number not in dl6db.dmap[table]:
        dlist_html += f"<li>No dives recorded for this {table}</ol>"
    else:
        for dive_num in dl6db.dmap[table][number]:
            dive = dl6db.index["Logbook"][dive_num]
            dlist_html += f'<li class="dive_link" onclick="link_dive({dive_num})">Dive {dive["Number"]} {dive['Divedate']} {dive['Entrytime']}</li>' 
        dlist_html += "</ol>"      
    return dlist_html  

def html_place(place: dict, dl6db: DL6DB, outdirectory: str) -> str:
    """Return HTML representation of a place dictionary.    
    args:
        dive: Dictionary containing dive details.
        dl6db: DL6DB object containing the database details.    
        outdirectory: Directory where HTML files will be saved.
    """
    if not place:
        return "<p>No place data available.</p>"

    number = place["ID"]
    html = f'<h2>Place: {number} "{place["Place"]}"</h2>\n'
    html += f'<button id="Place_MAP" onclick="gotoTab(\'Map\',{number})">MAP</button>'
    html += printDBdata(place)
    html += printComments(place)
    html += divelist(dl6db, "Place", number)
    
    filename = f"{outdirectory}{os.sep}html{os.sep}place_{number}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f'Wrote {filename}          \r',end='')
    return html

def dive_view_buttons(tripID, buddyID, placeID) -> str:
    """Return HTML buttons for navigating dive views."""
    return f"""
        <button id="prev" onclick="prevLog()">PREVIOUS</button>
        <button id="next" onclick="nextLog()">NEXT</button>
        <button id="last" onclick="lastLog()">Last</button>

        <span>goto: </span>
        <input type="number" id="dlogGotoNumber" min="1" onchange="dlogGotoNumber()"> 

        <button id="Dive_BUDDY"  onclick="gotoTab('Buddy',{buddyID})">BUDDY</button>
        <button id="Dive_TRIP"   onclick="gotoTab('Trip',{tripID})">TRIP</button>        
        <button id="Dive_PLACE"  onclick="gotoTab('Place',{placeID})">PLACE</button>
        <button id="Dive_MAP"    onclick="gotoTab('Map',{placeID})">MAP</button>
        """

def photo_button(dive: dict) -> str:
    """Return HTML button for navigating photos."""
    if dive['HasMedia'] == True:
        url = dive['Url']   
        return f'<button id="Dive_PHOTOS" onclick="gotoGallery({dive["Number"]})">PHOTOS</button>'
    else:
        return '<span id="Dive_PHOTOS" style="color: grey;" title="No media">NO PHOTOS</span>'

def html_dive(dive: dict, dl6db: DL6DB, outdirectory: str, gallery_use: bool = False) -> str:
    '''Return HTML representation of a dive dictionary.
    args:
        dive: Dictionary containing dive details.
        dl6db: DL6DB object containing the database details.    
        outdirectory: Directory where HTML files will be saved.
    '''
    number = dive["Number"]
    if not dive["BuddyIDs"]: 
        buddyID = None
    else:
        buddyID = dive["BuddyIDs"][0]
    
    html = f'<h2 id="dlog_header">Dive {number} on {dive['Divedate']} {dive['Entrytime']} at "{dive['Place']}"</h2>\n'
    html += "<div id='dive_profile'>"
    html += gen_profile_svg(dl6db, number=number, width=1000, height=300 )
    html += "</div>\n<div id='dive_divider'></div>\n<div id='dive_bottom'>"
    html += dive_view_buttons(dive['TripID'], buddyID, dive['PlaceID'])
    if gallery_use == True:
        html += photo_button(dive)
    html += printDBdata(dive)
    html += printComments(dive)
    html += "</div>"
 
    filename = f"{outdirectory}{os.sep}html{os.sep}dive_{number}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f'Wrote {filename}              \r',end='')
    return html

def html_trip(trip: dict, dl6db: DL6DB, outdirectory: str) -> str:
    """Return HTML representation of a trip dictionary. """
    number = trip["ID"]
    html = f'<h2>Trip: {number} "{trip['TripName']}"</h2>\n'
    html += printDBdata(trip)
    html += printComments(trip)
    html += divelist(dl6db, "Trip", number)
 
    filename = f"{outdirectory}{os.sep}html{os.sep}trip_{number}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f'Wrote {filename}            \r',end='')
    return html 

def html_buddy(buddy: dict, dl6db: DL6DB, outdirectory: str) -> str:
    """Return HTML representation of a buddy dictionary. """
    number = buddy["ID"]
    html = f'<h2>Buddy: {number} "{buddy['FirstName']} {buddy['LastName']}"</h2>\n'
    html += printDBdata(buddy)
    html += printComments(buddy)
    html += divelist(dl6db, "Buddy", number)
 
    filename = f"{outdirectory}{os.sep}html{os.sep}buddy_{number}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f'Wrote {filename}               \r',end='')
    return html 

def html_equipment(equipment: dict, dl6db: DL6DB, outdirectory: str) -> str:
    """Return HTML representation of an equipment dictionary. """
    number = equipment["ID"]
    html = f'<h2>Equipment: {number} "{equipment['Object']} {equipment['Manufacturer']}"</h2>\n'
    html += printDBdata(equipment)
    html += printComments(equipment)
 
    filename = f"{outdirectory}{os.sep}html{os.sep}equipment_{number}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f'Wrote {filename}              \r',end='')
    return html 

def html_brevets (brevet: dict, dl6db: DL6DB, outdirectory: str) -> str:
    """Return HTML representation of a brevet dictionary. """
    number = brevet["ID"]
    scan = base64.b64encode( brevet["Scan1"] ).decode('utf-8') if brevet["Scan1"] != None else ""
    html = f'<h2>Brevet: {number} "{brevet['Brevet']} {brevet['Org']}"</h2>\n'
    html += printDBdata(brevet)
    html += "<h3>Scan</h3>\n"
    html += f"<div>\n<img src='data:image/png;base64,{scan}'\n</div>\n"
    html += "<hr>\n"
 
    filename = f"{outdirectory}{os.sep}html{os.sep}brevets_{number}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f'Wrote {filename}              \r',end='')
    return html 