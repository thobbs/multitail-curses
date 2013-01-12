import unittest
from tempfile import TemporaryFile as temp

from nose.tools import assert_equal

import multitail

class TestSeeking(unittest.TestCase):

    def test_basic(self):
        with temp() as f:
            for i in range(10):
                f.write("%d\n" % i)

            for i in range(10):
                multitail._seek_to_n_lines_from_end(f, i)
                assert_equal(i, len(f.readlines()))

    def test_short_file(self):
        """ The file is shorter than the number of lines we request """
        with temp() as f:
            for i in range(3):
                f.write("%d\n" % i)

            multitail._seek_to_n_lines_from_end(f, 100)
            assert_equal(3, len(f.readlines()))

    def test_multiple_buffers(self):
        """ We need to buffer multiple times """
        with temp() as f:
            for i in range(10000):
                f.write("%d\n" % i)

            multitail._seek_to_n_lines_from_end(f, 5000)
            assert_equal(5000, len(f.readlines()))
