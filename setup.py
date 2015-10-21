from setuptools import setup
import os


def long_description():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'README.rst'), 'r') as readme:
        return readme.read()

setup(
    name='geoselect',
    version='0.2.2',
    py_modules=['geoselect'],
    install_requires=[
        'ExifRead>2.0,<3.0',
        'path.py>8.0,<9.0',
        'wheel==0.24.0',
    ],
    entry_points='''
        [console_scripts]
        geoselect=geoselect:main
    ''',


    author='Freek Kalter',
    author_email='freek@kalteronline.org',
    description='A script to select photos from a set, based on geographical location.',
    long_description=long_description(),
    license='GPL v3',
    keywords='gps photos filter',
    url='https://github.com/FreekKalter/geoselect',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Multimedia',
    ],
)
