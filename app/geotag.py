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
import pickledb
import piexif

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

    key = str(geotags)
    geoLocation = db.get(key)
    if not geoLocation:
        print('doing API call')

        # call api, because key is not yet present in db
        geoLocation = get_location(geotags)
        db.set(key, geoLocation)

    if (len(geoLocation['Response']['View']) < 1): return None, geotags, exif

    return geoLocation['Response']['View'][0]['Result'][0]['Location']['Address']['Label'], geotags, exif

def storeDB():
    db.dump()

db = pickledb.load('/app/geoCacheDb/geolocations.db', False)

import json
prettyprint = lambda obj: print(json.dumps(obj, indent=4, ensure_ascii=False))

from datetime import datetime
convertToDate = lambda str: datetime.strptime(str, '%Y-%m-%d %H:%M:%S').date().strftime("%d.%m.%Y")

# returns a map
# key: time down to a day
# value: a LIST of all photos within the same day
def getTimeOrderedPhotos(photos):

    def byModificationTime(elem):
        return elem['modificationTime']

    photos.sort(key=byModificationTime)

    photoMap = {}
    for photo in photos:
        date = convertToDate(photo['modificationTime'])
        if date not in photoMap:
            photoMap[date] = [photo]
        else:
            photoMap[date].append(photo)
    
    return photoMap

def findOnePhotoWithGeoTag(photosByDay):
    photosWithGeoTag = []
    for photo in photosByDay:
        if photo["location"] != 'NO_GEO_LOCATION':
            photosWithGeoTag.append(photo)
    if (len(photosWithGeoTag) == 0):
        return None, 0
    return photosWithGeoTag[int(len(photosWithGeoTag)/2)], len(photosWithGeoTag)

def getAllPhotosWithoutGeoTag(photosByDay):
    photosWithoutGeoLocation = []
    for photo in photosByDay:
        if photo["location"] == 'NO_GEO_LOCATION':
            photosWithoutGeoLocation.append(photo)
    return photosWithoutGeoLocation

import base64

def takeOverGeoTag(photoWithoutGeoTag, photoWithGeoTag):

    # get original exif data first!
    FILE_EXTENSIONS = ['.jpg', '.jpeg', 'tiff']
    iteration = iter(i for i in FILE_EXTENSIONS if photoWithoutGeoTag['path'].lower().endswith(i))
    if next(iteration, None) == None:
        print(("skipping {}".format(photoWithoutGeoTag['path'])))
        return

    exif_data = piexif.load(photoWithGeoTag['path'])
    exif_dataToUpdate = piexif.load(photoWithoutGeoTag['path'])

    newGPS = {"GPS": exif_data['GPS']}
    
    # update exif data to include GPS tag
    exif_dataToUpdate.update(newGPS)
    exif_bytes = piexif.dump(exif_dataToUpdate)
    piexif.insert(exif_bytes, photoWithoutGeoTag['path'])
    
    return False


def addGeoTagToPhotos(photos, dry):
    
    noGeoTagsFountCounter = 0
    # in order to have the complexity low, we want to order the photos first by time
    orderedPhotos = getTimeOrderedPhotos(photos)

    for day, photosInSameTime in orderedPhotos.items():
        _, amountWithGeoTag = findOnePhotoWithGeoTag(photosInSameTime)
        print('{}: {} pictures and {} with GeoInformaton'.format(day, len(photosInSameTime), amountWithGeoTag))


    for _, photosInSameTime in orderedPhotos.items():

        photoWithGeoTag, _ = findOnePhotoWithGeoTag(photosInSameTime)

        if photoWithGeoTag is None:
            noGeoTagsFountCounter += 1
            continue

        photosWithoutGeoTag = getAllPhotosWithoutGeoTag(photosInSameTime)
        
        if not dry:
            for photoWithoutGeoTag in photosWithoutGeoTag:
                takeOverGeoTag(photoWithoutGeoTag, photoWithGeoTag)
    
    print('no geo tags found for {} days'.format(noGeoTagsFountCounter))





