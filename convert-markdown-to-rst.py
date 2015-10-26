#!/home/fkalter/anaconda/bin/python2.7
from __future__ import print_function
import subprocess
import sys
import re

files_changed = subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
# Convert Readme.md to readme.rst (for pypi documentation), run only when Readme.md has changed.
if 'README.md' in files_changed:
    try:
        subprocess.check_output(['pandoc', '--from=markdown', '--to=rst', '--out=README.rst', 'README.md'])
    except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit(1)
    try:
        subprocess.check_output(['git', 'add', 'README.rst'])
    except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit(1)
    else:
        print('pandoc run succesfully, README.rst added')

# Run python test suite before commiting *.py files
python_regex = re.compile('.*\.py$', re.IGNORECASE)
if [f for f in files_changed.split('\n') if python_regex.match(f)]:
    try:
        subprocess.check_output(['tox'])
    except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit(1)
    else:
        print('python tests succeeded')
