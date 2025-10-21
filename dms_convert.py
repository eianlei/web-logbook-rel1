""" web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"
"""

import re
"""
parses DMS formatted coordinate to decimal
"""

def ParseDMS(input):
    """
    parses DMS formatted coordinate to decimal
    """
    parts = re.split(r'[^\d\w\.]+', input)
    decimal = ConvertDMSToDD(parts[0], parts[1], parts[2], parts[3]);
    return decimal

def ConvertDMSToDD(degrees, minutes, seconds, direction):
    """Convert DMS to decimal degrees
    """
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == "S" or direction == "W" :
        return dd * -1.0
    return dd

if __name__ == "__main__":
    """ test the ParseDMS function
    """
    test1 = '60°2\'31.19"N'
    print (f"{test1} -> {ParseDMS(test1)} ")
    test1 = "19°53'52.31\"E"
    print (f"{test1} -> {ParseDMS(test1)} ")
    test1 = '110°59\'59.19"S'
    print (f"{test1} -> {ParseDMS(test1)} ")
    test1 = "0°53'52.31\"W"
    print (f"{test1} -> {ParseDMS(test1)} ")