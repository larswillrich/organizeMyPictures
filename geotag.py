# ==========================================
# ==========================================
# 
# This source code is based on 
# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
# 
# ==========================================
# ==========================================

import requests
from PIL.ExifTags import GPSTAGS, TAGS
from PIL import Image
import os

def get_exif(filename):
    image = Image.open(filename)
    image.verify()

    try:
        return image._getexif()
    except AttributeError:
        return None

def get_geotagging(exif):
    if not exif:
        return None
        #raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                return None
                #raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def get_location(geotags):
    coords = get_coordinates(geotags)

    uri = 'https://reverse.geocoder.api.here.com/6.2/reversegeocode.json'
    headers = {}
    params = {
        'app_id': os.environ['HERE_APP_ID'],
        'app_code': os.environ['HERE_APP_CODE'],
        'prox': "%s,%s" % coords,
        'gen': 9,
        'mode': 'retrieveAddresses',
        'maxresults': 1,
    }

    response = requests.get(uri, headers=headers, params=params)
    try:
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(str(e))
        return {}


def getGeoData(file):
    exif = get_exif(file)

    geotags = None if exif == None else get_geotagging(exif)
    
    if (geotags == None): return None, None, exif

    if 'GPSLatitude' not in geotags: return None, geotags, exif

#    uncommended, because I don't want to speak with the HERE API in testing due to ressource limits in free version
#    include again!!
#
#    return get_location(geotags)['Response']['View'][0]['Result'][0]['Location']['Address']['Label'], geotags, exif
    return 'GEO_LOCATION', geotags, exif