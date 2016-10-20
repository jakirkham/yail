#!/usr/bin/env python

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Oct 20, 2016 11:43$"


import doctest
import sys
import unittest

from yail import core


# Load doctests from `types`.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(core))
    return tests


if __name__ == '__main__':
    sys.exit(unittest.main())
