General API notes
-----------------

All API calls (currently) permit GET and POST requests with the same arguments.

A trailing slash is optional on all API endpoints. There is no difference
between using one and not using one.

Responses can be served as ``application/json`` or ``text/html`` as per the accept header. If the request
is made in "text/html" then it will return the html content otherwise it will return the json content (unless ``JSONP`` is
explicitly requested, in which case datagrepper returns the appropriate ``application/javascript``).


/raw
----

The ``/raw`` endpoint returns lists of messages.

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
  any listed category.

  Default: all categories

``topic``
  Topic to query for.

  In fedmsg, a *topic* is a full reverse-domain description of the type of
  message, such as ``org.fedoraproject.prod.git.receive``.

  This argument can be provided multiple times; returns messages referring to
  any listed topic.

  Default: all topics

``contains``
  Keyword to search in the messages.

  Sometime one knows only a part of a message, this would allow retrieving
  all the messages containing that part.

  This argument can be provided multiple times; returns messages referring to
  any listed topic.

  Default: all messages

``not_user``
  FAS users to exempt from query.

  This argument can be provided multiple times; returns only messages that do
  not refer to any listed user.

  Default: no users

``not_package``
  Fedora package to exempt from query.

  This argument can be provided multiple times; returns only messages that do
  not refer to any listed package.

  Default: no packages

``not_category``
  Category to exempt from query.

  In fedmsg, a *category* is what service emitted the message, e.g. ``git``,
  ``bodhi``, or ``wiki``. The category is usually the third or fourth part of
  the topic.

  This argument can be provided multiple times; returns only messages that
  do not fall under the listed categories.

  Default: no categories

``not_topic``
  Topic to exempt from query.

  In fedmsg, a *topic* is a full reverse-domain description of the type of
  message, such as ``org.fedoraproject.prod.git.receive``.

  This argument can be provided multiple times; returns only messages that
  do are not marked with the listed topics.

  Default: no topics

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

  Default: "desc"

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
  Options are: ``title``, ``subtitle``, ``icon``, ``secondary_icon``, ``link``,
  ``usernames``, ``packages``, ``objects``, and ``date``.

  Default: None

``grouped``
  Argument to specify if the server should attempt to group together similar
  messages.  Must be one of either "true" or "false".

  Default: false

``chrome``
  "chrome" decides whether the messages should be displayed with html boiler-plate
  or not. Must be one of either "true" or "false". "true" means with boiler-plate and
  "false" implies without it.

  Default: true

``size``
  Argument need to be specified if you want to receive different kinds of message cards.
  Options are: small, medium, large, and extra-large.
  ``"small"`` contains link and title. ``"medium"`` contains link, title, icon
  and subtitle.  ``"large"`` contains link, title, icon, subtitle,
  secondary_icon and datetime.  ``"extra-large"`` contains those of "large",
  but it also displays the full JSON body of the raw message.

  Default: large

/id
---

Returns the message by the particular message-id given by the user.

Formatting arguments
====================

``chrome``
  Same as that of /raw

``size``
  Same as that of /raw

``is_raw``
  Checks whether the card is coming from /raw url or not. Must be one of either "true" or "false".
  If card is from /raw url then it will be "true" otherwise "false".

/topics
-------

Returns a list of all topics in the datanommer database. Takes no arguments.

This is cached hourly, and it often takes a while to generate.
