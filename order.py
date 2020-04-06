
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

    # this is the used key in EXIF dictinary for geo location data
    GEOKEY = 34853

    # analised files, adapt or extend it
    FILE_EXTENSIONS = ['.jpg', '.png']

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

        print('Start collecting GEO Information')
        self.resetCounter()

        for file in self.pictureDict:
            if self.incrementCounter() % 100 == 0:
                print('{} '.format(self.COUNTER), end='', flush=True)

            location, geotags, exif = self.geotag.getGeoData(file['path'])
            
            file['location'] = location
            if geotags != None:
                #for i in geotags.keys():
                #    file[i] = geotags[i]
                    
                if self.GEOKEY in exif:
                    file['geoTagBase64'] = self.base64.b64encode(str(exif[Pictures.GEOKEY]).encode('ascii')) 

    def saveDF(self, csvPath):
        picDF = self.pd.DataFrame(self.pictureDict)
        picDF.to_csv(csvPath, index=False, header=True)

    def fromCSV(self, csvPath):
        input_file = self.csv.DictReader(self.codecs.open(csvPath, 'rU', 'utf-8'))
        self.pictureDict = []
        for row in input_file:
            self.pictureDict.append(row) 
        
    def printDublicates(self):
        countDuplicates = {}
        for picture in self.pictureDict:
            if picture['hash'] in countDuplicates:
                countDuplicates[picture['hash']] = countDuplicates[picture['hash']] + 1
            else:
                countDuplicates[picture['hash']] = 0

        onlyDuplicates = [{"{}".format(k): "{}".format(v)} for k, v in countDuplicates.items() if v > 0]
        self.prettyprint(onlyDuplicates)
        print('in total {} duplicates'.format(len(onlyDuplicates)))
            

# this path is the path to your pictures, most likely you want to adapt this!
#path = '/Volumes/DATA/Lars_Data/media/'
path = './pictures'

pictures = Pictures(path)
pictures.collect()
pictures.saveDF('files.csv')

#pictures.fromCSV('files.csv')
print('')
pictures.printDublicates()