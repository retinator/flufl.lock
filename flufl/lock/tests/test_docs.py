# Copyright (C) 2004-2010 Barry A. Warsaw
#
# This file is part of flufl.lock.
#
# flufl.lock is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# flufl.lock is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.lock.  If not, see <http://www.gnu.org/licenses/>.

"""Test harness for doctests."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'additional_tests',
    ]


import os
import errno
import atexit
import doctest
import logging
import tempfile
import unittest

# pylint: disable-msg=F0401
from pkg_resources import (
    resource_filename, resource_exists, resource_listdir, cleanup_resources)


COMMASPACE = ', '
DOT = '.'
DOCTEST_FLAGS = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_NDIFF)



def stop():
    """Call into pdb.set_trace()"""
    # Do the import here so that you get the wacky special hacked pdb instead
    # of Python's normal pdb.
    import pdb
    pdb.set_trace()



def make_temporary_lockfile(testobj):
    """Make a temporary lock file for the tests."""
    def lockfile_creator():
        fd, testobj._lockfile = tempfile.mkstemp()
        os.close(fd)
        os.remove(testobj._lockfile)
        return testobj._lockfile
    return lockfile_creator


def setup(testobj):
    """Test setup."""
    # Initialize logging.
    logging.basicConfig()
    # Make sure future statements in our doctests match the Python code.  When
    # run with 2to3, the future import gets removed and these names are not
    # defined.
    try:
        testobj.globs['absolute_import'] = absolute_import
        testobj.globs['unicode_literals'] = unicode_literals
        testobj.globs['temporary_lockfile'] = make_temporary_lockfile(testobj)
    except NameError:
        pass
    testobj.globs['stop'] = stop


def teardown(testobj):
    """Test teardown."""
    try:
        os.remove(testobj._lockfile)
    except OSError as error:
        if error.errno != errno.ENOENT:
            raise
    except AttributeError:
        # lockfile_creator() was never called.
        pass



def additional_tests():
    "Run the doc tests (README.txt and docs/*, if any exist)"
    doctest_files = [
        os.path.abspath(resource_filename('flufl.lock', 'README.txt'))]
    if resource_exists('flufl.lock', 'docs'):
        for name in resource_listdir('flufl.lock', 'docs'):
            if name.endswith('.txt'):
                doctest_files.append(
                    os.path.abspath(
                        resource_filename('flufl.lock', 'docs/%s' % name)))
    kwargs = dict(module_relative=False,
                  optionflags=DOCTEST_FLAGS,
                  setUp=setup, tearDown=teardown,
                  )
    atexit.register(cleanup_resources)
    return unittest.TestSuite((
        doctest.DocFileSuite(*doctest_files, **kwargs)))
