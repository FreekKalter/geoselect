# geoselect

A script to select photos from a set, based on geographical location. Either via a decimal latitude/longitude point.
Or a photo taken in the same location based on the files exif-gps tags.

## Installing

    # clone this repo
    clone https://github.com/FreekKalter/geoselect.git
    cd geoselect
    # install requirements
    pip install -r

## Using

By default geogrouping will search in the current directory for the following file extensions: jpg, jpeg, gif, bmp, png. And print the filenames to standard output.
LOCATION can be a "latitude,longitude" specified in decimal degrees like: "41.40338, 2.17403". Or it can be a photo with exif gps coordinates, wich will find photos
taken at the same location. Within a specifie radius (default: 1 km).

Another feature uses the time a picture is taken to "gues" at wich location it is taken. Sometimes the device used to take a picture takes a while to get a 'gps fix'.
So it might not register the gps coordinates for the first picture. The ```-- time-based```option looks for any pictures taken in a short time before or after a picture with
the specified location is taken.

```
geogrouping.py [options] LOCATION

--extentions=jpg,jpeg       a comma separated list of extension to search for
--location=path             path to search for files
--time_based                add photos without gps metadata if they are likely to be taken at the specified
                            location based on time
--copy                      copy found files to specified location
--radius                    default 1, in wich area around the specified location to look for photos

```
