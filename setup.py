from setuptools import setup


setup(
    name='geoselect',
    version='0.1',
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
    license='GPL v3',
    keywords='gps photos filter',
    url='https://github.com/FreekKalter/geoselect',
)
