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

"""This is an old stress test that needs to be updated."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    ]


import os
import sys
import time
import errno
import random
import datetime

from flufl.lock import Lock, NotLockedError, TimeOutError



# Unit test framework
def _dochild():
    prefix = '[%d]' % os.getpid()
    # Create somewhere between 1 and 1000 locks
    lockfile = Lock('/tmp/LockTest', lifetime=datetime.timedelta(seconds=120))
    # Use a lock lifetime of between 1 and 15 seconds.  Under normal
    # situations, Mailman's usage patterns (untested) shouldn't be much longer
    # than this.
    workinterval = 5 * random.random()
    hitwait = 20 * random.random()
    print prefix, 'workinterval:', workinterval
    is_locked = False
    t0 = 0
    t1 = 0
    t2 = 0
    try:
        try:
            t0 = time.time()
            print prefix, 'acquiring...'
            lockfile.lock()
            print prefix, 'acquired...'
            is_locked = True
        except TimeOutError:
            print prefix, 'timed out'
        else:
            t1 = time.time()
            print prefix, 'acquisition time:', t1-t0, 'seconds'
            time.sleep(workinterval)
    finally:
        if is_locked:
            try:
                lockfile.unlock()
                t2 = time.time()
                print prefix, 'lock hold time:', t2-t1, 'seconds'
            except NotLockedError:
                print prefix, 'lock was broken'
    # wait for next web hit
    print prefix, 'webhit sleep:', hitwait
    time.sleep(hitwait)


def _seed():
    try:
        fp = open('/dev/random')
        d = fp.read(40)
        fp.close()
    except EnvironmentError as error:
        if error.errno != errno.ENOENT:
            raise
        import sha
        d = sha.new(`os.getpid()`+`time.time()`).hexdigest()
    random.seed(d)


def _onetest():
    loopcount = random.randint(1, 100)
    for i in range(loopcount):
        print 'Loop %d of %d' % (i+1, loopcount)
        pid = os.fork()
        if pid:
            # parent, wait for child to exit
            pid, status = os.waitpid(pid, 0)
        else:
            # child
            _seed()
            try:
                _dochild()
            except KeyboardInterrupt:
                pass
            os._exit(0)


def _reap(kids):
    if not kids:
        return
    pid, status = os.waitpid(-1, os.WNOHANG)
    if pid != 0:
        del kids[pid]


def _test(numtests):
    kids = {}
    for i in range(numtests):
        pid = os.fork()
        if pid:
            # parent
            kids[pid] = pid
        else:
            # child
            _seed()
            try:
                _onetest()
            except KeyboardInterrupt:
                pass
            os._exit(0)
        # slightly randomize each kid's seed
    while kids:
        _reap(kids)


if __name__ == '__main__':
    _test(int(sys.argv[1]))
