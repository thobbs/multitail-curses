import os
from setuptools import setup

import multitail

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "multitail-curses",
    version = multitail.__version__,
    author = "Tyler Hobbs",
    author_email = "tylerlhobbs@gmail.com",
    description = ("A curses-based utility script for tailing multiple "
                   "files simultaneously."),
    license = "MIT",
    keywords = "tail script multitail",
    url = "http://github.com/thobbs/multitail-curses",
    download_url = 'http://github.com/thobbs/multitail-curses/archive/%s.tar.gz' % (multitail.__version__,),
    packages=[],
    py_modules=['multitail'],
    scripts=['multitail'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],
)
