
# add your API credentials in file ./hereApiCredentials.sh with format
#
# HERE_APP_ID=<insert your app id>
# HERE_APP_CODE=<insert your app code>
#
HERE_APP_ID=tbd
HERE_APP_CODE=tbd
. ./hereApiCredentials.sh

docker build -t pictureprogram . && 
docker run \
-v $(pwd)/../pictures/:/app/picturesToProcess \
-v $(pwd)/geoCacheDb:/app/geoCacheDb \
--env "HERE_APP_ID="$HERE_APP_ID \
--env "HERE_APP_CODE="$HERE_APP_CODE \
--env "path=./picturesToProcess" \
--env "printDuplicates=false" \
--env "moveDuplicates=false" \
--env "addGeoTag=false" \
-it pictureprogram
cd ..
