NFS-safe file locking with timeouts for POSIX systems

..
    This file is part of flufl.lock.

    flufl.lock is free software: you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License.

    flufl.lock is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with flufl.lock.  If not, see <http://www.gnu.org/licenses/>.


==========
flufl.lock
==========

The ``flufl.lock`` library provides an NFS-safe file-based locking algorithm
influenced by the GNU/Linux `open(2)` manpage, under the description of the
`O_EXCL` option::

        [...] O_EXCL is broken on NFS file systems, programs which rely on it
        for performing locking tasks will contain a race condition.  The
        solution for performing atomic file locking using a lockfile is to
        create a unique file on the same fs (e.g., incorporating hostname and
        pid), use link(2) to make a link to the lockfile.  If link() returns
        0, the lock is successful.  Otherwise, use stat(2) on the unique file
        to check if its link count has increased to 2, in which case the lock
        is also successful.

The assumption made here is that there will be no *outside interference*,
e.g. no agent external to this code will ever ``link()`` to the specific lock
files used.

Lock objects support lock-breaking so that you can't wedge a process forever.
This is especially helpful in a web environment, but may not be appropriate
for all applications.

Locks have a *lifetime*, which is the maximum length of time the process
expects to retain the lock.  It is important to pick a good number here
because other processes will not break an existing lock until the expected
lifetime has expired.  Too long and other processes will hang; too short and
you'll end up trampling on existing process locks -- and possibly corrupting
data.  In a distributed (NFS) environment, you also need to make sure that
your clocks are properly synchronized.


Requirements
============

``flufl.lock`` requires Python 2.6 or newer.  It is compatible with Python 3.2.


Project details
===============

You may download the latest version of the package from the Python
`Cheese Shop`_ or from Launchpad_.

You can also install it via ``easy_install`` or ``pip``.

    % sudo easy_install flufl.lock
    % sudo pip install flufl.lock

See the Launchpad project page for access to the Bazaar branch, bug report,
etc.


.. _`Cheese Shop`: http://pypi.python.org/flufl.lock
.. _Launchpad: https://launchpad.net/flufl.lock
