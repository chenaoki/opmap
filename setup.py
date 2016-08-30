"""setup.py
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
    name = 'opmap',
    version = '0.0.1',
    description = 'Analysis package for optical mapping data',
    long_description=long_description,
    url='localhost',
    author='Naoki Tomii',
    author_email='chenaoki@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['contrib','docs','tests'])
)

