""" web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"
"""

from dl6_db import DL6DB


def mkProfiles(profileInt: int, profile: str, profile2: str) -> dict:
    '''make floating point profile arrays of the DL6 strings to a dict
    '''
    # init the arrays
    prof = {}
    prof['timeSamples']  = []
    prof['depthProfile'] = []
    prof['tempProfile'] = []
    prof['pressureProfile'] = []
    if profile == None or profileInt == None :
        return None
    slen = len(profile)
    time = 0
    rrec = range(0, slen, 12) # doing range with a float is a killer
    for n in rrec :
        depth_str = f'-{profile[n : n+3]}.{profile[n + 3: n + 5]}'
        depth = float(depth_str)
        prof['timeSamples'].append(time)
        prof['depthProfile'].append(depth)
        time += profileInt

    # process the Profile2, temp and pressure
    if profile2 != None:
        slen = len(profile2)
        if slen > 0 : # but only of there is a Profile2 string
            for n in range(0, slen, 11):
                temp_str  = f'{profile2[n  : n+2]}.{profile2[n + 2: n + 3]}'
                pres_str  = f'{profile2[n+3: n+6]}.{profile2[n + 6: n + 7]}'
                temp = float(temp_str)
                pres = float(pres_str)
                prof['tempProfile'].append(temp)
                prof['pressureProfile'].append(pres)

    return prof

def diveProfile(dl6db: DL6DB, num_int: int) -> dict:
    """get the profile dict for a given dive number integer from the dl6db object
    Args:
        dl6db: DL6DB object
        num_int: dive number integer
    Returns:
        profile_dict: dict with timeSamples, depthProfile, tempProfile, pressureProfile lists
    """
    if dl6db.index['Logbook'][num_int]['ProfileInt']:
        profile = dl6db.index['Logbook'][num_int]['Profile']
        profile2 = dl6db.index['Logbook'][num_int]['Profile2']
        profileInt = dl6db.index['Logbook'][num_int]['ProfileInt']/60.0
        profile_dict = mkProfiles(profileInt, profile, profile2)
        return profile_dict
    else:
        return None

def mkProfileLineXY(timeSamples, profileSamples, width, height, type="depth", top_offset=0, format=0) -> list:
    ''' format=0 default:
          convert a profile to a list of (x,y) integer 2-tuples, given height, width, scale
        format=1, instead of (x,y) tuples return constant x,y, x,y, list
        format=2, return a list of strings {x:0,y:0,d:0.0} for javascript
          where d is the depth value, negative for depth, positive for temp and pressure
    '''
    if len(timeSamples) == 0 or len(profileSamples) == 0:
        return []
    if type == "depth":
        if format == 0:
            xy_list = [(0,top_offset)]
        elif format == 1:
            xy_list = [0, top_offset]
        elif format == 2:
            xy_list = [ f"{{x:0,y:{top_offset:.0f},d:0,t:0}}" ]
    else:
        xy_list = []    
    if type == "depth":
        maxValue = min(profileSamples)
    else:    
        maxValue = max(profileSamples)
    for index, t in enumerate(timeSamples):
        x = t / timeSamples[-1] * width
        try:
            point = profileSamples[index]
        except:
            return xy_list    
        match type:
            case "depth":
                y = (point / maxValue) * height + top_offset
            case "pressure":
                y = (1.0 - (point / 300.0)) * height + top_offset
            case "temperature":
                y = (1.0 - (point / 40.0)) * height + top_offset   
            case _:
                y= 1             
        if format == 0:        
            xy_list.append((int(x), int(y)))
        elif format == 1:
            xy_list.extend([ int(x), int(y) ])
        elif format == 2:
            xy_list.append( f"{{x:{x:.0f},y:{y:.0f},d:{-point:.1f},t:{t:.1f}}}" )
    
    return xy_list

def lineXY2polygon(xy: list):
    xy.append(  xy[0] )
    return xy