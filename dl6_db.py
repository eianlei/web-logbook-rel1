""" 2025-10-21 dl6_db.py
web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"
"""

"""Object DL6DB stores all of DivingLog6 sqlite database tables defined in dl6_tables object
functions to open the database and fetch all data to DL6DB
"""
import sqlite3
#import pyodbc
from sqlite3 import Error
from operator import itemgetter
from typing import List, Dict
from dataclasses import dataclass, field
from dms_convert import ParseDMS
 

class DL6DB(object):
    """Object DL6DB stores DivingLog6 sqlite database tables

    Args:
        file: file name of the database
    Attributes:
        tD[table]: 
    """
    def __init__(self, file: str, db_type: str):
        self.file = file
        self.db_type = db_type
        self.tD: dict = {}
        self.index: dict = {}
        self.tables_keys: list = []
        self.dive_first_num: int = 0
        self.dive_last_num: int = 0
        self.dive_count: int = 0
        self.diveNum2Logbook = {}
        self.dmap: dict = {}
        # # extra to handele gallery
        # self.gallery: Gallery  
        # self.gallery_idlist: List[int] = []
        
    def newTable(self, tableName: str):
        """create a new table as a List
           also create index dict for each table
        Args:
            tableName (str): name of table
        """
        self.tD[tableName] = []
        self.index[tableName] = {}
        
    def newDmap(self, tableName: str):
        self.dmap[tableName] = {}

def create_connection(db_file: str, db_type: str) -> sqlite3.Connection  | None:
    """ create a database connection to the SQLite or Microsoft Access database
        specified by the db_file
    :param db_file: database file
    :param db_type: sql | mdb
    :return: Connection object or None
    """
    if db_type == "sql":
        conn : sqlite3.Connection
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
            return None
    elif db_type == "mdb":
        print("mdb not implemented here")
        return None
    else:
        print(f"unknown db type {db_type}")
        return None        

def fetch_allof_table(db_type: str, conn: sqlite3.Connection , 
                      table: str, sort_key: str)-> list | None:
    """fetches all rows from database table and returns a list of rows
        sorted by a key
    Args:
        db_type: sql | mdb
        conn (sqlite3.Connection): opened connection to sqlite3 database
        table (str): name of table to fetch
        sort_key (str): the column name used as sorting key

    Returns:
        list: list of all rows of the table accessible by column names via dict
    """
    if db_type == "sql":
        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}
        
        #conn.row_factory = sqlite3.Row # this allows you to access row column values by column name
        conn.row_factory = dict_factory # convert table rows to dict
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} ORDER BY {sort_key}")
        rows: list
        rows = cur.fetchall()
        return rows

    else:
        print(f"unknown db type {db_type}")
        return None         

""" specify here which tables and sort keys and index keys you want, assign to DL6DB 
    1st element is table name, then sort key, then indexing key
    use with get_dl6_db, index_dl6_db
"""
dl6_tables = [("Logbook", "Number", "Number"),
              ("Trip", "ID", "ID"),
              ("Place", "Place", "ID"),
              ("Buddy", "FirstName", "ID"),
              ("Equipment", "Object", "ID"),
              ("Country", "Country", "ID"),
              ("City", "City", "ID"),
              ("Brevets", "CertDate", "ID")
              ]

def get_dl6_db(db: DL6DB)-> bool:
    """all of DivingLog6 sqlite database tables defined in dl6_tables object 
    fetched to arg db

    Args:
        db (DL6DB): object instance where database data is stored
        specify in db.tables_keys the tables you want
    Returns:
        bool: True if fetching data ok, False if a fail
    """

    connection: sqlite3.Connection | None
    connection = create_connection(db.file, db.db_type)
    if connection != None:
        with connection:
            for table, sort_key, idx in db.tables_keys:
                print(f'fetching table {table}')
                r = fetch_allof_table(db.db_type, connection, table, sort_key)
                db.newTable(table)
                db.tD[table] = r
        db.dive_first_num = int(db.tD["Logbook"][0]["Number"])
        db.dive_last_num = int(db.tD["Logbook"][-1]["Number"])
        db.dive_count = len(db.tD["Logbook"])
        return True
    else:
        print("DB connection failed")    
        return False      

def index_dl6_db(db: DL6DB):
    """create indexes for all tables

    Args:
        db (DL6DB): _description_
    """    
    # iterate all tables
    for t, k, idx in db.tables_keys:
        # iterate all rows in table and create index 
        for row in db.tD[t]:
            index = row[idx]
            db.index[t][index] = row
    print("indexing done")        
    return

def xcheck_Logbook(db: DL6DB):
    """ cross check Logbook against other tables for join of data

    Args:
        table (_type_): _description_
        Trip_dives (dict): _description_
        Place_dives (dict): _description_
    """    
    other_tables = [('Trip', 'TripID'),
                    ('Place', 'PlaceID'),
                    ('Buddy', 'BuddyIDs'),
                    ('Equipment', 'UsedEquip'),
                    ('Brevets', None)]
    for ot, _ in other_tables:
        _ = db.newDmap(ot)

    for row in db.tD['Logbook']:
        for ot, tkey in other_tables:
            if tkey == None:
                break
            if row[tkey] != None and row[tkey] != '':
                if isinstance(row[tkey], int): 
                    id_list = [ row[tkey] ]
                else:
                    if "," in row[tkey]: 
                        id_list =   [int(i) for i in row[tkey].split(',')] # need to have int list
                    else:
                        id_list = [int(row[tkey])]
                    row[tkey] = id_list # convert str csv to list of int
                for eID in id_list:  
                    if eID in db.dmap[ot].keys():
                        db.dmap[ot][eID].append(row["Number"] ) 
                    else:
                        db.dmap[ot][eID] = [ row["Number"] ]         

    return 

def tripMapBounds(db: DL6DB):
    ''' scans the table Trip, and then all linked dives, 
        and then finds the MapBounds = [maxLat, minLon], [minLat, maxLon]
    '''
    for TripRow in db.tD['Trip']:
        tripID = TripRow['ID']
        if db.dmap['Trip'][tripID] != None:
            TripRow['DiveIDs'] = db.dmap['Trip'][tripID]
            maxLat = -89.9
            minLat = 89.9
            maxLon = -179.9
            minLon = 179.9
            for diveID in db.dmap['Trip'][tripID]:
                thisDive  = db.index['Logbook'][diveID]
                placeID = thisDive['PlaceID']
                try:
                    thisPlace = db.index['Place'][placeID]
                    thisPlace['TripID'] = tripID
                except:
                    print(f'tripMapBounds: {tripID} {diveID} {placeID}')
                    continue
                if thisPlace['Lat'] != None and thisPlace['Lon'] != None:
                    thisDive['Lat'] = thisPlace['Lat']
                    thisDive['Lon'] = thisPlace['Lon']  
                    thisPlace['LatDec'] = LatDec = ParseDMS(thisPlace['Lat'])
                    thisPlace['LonDec'] = LonDec = ParseDMS(thisPlace['Lon'])
                    maxLat = max(LatDec, maxLat)
                    minLat = min(LatDec, minLat)
                    maxLon = max(LonDec, maxLon)
                    minLon = min(LonDec, minLon)
            TripRow['maxNW'] = [maxLat, minLon]
            TripRow['minSE'] = [minLat, maxLon]
    return

def mdb_clean(db: DL6DB):
    """ cleans the data from MDB Access database that is different from sqlite DB data

    Args:
        db (DL6DB): _description_
    """   
    for row in db.tD['Logbook']:
        mdb_divedate= str( row['Divedate'] )
        pure_divedate = mdb_divedate[:10]
        row['Divedate'] = pure_divedate
        #
        Entrytime= str( row['Entrytime'] )
        pure_Entrytime = Entrytime[11:16]
        row['Entrytime'] = pure_Entrytime
        
    return
# end