# Background and motivation
I was in the situation of having a lot of pictures alrady taken before I switched uploading all new pictures into the cloud. At this time, I had a kind of arbitrary directory structure to organize all my pictures.  
This brought me to the idea to create a program, to 
* move duplicate pictures based on their hash (unfortunately not yet checking the picture content. By doing this it would be also possible to move out duplicates with another quality. E.g. if a picture was scaled down)
* show the location in textual form of where a picture was taken by using the [HERE API](https://developer.here.com/) (reverse geocoding)
* enrich pictures with a geo tag of another picture (which was taken at the same day and has a geotag)

So the program is devided into two parts. Once to move out duplicates and the other one to enrich geo tags to pictures based on other pictures of the same day.
After scanning all pictures in each of the steps, a files.csv file is created. It will contains of all pictures scanned for performance reason or more analytic work you want to do ;)

# Quickstart
This program can run in a docker container. So you need to have a docker installed on your system!!  
There is a script `dockerCommand.sh` and you enter the path to your picture directory there. The section you need to change looks like:  
```
# your path to your pictures. This will be mounted into the docker runtime environment 
path=/enter/your/path/to/your/pictures/here
#
```

As soon you're starting the program by using the script `dockerCommand.sh` the container will be build and run. After successfully start it will ask you some questions you want to do. Following options are available:

* Do you want to print all duplicates? [no]:
* Do you want to move all duplicate pictures to another folder? [no]:
* Do you want to display some geo statistics about your pictures? [yes]:
* Do you want to add geo data to pictures? [no]

# Technical informations
The program is written in python and uses a bunch of 3th party libs. It's running inside a `python` docker container with `buster` as simple tag. For more information visit: https://hub.docker.com/_/python. At this timne it was python 3.8.2.


In order to display an overview of your GEO tagged pictures, you need to set the HERE API credentials in the file `hereApiCredentials.sh`. This must be located in the same directoy as the script `dockerCommand.sh`.  
An example of `./hereApiCredentials.sh`:  
```
HERE_APP_ID=SFK434J1k2K3L4J5JBASDF
HERE_APP_CODE=SKJAK123KJKASD3
```

# Good to know
* By using the script, there is a geo cache in the same directory called `geoCacheDb/geolocations.db`. Every API call to the HERE API will be saved here, so in a second run of the script, it will be much more faster to process all pictures.
