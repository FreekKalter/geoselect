from __future__ import print_function
from math import radians, cos, sin, asin, sqrt
from path import Path
from dateutil import parser
import exifread
import re


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
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


def build_dict(path):
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
            time = parser.parse(time_str)
            tags['TIME'] = time
            files_with_tags[str(f.abspath())] = tags
    return files_with_tags


def filter_veilingstr(files_with_tags, distance):
    '''
    Get photos taken whitin the specified radius from a fixed point.
    '''
    veilingstr = {'lat': 51.972904, 'long': 5.919421}
    aan_veilingstr = dict()
    for f, tags in files_with_tags.items():
        if 'GPS GPSLatitude' in tags:
            lat = convert_to_decimal(str(tags['GPS GPSLatitude']))
            long = convert_to_decimal(str(tags['GPS GPSLongitude']))
            if haversine(lat, long, veilingstr['lat'], veilingstr['long']) < distance:
                aan_veilingstr[f] = tags
                # Path(f).copy2('/media/truecrypt3/Dropbox/Camera Uploads/Elst/')
    return aan_veilingstr


def add_based_on_time(files_with_tags, aan_veilingstr):
    '''
    Sometimes the first photo in a series does not have gps coordinates yet because the phone
    doesnt have a gps-fix yet. To add these photos as well take the list of photos wich where
    taken in the right location. Then add any photos taken whitin 10 minutes of these photos,
    because they are almost certainly taken in the same area.
    '''
    to_add = dict()
    for veiling_f, veiling_tags in aan_veilingstr.items():
        for compare_f, compare_tags in files_with_tags.items():
            delta = abs(veiling_tags['TIME'] - compare_tags['TIME'])
            if (delta.total_seconds() < 10 * 60) and (compare_f not in aan_veilingstr.keys()) and\
                    ('Image Model' in compare_tags and str(compare_tags['Image Model']) == 'iPhone 5'):
                to_add[compare_f] = compare_tags
    return to_add


def main():
    files_with_tags = build_dict('/media/truecrypt3/Dropbox/Camera Uploads/')
    aan_veilingstr = filter_veilingstr(files_with_tags, 1)
    to_add = add_based_on_time(files_with_tags, aan_veilingstr)
    print(len(to_add))
    for f in to_add:
        Path(f).copy2('/home/fkalter/Elst/')


if __name__ == '__main__':
    main()
