#from distutils.core import setup

from setuptools import setup, find_packages

setup(name='texamplenet',
      version='1.0dev',
      #package_dir={'texample':'texample/','':'apps'},
      packages=find_packages(),#[
      #  'texample','texgallery','texarticles','texblog','texpub',\
      #  'texpubutils','ganalytics','pkgbuilds','pkgresources',\
      #  ],
      )
