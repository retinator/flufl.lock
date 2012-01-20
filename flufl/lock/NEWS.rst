===================
NEWS for flufl.lock
===================

2.2 (2012-01-19)
================
 * Support Python 3 without the use of 2to3.
 * Make the documentation clear that the `flufl.test.subproc` functions are
   not part of the public API.  (LP: #838338)
 * Fix claim file format in `take_possession()`.  (LP: #872096)
 * Provide a new API for dealing with possible additional unexpected errnos
   while trying to read the lock file.  These can happen in some NFS
   environments.  If you want to retry the read, set the lock file's
   `retry_errnos` property to a sequence of errnos.  If one of those errnos
   occurs, the read is unconditionally (and infinitely) retried.
   `retry_errnos` is a property which must be set to a sequence; it has a
   getter and a deleter too.  (LP: #882261)

2.1.1 (2011-08-20)
==================
 * Fixed TypeError in .lock() method due to race condition in _releasetime
   property.  Found by Stephen A. Goss. (LP: #827052)

2.1 (2010-12-22)
================
 * Added lock.details.

2.0.2 (2010-12-19)
==================
 * Small adjustment to doctest.

2.0.1 (2010-11-27)
==================
 * Add missing exception to __all__.

2.0 (2010-11-26)
================
 * Package renamed to flufl.lock.


Earlier
=======

Try `bzr log` for details.
