""" web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"
"""
import html
import svg
from textwrap import dedent
from datetime import timedelta
from dl6_db import get_dl6_db, DL6DB
from dl6_profiles import diveProfile, lineXY2polygon, mkProfileLineXY

def gen_profile_svg(dl6db: DL6DB, number: int, width: int, height: int,  
                    grids: int =1, temp: int =1,pressure: int =1, header: int =1) ->  str :
    ''' generates a profile SVG image of specified dive
    Args:
        dl6db (DL6DB): the database object
        number (int): the dive number
        width (int): width of SVG in pixels
        height (int): height of SVG in pixels
 
        grids (int, optional): if 1, draw grid lines. Defaults to 1.
        temp (int, optional): if 1, draw temperature profile. Defaults to 1.
        pressure (int, optional): if 1, draw pressure profile. Defaults to 1.
        header (int, optional): if 1, draw header text. Defaults to 1.'''
    log = dl6db.index['Logbook'][number] 
    ## we append all the SVG elements to a list and then add the list to SVG canvas
    elements = []
    elements.append(
        svg.Style(
        text=dedent("""
            .small { font: 10px sans-serif; }
            .big { font: bold 14px sans-serif; }
        """)))
    # adjust profile plot to header and grids
    plotheight = height - (header *20) - (grids *20)
    top_offset = header *20
    
    # print header on top
    if header == 1:
        header_txt = f'Dive {number} on {log['Divedate']} {log['Entrytime']} at {log['Place']}'
        #h_html= header_txt.encode("utf-8", "xmlcharrefreplace")
        h_html = xml_encode( header_txt )
        header_svg= svg.Text(x=1, y=18, text= h_html, class_=["big"])
        elements.append(header_svg)
    
    # get the profile data, if any
    p = diveProfile(dl6db, int(number))
    if p == None:
        elements.append(svg.Text(x=10, y=50, text= "NO PROFILE DATA", class_=["big"]))
    else:
        # gradient #00aefb - #060246
        elements.append(f"""
            <defs>
                <linearGradient id="grad1" x1="0%" x2="0%" y1="0%" y2="100%">
                <stop offset="0%" stop-color="lightBlue" />
                <stop offset="100%" stop-color="darkBlue" />
                </linearGradient>
            </defs>""")
        # draw depth
        xy_depth = mkProfileLineXY(p['timeSamples'], p['depthProfile'], width, plotheight, type="depth", top_offset=top_offset, 
                                   format=1)
        depth_point_list = mkProfileLineXY(p['timeSamples'], p['depthProfile'], width, plotheight, type="depth", top_offset=top_offset, 
                                   format=2)
        depth_point_string = ','.join(depth_point_list)
        depth_poly = svg.Polygon(id=f"svg_depth", points=xy_depth, stroke="blue", fill="url(#grad1)", stroke_width=1)
        elements.append(depth_poly)
        
        ## draw pressure
        if pressure == 1:
            xy_pressure = mkProfileLineXY(p['timeSamples'], p['pressureProfile'], width, plotheight, type="pressure", 
                                          top_offset=top_offset, format= 1)
            press_poly = svg.Polyline(points=xy_pressure, stroke="black", stroke_width=1, fill="none")
            elements.append(press_poly)
        ## draw temperature
        if temp == 1:
            xy_temp = mkProfileLineXY(p['timeSamples'], p['tempProfile'], width, plotheight, type="temperature", 
                                      top_offset=top_offset, format=1)
            temp_poly = svg.Polyline(points=xy_temp, stroke="red", stroke_width=2, fill="none")
            elements.append(temp_poly)   
 
        ## draw gridlines if requested, default on
        if grids == 1:
            ## draw depth grid
            maxDepth = min(p['depthProfile']) * -1
            dd = 5
            while (dd < maxDepth):
                y2 = 20 + (dd / maxDepth) * (plotheight)
                elements.append(svg.Line(x1=0, y1=y2, x2=width, y2=y2, stroke_width=1, stroke="green"))
                elements.append(svg.Text(x=4, y=y2-2, text=f'{int(dd)} m', class_=["small"]))
                elements.append(svg.Text(x=width-40, y=y2-2, text=f'{int(dd)} m', class_=["small"]))
                dd +=5.0
            ## draw time grid
            totalTime = p["timeSamples"][-1]
            tt = 5
            elements.append(svg.Text(x=1, y=height-1, text= "min", class_=["small"]))
            while (tt < totalTime):
                x2 = (tt / totalTime) * width
                elements.append(svg.Line(x1=x2, y1=top_offset, x2=x2, y2=height-top_offset, stroke_width=1, stroke="black"))
                elements.append(svg.Text(x=x2+2, y=height-1, text=f'{int(tt)}', class_=["small"]))
                tt +=5.0
        ## crosshair        
        elements.append(svg.Line(id=f"svg_vline",x1=0, y1=0, x2=0, y2=height-top_offset, stroke_width=2, stroke="orange"))
        elements.append(svg.Line(id=f"svg_hline",x1=0, y1=0, x2=width, y2=0, stroke_width=2, stroke="orange"))
        elements.append(svg.Text(id=f"svg_coordText", x=10, y=50, text='time: -, depth: -', class_=["small"]))
    ### create the canvas
    viewbox = svg.ViewBoxSpec(0, 0, width, height)
    canvas = svg.SVG(id= f'svg_profile_{number}',width=width, height=height, elements=elements, 
                     viewBox= viewbox)
    if p != None:
        tracker = f"\n<script>\n var depth_points = [{depth_point_string}];\n</script>"
    else:
        tracker = ""
 
    return canvas.as_str() + tracker

def xml_encode(i: str)-> str:
    """ converts UTF-8 scandinavian characters to XML escapes
    Args:
        i (str): input utf-8 string
    Returns:
        str: &öÖäÄåÅ replaced by XML encoding
    """
    o= i.replace('&', '&#38;')
    o= o.replace('ö', '&#246;')
    o= o.replace('Ö', '&#214;')
    o= o.replace('ä', '&#228;')
    o= o.replace('Ä', '&#196;')
    o= o.replace('å', '&#229;')
    o= o.replace('Å', '&#197;')
    return o

 