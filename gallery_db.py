# 2025-09-11
""" Handles the gallery.db database
"""
import sqlite3 
from dl6_db import fetch_allof_table, create_connection

class Gallery(object):
    def __init__(self, file: str) -> None:
        self.file = file 
        self.g = []
        self.index = {}
        self.v = []
        self.v_index = {}
        
def get_gallery(gallery: Gallery):
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

def add_gallery2logbook(dl6db, gallery):
    for item in gallery.g:
        dive_number = int(item["ID"])
        if dive_number in dl6db.index["Logbook"]:
            dl6db.index["Logbook"][dive_number]["HasMedia"] = True
            dl6db.index["Logbook"][dive_number]["Url"] = gallery.index[dive_number]["Url"]
    for dive in dl6db.tD["Logbook"]:
        if "HasMedia" not in dive.keys():
            dive["HasMedia"] = False

 
    return
    