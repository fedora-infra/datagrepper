.. |crarr| unicode:: U+021B5 .. DOWNWARDS ARROW WITH CORNER LEFTWARDS

Pre-requisites
--------------

As an alternative to cURL, HTTPie_ is a tool you can use to interact with a JSON
API, like datagrepper. All examples in this guide use HTTPie. Use this command
to install it on Fedora::

   sudo dnf install httpie


Requesting all messages in the last 2 days
------------------------------------------

datagrepper takes time arguments in `seconds`. So, we need to convert two days
to 172,800 seconds first. Then, we can use HTTPie_ to get the JSON payload::

   http get {{URL}}raw delta==172800


Paging results
--------------

The previous example is a large JSON response that's too big to read through.
Limit the number of results to make it more digestable::

   http get {{URL}}raw delta==172800 rows_per_page==1

.. code-block:: javascript

    {
        "arguments": {
            "delta": 1728000.0,
            "end": 1366221938.0,
            "page": 1,
            "rows_per_page": 1,
            "order": "desc",
            "start": 1364493938.0,
            "topics": [],
            "categories": [],
            "users": []
            "packages": [],
            "not_topics": [],
            "not_categories": [],
            "not_users": []
            "not_packages": [],
        },
        "count": 1,
        "pages": 2052,
        "raw_messages": [
            ...
        ],
        "total": 2052
    }

In this example, ``raw_messages`` was omitted for readability.

Notice a few things.

#. **``arguments`` dict**: Describes all parameters datagrepper uses to execute
   query
#. **Timestamps**: ``start`` and ``end`` included (derived from your ``delta``)
#. **Pagination**: ``rows_per_page`` shows the rows per page, its sibling value
   ``page`` is pointer to "page" of data you are on

Use this command to get to the next page::

   http get {{URL}}raw \
      delta==172800 \
      rows_per_page==1 \
      page==2

.. code-block:: javascript

    {
        "arguments": {
            "delta": 1728000.0,
            "end": 1366221938.0,
            "page": 2,
            "rows_per_page": 1,
            "order": "desc",
            "start": 1364493938.0,
            "topics": [],
            "categories": [],
            "users": []
            "packages": [],
            "not_topics": [],
            "not_categories": [],
            "not_users": []
            "not_packages": [],
        },
        "count": 1,
        "pages": 2052,
        "raw_messages": [
            ...
        ],
        "total": 2052
    }

The number of rows are retrieved from newest to oldest ("descending"). The
``order`` argument lets you specify that. The default is ``desc``, but you can
set it to ``asc`` for ascending order (i.e. oldest to newest).


Only Bodhi messages (OR wiki)
-----------------------------

There is a `list of topics`_ that come across Fedora's messaging bus
(**fedmsg**). Specify a ``category`` to limit your message to one kind of
topic::

   http get {{URL}}raw \
      delta==172800 \
      category==bodhi

Here, ``category`` is singular but comes back in the ``arguments`` dict as
*categories* (plural)! You can specify multiple categories and messages that
match *either* category will return. They are ``OR``'d together::

   http get {{URL}}raw \
      delta==172800 \
      category==bodhi \
      category==wiki

Messages for specific users and packages
----------------------------------------

Search for events relating to multiple users with this query::

   http get {{URL}}raw \
      delta==172800 \
      user==toshio \
      user==pingou

Same for packages::

   http get {{URL}}raw \
      delta==172800 \
      package==nethack


Excluding data
--------------

For each positive filter, there is a corresponding *negative filter*. If you
want to query all messages **except for Koji messages**, use this query::

   http get {{URL}}raw \
      delta==172800 \
      not_category==buildsys

Positive and negative filters are combinable. This query returns all messages
except for user ``toshio``'s *Ask Fedora* activity::

   http get {{URL}}raw \
      delta==172800 \
      user==toshio \
      not_category==askbot


Putting it all together (CNF)
-----------------------------

Multiple ``category``, ``user``, and ``package`` filters are merged together in
a way that looks like `Conjunctive Normal Form`_ (CNF).

The following query returns all messages from the past two days where
*(category==bodhi OR category==wiki) AND (user==toshio OR user==pingou)*::

   http get {{URL}}raw \
      delta==172800 \
      category==bodhi \
      category==wiki \
      user==toshio \
      user==pingou


Topics list
-----------

If you don't know what topics are available for you to query, check the `list
of topics`_ in the documentation.


Get help
--------

If you get stuck, join ``#fedora-apps`` on freenode_ to ask questions. Or, if
everything is awesome, we welcome high-fives and karma cookies.


.. _`HTTPie`: https://github.com/jkbr/httpie#httpie-a-cli-curl-like-tool-for-humans
.. _`list of topics`: http://fedora-fedmsg.readthedocs.io/en/latest/topics.html
.. _`Conjunctive Normal Form`: https://wikipedia.org/wiki/Conjunctive_normal_form
.. _`freenode`: https://fedoraproject.org/wiki/How_to_use_IRC

