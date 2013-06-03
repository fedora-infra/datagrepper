General API notes
-----------------

All API calls (currently) permit GET and POST requests with the same arguments.

A trailing slash is optional on all API endpoints. There is no difference
between using one and not using one.

Responses are always served as ``application/json`` (unless ``JSONP`` is
explicitly requested, in which case datagrepper returns the appropriate
``application/javascript``).


/raw
----

The ``/raw`` endpoint provides limited query support, but is "instant" and does
not require your query to be put into a job queue.

Response format
===============

Sample response:

.. code-block:: javascript

    {
      "arguments": {
        "page": 1,
        "rows_per_page": 20,
        ...
      },
      "count": 1,
      "pages": 42,
      "raw_messages": [
        {
          "certificate": "...",
          "i": 1,
          "msg": {
            ...
          },
          "signature": "...",
          "timestamp": 1361414385.0,
          "topic": "org.fedoraproject.prod.sample"
        },
        ...
      ],
      "total": 851
    }

The ``arguments`` item in the root dictionary contains all possible arguments,
and displays the value used (the default if the argument was not provided).

Time arguments
==============

Below is a table describing what timeframe messages are received from
depending on what combination of time options you provide.

========= ========= ======= =================
``delta`` ``start`` ``end`` Message timeframe
========= ========= ======= =================
no        no        no      last ``rows_per_page`` items
**yes**   no        no      last ``delta`` seconds
no        **yes**   no      from ``start`` until now
**yes**   **yes**   no      from ``start`` until ``delta`` seconds from ``start``
no        no        **yes** the 600 seconds before ``end``
**yes**   no        **yes** the ``delta`` seconds before ``end``
no        **yes**   **yes** between ``start`` and ``end``
**yes**   **yes**   **yes** between ``start`` and ``end`` (``delta`` is ignored)
========= ========= ======= =================


``delta``
  Return results from the last ``delta`` seconds.

  Default: None

``start``
  Return results starting at time ``start`` (in `UNIX time
  <https://en.wikipedia.org/wiki/Unix_time>`_).

  Default: None or (``end`` minus ``delta``)

``end``
  Return results ending at time ``end`` (in `UNIX time
  <https://en.wikipedia.org/wiki/Unix_time>`_).

  Default: None or current

Filter arguments
================

``user``
  FAS user to query for.

  This argument can be provided multiple times; returns messages referring to
  any listed user.

  Default: all users

``package``
  Fedora package to query for.

  This argument can be provided multiple times; returns messages referring to
  any listed package.

  Default: all packages

``category``
  Category to query for.

  In fedmsg, a *category* is what service emitted the message, e.g. ``git``,
  ``bodhi``, or ``wiki``. The category is usually the third or fourth part of
  the topic.

  This argument can be provided multiple times; returns messages referring to
  any listed package.

  Default: all categories

``topic``
  Topic to query for.

  In fedmsg, a *topic* is a full reverse-domain description of the type of
  message, such as ``org.fedoraproject.prod.git.receive``.

  This argument can be provided multiple times; returns messages referring to
  any listed package.

  Default: all topics

Pagination arguments
====================

``page``
  Which page to return. Must be greater than 0.

  Default: 1

``rows_per_page``
  The number of messages to return for each page. Must be less than or equal to
  100.

  Default: 20

``order``
  The "order" in which messages should be returned.  Must be one of either
  "asc" or "desc".  "asc" means ascending, i.e. from oldest to newest.
  "desc" means descending, i.e. from newest to oldest.

  Default: "asc"

Formatting arguments
====================

``callback``
  To be specified when querying datagrepper via JavaScript/ajax, it will
  return a "jsonp" output with the MIME type 'application/javascript'
  instead of the traditionnal "json".

  Default: None

``meta``
  Argument to specify what meta information to return with the raw
  message from fedmsg.
  Options are: `title, subtitle, icon, secondary_icon, link, usernames,
  packages, objects`

  Default: None


/submit
-------

The ``/submit`` endpoint allows you to submit a job for a data query more
complex than what ``/raw`` can provide.

The status of a job (including a URL where you can download the data, if the
job is complete) is available from the ``/status`` endpoint.

Arguments inherited from /raw
=============================

The following arguments can be used in the same way as in ``/raw``:

- ``delta``
- ``start``
- ``end``
- ``meta``
- ``user``
- ``package``
- ``category``
- ``topic``

Advanced filter arguments
=========================

Advanced filter arguments allow you to filter based on values inside the
message body. Each argument consists of a key, an operator, and a value.

The key references a key in the message. A path of keys can be specified by
joining each part of the path with ``->``. A single part of the path may be a
single asterisk (``*``) to allow for any key in that part.

There are various operators. In the following table, *value* is the value in
the job request and *message value* is the value in the message for the key.

======== =================================================================================
Operator Conditions to return message
======== =================================================================================
``==``   *message value* is equal to *value*
``!=``   *message value* is not equal to *value*
``<``    *message value* is less than *value*
``<=``   *message value* is less than or equal to *value*
``>``    *message value* is greater than *value*
``>=``   *message value* is greater than or equal to *value*
``=~``   *message value* is a string and the regular expression *value* is found in *message value*
``!~``   *message value* is a string and the regular expression *value* is not found in *message value*
``=*``   - if *message value* is a string, *value* is a substring of *message value*;
         - if *message value* is a list, *value* is an item in *message value*;
         - if *message value* is a dictionary, *value* is a key in *message value*
``!*``   - if *message value* is a string, *value* is not a substring of *message value*;
         - if *message value* is a list, *value* is not an item in *message value*;
         - if *message value* is a dictionary, *value* is not a key in *message value*
======== =================================================================================


Advanced filter arguments are added to the query string by the following
mechanism::

    arg = urlencode( urlencode(key) + operator + urlencode(value) )

Response format
===============

Successful response:

.. code-block:: javascript

    {
        "args": {
            ...
        },
        "job_id": 1,
        "options": {
            "category": [ ],
            "delta": null,
            ...
        }
    }

Error response:

.. code-block:: javascript

    {
        "error": "error_type",
        ...
    }

Errors
======

``invalid_arg``
  An advanced filter argument couldn't be parsed.

  ``value`` is the value of the argument

``unicode_decode``
  A ``UnicodeDecodeError`` occurred when trying to parse the argument.

  ``value``, ``reason``, ``start``, and ``end`` are from the raised exception.

Implementation notes
====================

For the ``=*`` and ``!*`` operators, we simply use Python's ``in`` operator.


/status
-------

Returns the status of a job. If the job is finished, also returns the filename.

Response format
===============

.. code-block:: javascript

    {
        "id": 1,
        "state": "done",
        "url": "http://..."
    }

Valid states include ``free``, ``open``, ``done``, ``failed``, and ``deleted``.
``url`` is displayed for the ``done`` state only.
