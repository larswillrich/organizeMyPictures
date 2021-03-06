
class Pictures:
    import os
    import hashlib
    import json
    import geotag
    from os.path import join, getsize
    from datetime import datetime
    import base64
    import pandas as pd
    import csv
    import codecs
    import shutil

    # this is the used key in EXIF dictinary for geo location data
    GEOKEY = 34853

    # analised files, adapt or extend it
    FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png', 'tiff']

    def __init__(self, path):
        self.path = path
        self.resetCounter()

    prettyprint = lambda self, obj: print(self.json.dumps(obj, indent=4, ensure_ascii=False))

    def incrementCounter(self):
        self.COUNTER += 1
        return self.COUNTER

    def resetCounter(self):
        self.COUNTER = 0

    def fileCriteriaAreGiven(self, currentFile):
        if self.incrementCounter() % 100 == 0:
            print('{} '.format(self.COUNTER), end='', flush=True)
        iteration = iter(i for i in Pictures.FILE_EXTENSIONS if currentFile.lower().endswith(i))
        return next(iteration, None) != None

    def getMd5(self, fname):
        hash_md5 = self.hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    getmtime = lambda self, file: self.datetime.utcfromtimestamp(self.os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
    getctime = lambda self, file: self.datetime.utcfromtimestamp(self.os.path.getctime(file)).strftime('%Y-%m-%d %H:%M:%S')

    def collect(self):
        # get all files
        print('collect files in ...{}'.format(self.path))
        getAllFiles = lambda self: [self.os.path.join(root, file) for root, dir, files in self.os.walk(self.path, topdown=False) for file in files]

        allFiles = getAllFiles(self)
        print('{} files found'.format(len(allFiles)))

        # organize in dictinary with usefull informations and filter out all 'non pictures'

        print('Start collecting metainformation')
        self.pictureDict = [
            {'path': file, 
            'hash': self.getMd5(file), 
            'creationTime': self.getctime(file),
            'modificationTime': self.getmtime(file),
            'size': self.os.path.getsize(file)
            } 
            for file in allFiles if self.fileCriteriaAreGiven(file)]


    def collectGeoInformation(self):
        print()
        print()
        print('Start collecting GEO Information')
        self.resetCounter()

        
        for file in self.pictureDict:
            if self.incrementCounter() % 100 == 0:
                print('{} '.format(self.COUNTER), end='', flush=True)

            location, geotags, exif = self.geotag.getGeoData(file['path'])
            
            if location == None:
                file['location'] = 'NO_GEO_LOCATION' 
            else:
                file['location'] = location
            if geotags != None:
                if self.GEOKEY in exif:
                    encodedGEO = str(exif[Pictures.GEOKEY]).encode('utf-8')
                    base64encodedGEO = self.base64.b64encode(encodedGEO)
                    xmlfileformat = base64encodedGEO.decode('utf-8')

                    file['geoTagBase64'] = xmlfileformat

        self.geotag.storeDB()

    def saveDF(self, csvPath):
        picDF = self.pd.DataFrame(self.pictureDict)
        picDF.to_csv(csvPath, index=False, header=True)

    def fromCSV(self, csvPath):
        input_file = self.csv.DictReader(self.codecs.open(csvPath, 'rU', 'utf-8'))
        self.pictureDict = []
        for row in input_file:
            self.pictureDict.append(row) 
    
    def printGeoCodeStatistic(self):
        noLocationAvailable = 0
        locationAvailable = 0
        locationStatistics = {}

        for file in self.pictureDict:
            if 'location' not in file:
                print('no location data evailable. You should configure the program probably')
                return
            if file['location'] != 'NO_GEO_LOCATION' :
                locationAvailable += 1

                location = file['location'].split(",")[len(file['location'].split(","))-1].strip()
                if location not in locationStatistics:
                    locationStatistics[location] = 1
                else:
                    locationStatistics[location] = locationStatistics[location] + 1
            else:
                noLocationAvailable += 1
            
        print('With Geo Informations: {}'.format(locationAvailable))
        print('WithOUT Geo Informations: {}'.format(noLocationAvailable))
        print()
        print('Here is an overview how many pictures have been taken somewhere:')
        self.prettyprint(locationStatistics)

    def calculateAndPrintDuplicates(self):
        countDuplicates = {}
        for picture in self.pictureDict:
            if picture['hash'] in countDuplicates:
                countDuplicates[picture['hash']]['duplicates'] = countDuplicates[picture['hash']]['duplicates'] + 1

                # add path of every duplicated photo. Remember, the first picture, when the number of duplicates is 0, don't add a path!
                countDuplicates[picture['hash']]['pathes'].append(picture["path"])
            else:
                countDuplicates[picture['hash']] = {
                    'duplicates': 0,
                    'creationTime': picture["creationTime"],
                    'pathes': []
                }

        self.onlyDuplicates = [{k: v} for k, v in countDuplicates.items() if v['duplicates'] > 0]
        self.prettyprint(self.onlyDuplicates)
        print('in total {} pictures have duplicates'.format(len(self.onlyDuplicates)))

    def moveDuplicatePicturesTo(self, pathToStoreDuplicatePictures):
        
        # are there any pictures available? Maybe not calculated, so do it again
        if not self.onlyDuplicates:
            self.calculateAndPrintDuplicates()

        # if path where to store duplicates not exist, create one
        if not self.os.path.exists(pathToStoreDuplicatePictures):
            self.os.mkdir(pathToStoreDuplicatePictures)

        # I don't want to have name conflicts, add a number!
        counter = 0
        for duplicatePicture in self.onlyDuplicates:
            pictureObject = duplicatePicture[next(iter(duplicatePicture))]

            for path in pictureObject['pathes']:
                print('move')
                print(path)

                counter = counter + 1
                noUsage, file_extension = self.os.path.splitext(path)
                self.shutil.move(path, '{}_{}{}'.format(self.os.path.join(pathToStoreDuplicatePictures, pictureObject['creationTime']),counter, file_extension))
    
    def addGeoTagToPhotos(self, dry):
        self.geotag.addGeoTagToPhotos(self.pictureDict, dry)

    def alreadyReadGeoTags(self):
        if 'location' in self.pictureDict[0]:
            return True
        return False
