#!/home/fkalter/anaconda/bin/python2.7
from __future__ import print_function
import subprocess
import sys

out = subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
if 'README.md' in out:
    print('calling pandoc')
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
