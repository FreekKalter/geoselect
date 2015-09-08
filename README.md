TODO: i wrote the documentation first, script is still very specific to my usecase
TODO: better name, on second thought geogrouping does not realy describe what it does at this point
# Geo grouping

A script to select photos from a set based on location.

## Getting geogrouping

    # clone this repo
    clone https://github.com/FreekKalter/geogrouping.git
    cd geogrouping
    # install requirements
    pip install -r

## Running

By default geogrouping will search in the current directory for the following file extensions: jpg, jpeg, gif, bmp, png. And then print the filenames to standard out. LOCATION can be a lat/long specified in decimal degrees like: "41.40338, 2.17403". Or it can be a photo with exif gps coordinates, it will find pictures taken in the
same place. The default radius is 2 kilometers.

```
geogrouping.py [options] LOCATION

--extentions=jpg,jpeg       a comma separated list of extension to search for
--location=path             path to search for files
--time_based                add photos without gps metadata if they are likely to be taken at the specified
                            location based on time
--copy                      copy found files to specified location
--radius                    default 2, in wich area around the specified location to look for photos

```
