from order import Pictures
import os
from pathlib import Path
import sys

# functions
def isCSVFilePresent(path):
    csvFile = Path(os.path.join(path, 'files.csv'))
    if csvFile.is_file():
        return True
    return False

def end():
    print()
    print('good bye ;)')
    sys.exit()

# check parameter
# =====================================

# printDuplicates ???
if os.environ.get('printDuplicates') is not None:
    printDuplicates = os.environ['printDuplicates']
else:
    printDuplicates = 'false'

# addGeoTag ???
if os.environ.get('addGeoTag') is not None:
    addGeoTag = os.environ['addGeoTag']
else:
    addGeoTag = 'false'

# moveDuplicates ???
if os.environ.get('moveDuplicates') is not None:
    moveDuplicates = os.environ['moveDuplicates']
else:
    moveDuplicates = 'false'

# path to pictures in docker container
path = '/app/picturesToProcess'

# read from CSV File, if exists    
readFromCSV = isCSVFilePresent(path)

# start of picture program
# =====================================
print('Welcome to my picture Program. More then happy to have you here!')

pictures = Pictures(path)
if readFromCSV:
    print('Found files.csv file, so do not create a new csv file but use the existing one.')
    pictures.fromCSV(os.path.join(path, 'files.csv'))        
else: 
    print('Did not find a files.csv, where may already some analysing data are already available. But seems not, so I will create one for you ...')
    pictures.collect()
    pictures.saveDF(os.path.join(path, 'files.csv'))

if printDuplicates == 'true' or moveDuplicates == 'true':
    print('')
    print('I will show you all duplicates now:')
    pictures.calculateAndPrintDuplicates()
    if moveDuplicates == 'true':
        print('you have chosen to move the duplicate pictures. They will be available in the folder \'dublicatesFromPyPictureProgram\'')
        pictures.moveDuplicatePicturesTo(os.path.join(path, 'dublicatesFromPyPictureProgram'))
    
    end()

pictures.collectGeoInformation()
pictures.saveDF(os.path.join(path, 'files.csv'))

if addGeoTag != 'false':
    print('add geo tag to pictures from within other pictures from the same day')

    if addGeoTag == 'dry':
        print('only run dry, so no actual changes!')
        print('=====================================')
        pictures.addGeoTagToPhotos(True)
    else:
        pictures.addGeoTagToPhotos(False)
        pictures.collect()
        pictures.collectGeoInformation()
        pictures.saveDF(os.path.join(path, 'files.csv'))

print('')
print('I will show you some geotag statistics:')
pictures.printGeoCodeStatistic()
end()




