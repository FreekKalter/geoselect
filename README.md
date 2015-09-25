# geoselect

A script to select photos from a set, based on geographical location. Either via a decimal latitude/longitude point.
Or a photo taken in the desired location, it will look for exif standerized gps lat- and longitude tags.

## Installing

    # clone this repo
    clone https://github.com/FreekKalter/geoselect.git
    cd geoselect

    # initialize virtual environment (optional)
    virtualenv venv
    source venv/bin/activate

    # install requirements
    pip install -r requirements.txt


*TODO: use pip to install*
## Using

By default geoselect will search in the current directory for the following file extensions: jpg, jpeg, gif, bmp, png. It will print the filenames to standard output.
LOCATION can be a "latitude,longitude" specified in decimal degrees like: "41.40338, 2.17403". Or it can be a path to a photo with exif gps coordinates, it will then search for photos taken at the same location.
Within a specifie radius (default: 1 km).

A (expiremental) feature uses the time a picture is taken to "gues" at wich location it is made. Sometimes the device used to make the picture takes a while to get a 'gps fix'.
So it might not register the gps coordinates for the first picture in a series. The ```-- time-based```option looks for any pictures taken in a short time before or after a picture with the specified location is taken. Because it is very likely pictures taken very shortly after each ohter are taken at roughly the same location.

```
usage: geoselect.py [-h] [--path PATH] [--extentions EXTENTIONS] [--copy-to COPYTO] [--time-based] location

select images bases on location

positional arguments:
  location              location given in decimal degrees like: "40.783068, -73.965350", or a photo with exif gps
                        tags

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           path to look for image files
  --extentions EXTENTIONS
                        comma separated list of extension to look for in PATH
  --copy-to COPYTO      path where found photos should be copied
  --time-based          also add photos wich themselfs dont have gps information, but are taken in a short time
                        before or after one that has (in the right location)
```
