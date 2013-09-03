.. |crarr| unicode:: U+021B5 .. DOWNWARDS ARROW WITH CORNER LEFTWARDS

Prerequisites
-------------

If you've never interacted with a JSON API before, you should check out
the handy command-line tool `HTTPie
<https://github.com/jkbr/httpie#httpie-a-cli-curl-like-tool-for-humans>`_.
All our examples here will use it.  To install it on Fedora run ``$ sudo
yum -y install httpie``.

If you get stuck here, feel free to drop into the ``#fedora-apps``
channel on `freenode <http://fedoraproject.org/wiki/How_to_use_IRC>`_ to
ask questions or even just to give us a high five if everything goes well.

Requesting all messages in the last 2 days
------------------------------------------

datagrepper takes all time arguments in `seconds`, so we'll need to
convert 2 days to 172800 seconds first.  Then we can use `HTTPie
<https://github.com/jkbr/httpie#httpie-a-cli-curl-like-tool-for-humans>`_
like this::

    $ http get {{URL}}raw/ delta==172800

Paging results
--------------

You're going to get a large JSON response that's too big to read
through.  Try limiting the number of results to make it more
digestable::

    $ http get {{URL}}raw/ \
        delta==172800 \
        rows_per_page==1

.. code-block:: javascript

    {
        "arguments": {
            "categories": [],
            "delta": 1728000.0,
            "end": 1366221938.0,
            "packages": [],
            "page": 1,
            "rows_per_page": 1,
            "order": "asc",
            "start": 1364493938.0,
            "topics": [],
            "users": []
        },
        "count": 1,
        "pages": 2052,
        "raw_messages": [
            ...
        ],
        "total": 2052
    }

In the above output, the contents of ``raw_messages`` has been omitted for
readability.  Notice a few things: first, the ``arguments`` dict describes
all the parameters that datagrepper used to execute your query.  The
``start`` and ``end`` timestamps are included (there were derived from
the ``delta`` that you supplied). 

Your ``rows_per_page`` is there.  It has a sibling value ``page`` which
is a pointer to which "page" of data you are on.  You could issue the
following query to get the next one::

    $ http get {{URL}}raw/ \
        delta==172800 \
        rows_per_page==1 \
        page==2

.. code-block:: javascript

    {
        "arguments": {
            "categories": [],
            "delta": 1728000.0,
            "end": 1366221938.0,
            "packages": [],
            "page": 2,
            "rows_per_page": 1,
            "order": "asc",
            "start": 1364493938.0,
            "topics": [],
            "users": []
        },
        "count": 1,
        "pages": 2052,
        "raw_messages": [
            ...
        ],
        "total": 2052
    }


By default, the order of rows retrieved is from oldest to newest ("ascending").
There is an ``order`` argument you can specify to set that how you like.  The
default is "asc", but you can set it to "desc" for descending order, a.k.a.
from newest to oldest.

Only Bodhi messages (OR wiki)
-----------------------------

There is a `long list <http://fedmsg.com/en/latest/topics/>`_ of types of
messages that come across the Fedora Infrastructure's message bus.
You can limit the scope of your query to only one kind of message
by specifying a ``category``::

    $ http get {{URL}}raw/ \
        delta==172800 \
        category==bodhi

Note that, in this example, ``category`` is singular but it comes back in
the ``arguments`` dict as *categories* (plural!)  You can specify more
than one category and messages that match *either* category will be returned.
They are **OR**'d together::

    $ http get {{URL}}raw/ \
        delta==172800 \
        category==bodhi \
        category==wiki

Messages for a particular users and packages
--------------------------------------------

Just like categories, you can search for events relating to one or multiple
users::

    $ http get {{URL}}raw/ \
        delta==172800 \
        user==toshio \
        user==pingou

Same goes for packages::

    $ http get {{URL}}raw/ \
        delta==172800 \
        package==nethack

Putting it all together (CNF)
-----------------------------

If you specify multiple ``category`` filters and multiple ``user`` filters
and multiple ``package`` filters, they are merged together in a way that looks
like `Conjunctive Normal Form (CNF)
<http://en.wikipedia.org/wiki/Conjunctive_normal_form>`_.

For example, this query will return all messages from the past 2 days where
*(category==bodhi OR category==wiki) AND (user==toshio OR user==pingou)*::

    $ http get {{URL}}raw/ \
        delta==172800 \
        category==bodhi \
        category==wiki \
        user==toshio \
        user==pingou

Topics list
-----------

If you don't know what topics are available for you to query, you can use the
``/topics`` endpoint with no arguments::

    $ http get {{URL}}topics/

Bulk queries
------------

The ``/submit`` endpoint does not limit you to the number of messages you can
fetch. You can submit a job, then listen to the fedmsg bus for a
``datagrepper.job.status.change`` message for when your job is done.

The arguments are the same as ``/raw``.

You can check on your job's status with the ``/status`` endpoint::

    $ http get {{URL}}status/ id==1
