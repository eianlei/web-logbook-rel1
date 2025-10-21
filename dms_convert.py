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
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == "S" or direction == "W" :
        return dd * -1.0
    return dd

if __name__ == "__main__":
    test1 = '60°2\'31.19"N'
    print (f"{test1} -> {ParseDMS(test1)} ")
    test1 = "19°53'52.31\"E"
    print (f"{test1} -> {ParseDMS(test1)} ")
    test1 = '110°59\'59.19"S'
    print (f"{test1} -> {ParseDMS(test1)} ")
    test1 = "0°53'52.31\"W"
    print (f"{test1} -> {ParseDMS(test1)} ")