#!/usr/bin/env python

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Oct 20, 2016 11:43$"


import doctest
import itertools
import sys
import types
import unittest

from yail import core

from yail.core import (
    generator,
    empty,
    cycles,
    duplicate,
    pad,
)


# Load doctests from `types`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(core))
    return tests


class TestYail(unittest.TestCase):
    def setUp(self):
        pass


    def test_generator(self):
        assert list(generator(range(5))) == [0, 1, 2, 3, 4]

        assert isinstance(generator(range(5)), types.GeneratorType)
        assert issubclass(type(generator(range(5))), types.GeneratorType)
        assert type(generator(range(5))) is types.GeneratorType


    def test_empty(self):
        assert list(empty()) == []

        with self.assertRaises(StopIteration):
            next(empty())


    def test_cycles(self):
        assert list(cycles([], 5)) == []

        assert list(cycles([1], 5)) == list(itertools.repeat(1, 5))

        assert list(cycles([1, 2, 3])) == [1, 2, 3]
        assert list(cycles([1, 2, 3], 2)) == [1, 2, 3, 1, 2, 3]
        assert list(cycles([1, 2, 3], 3)) == [1, 2, 3, 1, 2, 3, 1, 2, 3]

        assert list(zip(range(9), cycles([1, 2, 3], None))) == [(0, 1),
                                                                (1, 2),
                                                                (2, 3),
                                                                (3, 1),
                                                                (4, 2),
                                                                (5, 3),
                                                                (6, 1),
                                                                (7, 2),
                                                                (8, 3)]


    def test_duplicate(self):
        assert list(duplicate([], 5)) == []

        assert list(duplicate([1], 5)) == list(itertools.repeat(1, 5))

        assert list(duplicate([1, 2, 3])) == [1, 2, 3]
        assert list(duplicate([1, 2, 3], 2)) == [1, 1, 2, 2, 3, 3]
        assert list(duplicate([1, 2, 3], 3)) == [1, 1, 1, 2, 2, 2, 3, 3, 3]


    def test_pad(self):
        assert list(pad([1,2,3])) == [1, 2, 3]
        assert list(pad([1,2,3], before=1)) == [None, 1, 2, 3]
        assert list(pad([1,2,3], after=2)) == [1, 2, 3, None, None]
        assert list(pad([1,2,3], before=1, after=2, fill=0)) == [0, 1, 2, 3,
                                                                 0, 0]
        assert list(zip(range(3), pad([1,2,3], before=None))) == [(0, None),
                                                                  (1, None),
                                                                  (2, None)]
        assert list(zip(range(6), pad([1,2,3], after=None))) == [(0, 1),
                                                                 (1, 2),
                                                                 (2, 3),
                                                                 (3, None),
                                                                 (4, None),
                                                                 (5, None)]

        padded = pad([1,2,3], before=None, after=None)
        assert list(zip(range(3), padded)) == [(0, None),
                                               (1, None),
                                               (2, None)]


    def tearDown(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
