
# add API credentials here
export HERE_APP_ID=
export HERE_APP_CODE=

docker build -t pictureprogram . && 
docker run \
-v $(pwd)/../_pictures:/app/testPictures \
-v $(pwd)/geoCacheDb:/app/geoCacheDb \
--env "HERE_APP_ID="$HERE_APP_ID \
--env "HERE_APP_CODE="$HERE_APP_CODE \
--env "path=./testPictures" \
--env "printDuplicates=true" \
--env "printGeoCodeStatistic=true" \
--env "moveDuplicates=false" \
--env "addGeoTag=false" \
-it pictureprogram
