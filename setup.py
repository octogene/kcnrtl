#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='KCnrtl',
      version='0.4b',
      description='Qt graphical client for the CNRTL french linguistic resources',
      license = "GPLv3", 
      author="Bogdan Cordier",
      author_email="bcord@hadaly.fr",
      url="http://code.lm7.fr/p/kcnrtl/",
      download_url="http://code.lm7.fr/p/kcnrtl/downloads/", 
      packages=['kcnrtl'],
      requires=['BeautifulSoup4','httplib2'],
      long_description=read('README'),
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Console",
        "Topic :: Utilities",
        "Natural Language :: French",
        "Intended Audience :: Education"
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
     )
