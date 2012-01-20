===================
NEWS for flufl.lock
===================

2.2 (2012-01-19)
================
 * Support Python 3 without the use of 2to3.
 * Make the documentation clear that the `flufl.test.subproc` functions are
   not part of the public API.  (LP: #838338)

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
