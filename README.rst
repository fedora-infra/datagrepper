datagrepper
-----------

A webapp to retrieve historical information about messages on the `fedmsg
<http://fedmsg.com>`_ bus.  It is a JSON api for the `datanommer
<https://github.com/fedora-infra/datanommer/>`_ message store.

Production Instance
-------------------

datagrepper is still in development and does not currently have a production
URL.  When it *does* have one, we'll be sure to link to it here.

Hacking on datagrepper
----------------------

Use a virtualenv::

    $ mkvirtualenv datagrepper
    $ workon datagrepper

Install dependencies::

    $ pip install -r requirements.txt

Run the development server::

    $ python runserver.py
