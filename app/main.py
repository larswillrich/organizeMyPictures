from order import Pictures
import os
from pathlib import Path

def isCSVFilePresent(path):
    csvFile = Path(os.path.join(path, 'files.csv'))
    if csvFile.is_file():
        return True
    return False

if os.environ.get('moveDuplicates') is not None:
    moveDuplicates = os.environ['moveDuplicates']
else:
    moveDuplicates = 'false'

path = '/app/testPictures'
readFromCSV = isCSVFilePresent(path)

print('Welcome to my picture Program. More then happy to have you here!')

pictures = Pictures(path)
if readFromCSV:
    print('Found files.csv file, so do not create a new csv file but use the existing one.')
    pictures.fromCSV(os.path.join(path, 'files.csv'))
else: 
    print('Did not find a files.csv, where may already some analysing data are already available. But seems not, so I will create one for you ...')
    pictures.collect()
    pictures.saveDF(os.path.join(path, 'files.csv'))

print('')
print('I will show you all duplicates now:')
pictures.calculateAndPrintDuplicates()

if moveDuplicates == 'true':
    print('you have chosen to move the duplicate pictures. They will be available in the folder \'dublicatesFromPyPictureProgram\'')
    pictures.moveDuplicatePicturesTo(os.path.join(path, 'dublicatesFromPyPictureProgram'))

print('good bye')


