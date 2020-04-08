from order import Pictures
import argparse

parser = argparse.ArgumentParser(description='Example with long option names')

parser.add_argument('--fromCSV', dest="loadFromCSV", action="store", default=False)
parser.add_argument('showDuplicates', dest="showDuplicates", action="store")
parser.add_argument('moveDuplicates', dest="moveDuplicates", action="store")
parser.add_argument('--dry', action="store", dest="dryRun", type=int)

print(parser.parse_args([ '--fromCSV', 'showDuplicates', 'moveDuplicates', '--dry' ]))


# this path is the path to your pictures, most likely you want to adapt this!
#path = '/Volumes/DATA/Lars_Data/media/'
#path = '/app/testPictures'
#pathToStoreDuplicatePictures = '/app/duplicatePictures'

#pictures = Pictures(path)
#pictures.collect()
#pictures.saveDF('files.csv')

#pictures.fromCSV('./files.csv')
#pictures.calculateDuplicatesAndSafe()

#pictures.moveDuplicatePicturesTo(pathToStoreDuplicatePictures)