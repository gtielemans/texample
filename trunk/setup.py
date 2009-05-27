from distutils.core import setup

setup(name='texamplenet',
      version='1.0dev',
      package_dir={'texample':'texample/','':'apps'},
      packages=[
        'texample','texgallery','texarticles','texblog','texpub',\
        'texpubutils','ganalytics','pkgbuilds','pkgresources',\
        ],
      )
