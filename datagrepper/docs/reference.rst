General API notes
-----------------

All API calls (currently) permit GET and POST requests with the same arguments.

A trailing slash is optional on all API endpoints. There is no difference
between using one and not using one.

JSON response format
--------------------

/raw
----

The ``/raw`` endpoint provides limited query support, but does not require your
query to be put into a job queue.

Time arguments
==============

Below is a table describing what timeframe messages are received from depending
on what combination of time options you provide.

========= ========= ======= =================
``delta`` ``start`` ``end`` Message timeframe
========= ========= ======= =================
no        no        no      last 600 seconds
**yes**   no        no      last ``delta`` seconds
no        **yes**   no      from ``start`` until now
**yes**   **yes**   no      from ``start`` until now (``delta`` is ignored)
no        no        **yes** the 600 seconds before ``end``
**yes**   no        **yes** the ``delta`` seconds before ``end``
no        **yes**   **yes** between ``start`` and ``end``
**yes**   **yes**   **yes** between ``start`` and ``end`` (``delta`` is ignored)
========= ========= ======= =================


``delta``
  Return results from the last ``delta`` seconds.

  Default: 600

``start``
  Return results starting at time ``start`` (in `UNIX time
  <https://en.wikipedia.org/wiki/Unix_time>`_).

  Default: (``end`` minus ``delta``)

``end``
  Return results ending at time ``end`` (in `UNIX time
  <https://en.wikipedia.org/wiki/Unix_time>`_).

  Default: current time

Filter arguments
================

``user``
  FAS user to query for.
  
  This argument can be provided multiple times; returns messages referring to
  any listed user.

``package``
  Fedora package to query for.
  
  This argument can be provided multiple times; returns messages referring to
  any listed package.

``category``
  Category to query for.

  In fedmsg, a *category* is what service emitted the message, e.g. ``git``,
  ``bodhi``, or ``wiki``. The category is usually the third or fourth part of
  the topic.
  
  This argument can be provided multiple times; returns messages referring to
  any listed package.

``topic``
  Topic to query for.

  In fedmsg, a *topic* is a full reverse-domain description of the type of
  message.
  
  This argument can be provided multiple times; returns messages referring to
  any listed package.
