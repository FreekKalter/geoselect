from __future__ import print_function
from math import radians, cos, sin, asin, sqrt
from path import Path
from dateutil import parser as timeparser
import time
import exifread
import re
import sys
import argparse


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Thanks to a answer on stackoverflow by Michael Dunn.
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


def get_time(filename, tags):
    # use exif 'Image DateTime' field as the time

    # very fuzzy time machting on filename

    # if above all fails use stat().mt_time (consistent on windows/linux as last modification time)
    pass


def convert_to_decimal(string):
    """
    Decode the exif-gps format into a decimal point.
    '[51, 4, 1234/34]'  ->  51.074948366
    """
    h, m, s = re.sub('\[|\]', '', string).split(', ')
    result = int(h)
    if '/' in m:
        m = m.split('/')
        result += int(m[0]) * 1.0 / int(m[1]) / 60
    else:
        result += int(m) * 1.0 / 60
    if '/' in s:
        s = s.split('/')
        result += int(s[0]) * 1.0 / int(s[1]) / 3600
    else:
        result += int(s) * 1.0 / 60
    return result


def build_dict(path, extensions):
    """
    Scan path for jpg files, and get their exif tags. Build a dict like:
    {'absolute_filename': {'EXIF field': 'exif tag value'}}
    Parse DateTime from filename in the same loop, added as 'TIME'.
    """
    p = Path(path)
    files_with_tags = dict()
    for f in p.files('*.jpg'):
        with open(str(f.abspath()), 'rb') as jpg:
            tags = exifread.process_file(jpg)
            del tags['JPEGThumbnail']
            time_str = re.sub('([a-zA-Z]+)|(-\d+)$', '', f.name.stripext())
            time_str = re.sub('\.', ':', time_str)
            time = timeparser.parse(time_str)
            tags['TIME'] = time
            files_with_tags[str(f.abspath())] = tags
    return files_with_tags


def location_filter(files_with_tags, location, distance):
    '''
    Get photos taken whitin the specified radius from a fixed point.
    '''
    on_location = dict()
    for f, tags in files_with_tags.items():
        if 'GPS GPSLatitude' in tags:
            lat = convert_to_decimal(str(tags['GPS GPSLatitude']))
            long = convert_to_decimal(str(tags['GPS GPSLongitude']))
            if haversine(lat, long, location['lat'], location['long']) < distance:
                on_location[f] = tags
    return on_location


def add_based_on_time(files_with_tags, on_location):
    '''
    Sometimes the first photo in a series does not have gps coordinates yet because the phone
    doesnt have a gps-fix yet. To add these photos as well take the list of photos wich where
    taken in the right location. Then add any photos taken whitin 10 minutes of these photos,
    because they are almost certainly taken in the same area.
    '''
    to_add = dict()
    for veiling_f, veiling_tags in on_location.items():
        for compare_f, compare_tags in files_with_tags.items():
            delta = abs(veiling_tags['TIME'] - compare_tags['TIME'])
            if (delta.total_seconds() < 10 * 60) and (compare_f not in on_location.keys()):
                to_add[compare_f] = compare_tags
    return to_add


def main():
    veilingstr = {'lat': 51.972904, 'long': 5.919421}
    argparser = argparse.ArgumentParser(description='select images bases on location')
    argparser.add_argument('location', type=str, default='',
                           help='location given in decimal degrees like: "40.783068, -73.965350",\
                                  or a photo with exif gps tags')
    argparser.add_argument('--path', type=str, default='.', help='path to look for image files')
    argparser.add_argument('--extentions', type=str, default='jpg,png,jpeg,tiff',
                           help='comma separated list of extension to look for in PATH')
    argparser.add_argument('--copy-to', dest='copyto', type=str, default='',
                           help='path where found photos should be copied')
    argparser.add_argument('--time-based', dest='time_based', action='store_true',
                           help='also add photos wich themselfs dont have gps information, but are taken\
                                 in a short time before or after one that has (in the right location)')
    args = argparser.parse_args()
    args.location = args.location.strip()
    m = re.match('(\d+(\.\d+)?)\s*,\s*(\d+(\.\d+)?)', args.location)
    location = dict()
    if m:
        location['lat'], location['long'] = float(m.group(1)), float(m.group(3))
    else:
        p = Path(args.location)
        if not p.exists():
            print('Photo given to extract location from: "' + p.abspath() + '" does not exist')
            sys.exit(1)
        with open(str(p.abspath()), 'rb') as f:
            tags = exifread.process_file(f)
            if 'GPS GPSLongitude' not in tags.keys() or 'GPS GPSLatitude' not in tags.keys():
                print('Photo does not contain gps information')
                sys.exit(1)
            location['lat'] = convert_to_decimal(str(tags['GPS GPSLatitude']))
            location['long'] = convert_to_decimal(str(tags['GPS GPSLongitude']))
    if not location:
        print('Invalid location given')
        argparser.print_help()
        sys.exit(1)
    if not Path(args.path).exists():
        print(args.path + ' does not exist')
        sys.exit(1)
    if args.copyto != '' and not Path(args.copyto).exists():
        print(args.copyto + ' does not exist')
        sys.exit(1)
    extensions = map(lambda x: x.strip(), args.extentions.split(','))
    files_with_tags = build_dict(args.path, extensions)
    on_location = location_filter(files_with_tags, veilingstr, 1)
    if args.time_based:
        on_location.update(add_based_on_time(files_with_tags, on_location))

    for f, tags in on_location.items():
        print(f)
        if args.copyto != '':
            Path(f).copy2(args.copyto)


def main2():
    p = Path('/media/truecrypt3/Dropbox/Camera Uploads/')
    for f in p.files('*.jpg'):
        with open(str(f.abspath()), 'rb') as jpg:
            tags = exifread.process_file(jpg)
            if 'Image DateTime' not in tags.keys():
                filename = re.sub('([a-zA-Z]+)|(-\d+)$', '', f.name.stripext())
                modified = time.strftime('%Y-%m-%d %H.%M.%S', time.localtime(f.stat().st_mtime))
                if filename != modified:
                    print(filename + '\n', modified)


if __name__ == '__main__':
    main()
