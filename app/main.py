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

path = os.environ.get('path')
correctPath = input('Is this path to your pictures correct: {} [yes]: '.format(path))
if (correctPath == ''):
    correctPath = 'yes'
if (correctPath != 'no' and correctPath != '' and correctPath != 'yes'):
    print('unsupported charakter, please retry')
    end()

if (correctPath != 'yes'):
    print('Please update the path in the file dockerCommand.sh and restart the program')
    end()

printDuplicates = input('Do you want to print all duplicates? [no]: ')
if (printDuplicates == ''):
    printDuplicates = 'no'
if (printDuplicates != 'no' and printDuplicates != '' and printDuplicates != 'yes'):
    print('unsupported charakter, please retry')
    end()

moveDuplicates = input('Do you want to move all duplicate pictures to another folder? [no]: ')
if (moveDuplicates == ''):
    moveDuplicates = 'no'
if (moveDuplicates != 'no' and moveDuplicates != '' and moveDuplicates != 'yes'):
    print('unsupported charakter, please retry')
    end()

if printDuplicates == 'no' and moveDuplicates == 'no':
    showGeoStatistics = input('Do you want to display some geo statistics about your pictures? [yes]: ')
    if (showGeoStatistics == ''):
        showGeoStatistics = 'yes'
    if (showGeoStatistics != 'no' and showGeoStatistics != '' and showGeoStatistics != 'yes'):
        print('unsupported charakter, please retry')
        end()

    addGeoTag = input('Do you want to add geo data to pictures? [no]: ')
    if (addGeoTag == ''):
        addGeoTag = 'no'
    if (addGeoTag != 'no' and addGeoTag != '' and addGeoTag != 'yes'):
        print('unsupported charakter, please retry')
        end()

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

if printDuplicates == 'yes' or moveDuplicates == 'yes':
    print('')
    print('I will show you all duplicates now:')
    pictures.calculateAndPrintDuplicates()
    if moveDuplicates == 'yes':
        print('you have chosen to move the duplicate pictures. They will be available in the folder \'dublicatesFromPyPictureProgram\'')
        pictures.moveDuplicatePicturesTo(os.path.join(path, 'dublicatesFromPyPictureProgram'))
    end()

if showGeoStatistics == 'yes' or addGeoTag == 'yes':
    if not pictures.alreadyReadGeoTags():
        pictures.collectGeoInformation()
        pictures.saveDF(os.path.join(path, 'files.csv'))

if addGeoTag == 'yes':
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
if showGeoStatistics == 'yes':
    pictures.printGeoCodeStatistic()

end()




