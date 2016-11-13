# Copyright (C) 2004-2015 Barry A. Warsaw
#
# This file is part of flufl.lock.
#
# flufl.lock is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# flufl.lock is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.lock.  If not, see <http://www.gnu.org/licenses/>.

"""Testing other aspects of the implementation and API."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    ]


import os
import datetime
import errno
import tempfile
import time
import unittest

try:
    # Python 3
    import builtins
except ImportError:
    # Python 2
    import __builtin__ as builtins


import flufl.lock._lockfile
from flufl.lock._lockfile import Lock, NotLockedError, TimeOutError


class TestableEnvironmentError(EnvironmentError):
    def __init__(self, errno):
        super(TestableEnvironmentError, self).__init__()
        self.errno = errno

EMOCKEDFAILURE = 99
EOTHERMOCKEDFAILURE = 98


class ErrnoRetryTests(unittest.TestCase):
    def setUp(self):
        self._builtin_open = builtins.open
        self._failure_countdown = None
        self._retry_count = None
        self._errno = EMOCKEDFAILURE
        fd, self._lockfile = tempfile.mkstemp('.lck')
        os.close(fd)
        self._lock = Lock(self._lockfile)

    def tearDown(self):
        self._disable()
        try:
            self._lock.unlock()
        except NotLockedError:
            pass
        try:
            os.remove(self._lockfile)
        except OSError as error:
            if error.errno != errno.ENOENT:
                raise

    def _enable(self):
        builtins.open = self._testable_open
        self._failure_countdown = 3
        self._retry_count = 0

    def _disable(self):
        builtins.open = self._builtin_open

    def _testable_open(self, *args, **kws):
        if self._failure_countdown <= 0:
            return self._builtin_open(*args, **kws)
        self._failure_countdown -= 1
        self._retry_count += 1
        raise TestableEnvironmentError(self._errno)

    def test_retry_errno_api(self):
        self.assertEqual(self._lock.retry_errnos, [])
        self._lock.retry_errnos = [EMOCKEDFAILURE, EOTHERMOCKEDFAILURE]
        self.assertEqual(self._lock.retry_errnos,
                         [EMOCKEDFAILURE, EOTHERMOCKEDFAILURE])
        del self._lock.retry_errnos
        self.assertEqual(self._lock.retry_errnos, [])

    def test_retries(self):
        # Test that _read() will retry when a given errno is encountered.
        self._lock.lock()
        self._lock.retry_errnos = [self._errno]
        self._enable()
        self.assertTrue(self._lock.is_locked)
        # The _read() trigged by the .is_locked call should have been retried.
        self.assertEqual(self._retry_count, 3)


class LifetimeTests(unittest.TestCase):
    def setUp(self):
        self._saved_CLOCK_SLOP = flufl.lock._lockfile.CLOCK_SLOP
        flufl.lock._lockfile.CLOCK_SLOP = datetime.timedelta(seconds=0)
        fd, self._lockfile = tempfile.mkstemp('.lck')
        os.close(fd)
        self._lifetime = datetime.timedelta(seconds=1)
        self._lock1 = Lock(self._lockfile, lifetime=self._lifetime)
        self._lock2 = Lock(self._lockfile, lifetime=self._lifetime)

    def tearDown(self):
        flufl.lock._lockfile.CLOCK_SLOP = self._saved_CLOCK_SLOP
        try:
            self._lock1.unlock()
        except NotLockedError:
            pass
        try:
            self._lock2.unlock()
        except NotLockedError:
            pass
        try:
            os.remove(self._lockfile)
        except OSError as error:
            if error.errno != errno.ENOENT:
                raise

    def test_no_break(self):
        self._lock1.lock()
        with self.assertRaises(TimeOutError):
            self._lock2.lock(timeout=datetime.timedelta(seconds=0))

    def test_break(self):
        self._lock1.lock()
        time.sleep(self._lifetime.seconds)
        self._lock2.lock(timeout=datetime.timedelta(seconds=0))
        self.assertTrue(self._lock2.is_locked)
        self.assertFalse(self._lock1.is_locked)
