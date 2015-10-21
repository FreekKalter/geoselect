geoselect
=========

A script to select photos from a set, based on geographical location.
Either via a decimal latitude/longitude point. Or a photo taken in the
desired location, it will look for exif standerized gps lat- and
longitude tags.

Installing
----------

Pip
~~~

The easiest way is to use pip to download and install the script.

::

    pip install geoselect

Get (latest) source
~~~~~~~~~~~~~~~~~~~

::

    # clone this repo
    clone https://github.com/FreekKalter/geoselect.git
    cd geoselect

    # initialize virtual environment (optional, but recommended)
    virtualenv venv
    source venv/bin/activate

    # install (--editable to hack on code whithout running pip install again)
    pip install --editable .

Using
-----

There are 2 ways to specify the location to select on. LOCATION can be a
"latitude,longitude" specified in decimal degrees like: "41.40338,
2.17403". Or it can be a path to a photo with exif gps coordinates, it
will then search for photos taken at the same location. It will search
within a specified radius (default: 1 km).

If ``--path`` is set, geoselect will look at that location for images
with common file extensions (jpg, jpeg, gif, bmp, png). This can be set
to something else with the ``--extensions`` parameter. If ``--path`` is
not set, paths to pictures are taken from stdinput. This way it can be
used as a stream filter, like most unix/linux commandline utils. For
example take the following pipeline:
``find /home/fkalter/photos -name '*holiday*' | geoselect --radius 10 "40.783068, -73.965350" | wc -l``
To count the number of pictures taken in/around central park wich have
'holiday' in the filename.

A (expiremental) feature uses the time a picture is taken to *gues* at
wich location it is made. Sometimes the device used to make the picture
takes a while to get a 'gps fix'. So it might not register the gps
coordinates for the first picture in a series. The ``-- time-based``
option looks for any pictures taken in a short time before or after a
picture with the specified location is taken. Because it is very likely
pictures taken very shortly after each ohter are taken at roughly the
same location.

::

    usage: geoselect.py [-h] [--path PATH] [--extentions EXTENTIONS] [--copy-to COPYTO] [--time-based] [--radius RADIUS]
                        [-V]
                        location

    A script to select photos from a set, based on geographical location. Either via a decimal latitude/longitude point.
    Or a photo taken in the desired location, it will look for exif standerized gps lat- and longitude tags.

    positional arguments:
      location              location given in decimal degrees like: "40.783068, -73.965350", or a path to a photo with
                            exif gps info

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH           path to look for image files, if not set files will be taken from stdin
      --extentions EXTENTIONS
                            comma separated list of extension to look for in PATH
      --copy-to COPYTO      path where found photos should be copied
      --time-based          also add photos wich themselfs dont have gps information, but are taken in a short time
                            before or after one that has (in the right location)
      --radius RADIUS       radius of area (in kilometers) to select photos from
      -V, --version         show program's version number and exit

