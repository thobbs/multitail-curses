multitail-curses
================
A curses-based utility script for tailing multiple files simultaneously.

I made this script for quickly tailing several log files in the same terminal
window.

.. image:: https://raw.github.com/thobbs/multitail-curses/master/screenshot.png

Installation
------------
The easiest way to install this is through pip or easy_install::

    pip install -U multitail-curses

You can also install from source by running::

    python setup.py install

Usage
-----
You can tail one to four files simultaneously.  For example::

    multitail foo.log bar.log

Press ``CTRL-C`` to stop tailing.

License
-------
This project is open source under the `MIT license <http://www.opensource.org/licenses/mit-license.php>`_.
