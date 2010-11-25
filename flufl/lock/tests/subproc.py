# Copyright (C) 2004-2010 by Barry A. Warsaw
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

"""A helper for setting up subprocess locks."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'acquire',
    ]


import time
import multiprocessing

from flufl.lock import Lock


def child_locker(filename, lifetime, queue):
    # First, acquire the file lock.
    with Lock(filename, lifetime):
        # Now inform the parent that we've acquired the lock.
        queue.put(True)
        # Keep the file lock for a while.
        time.sleep(lifetime.seconds - 1)


def acquire(filename, lifetime=None):
    """Acquire the named lock file in a subprocess."""
    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=child_locker,
                                   args=(filename, lifetime, queue))
    proc.start()
    while not queue.get():
        time.sleep(0.1)
