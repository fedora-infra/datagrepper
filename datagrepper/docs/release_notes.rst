=============
Release Notes
=============

.. towncrier release notes start

v1.0.0
======

Released on 2022-01-17.
This is a major release that rebases on datanommer's port to TimescaleDB.

Backwards Incompatible Changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Drop the ``grouped`` argument feature, as fedora-messaging does not support
  it (:issue:`264`).

Development Improvements
^^^^^^^^^^^^^^^^^^^^^^^^

* Drop the dependency on fedmsg (:issue:`264`).


Thanks to all contributors who made this release possible!
