datagrepper
===========

A webapp to retrieve historical information about messages on the `fedmsg
<http://fedmsg.com>`_ bus.  It is a JSON api for the `datanommer
<https://github.com/fedora-infra/datanommer/>`_ message store.

Production Instance
-------------------

https://apps.fedoraproject.org/datagrepper/

Hacking on datagrepper
----------------------

Prerequisites
~~~~~~~~~~~~~
    * virtualenvwrapper
    * Postgresql

Install postgresql and virtualenvwrapper::

   $ sudo yum install -y postgresql-server python-virtualenvwrapper

Setting up the stack
~~~~~~~~~~~~~~~~~~~~

Use a virtualenv::

    $ mkvirtualenv datagrepper
    $ workon datagrepper

Install dependencies::

    $ pip install -r requirements.txt
    $ pip install psycopg2

Configuring Postgresql (and getting some data)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In normal operations, the `datanommer
<https://github.com/fedora-infra/datanommer>`_ consumer daemon will be
running somewhere and continuously stuff each new `fedmsg
<http://fedmsg.com>`_ message that it sees into a postgres DB.  If you're
just sitting down to hack on datagrepper, that won't be your situation
so you'll need a dump of the database.

.. note:: If you've tried installing postgres before and think you've
   messed it up, you'll need to blow away the old databases with
   ``$ rm -rf /var/lib/pgsql``

Install postgres (and fedmsg, while we're at it)::

    $ sudo yum install -y postgresql-server fedmsg
    $ sudo postgresql-setup initdb

Make sure postgres is set to allow connections over tcp/ip using password
authentication.  Edit the ``/var/lib/pgsql/data/pg_hba.conf``.  You might
find a line like this::

    host    all             all             127.0.0.1/32            ident

Instead of that line, you need one that looks like this::

    host    all             all             127.0.0.1/32            md5

----

Become yourself again (not the ``postgres`` user) and start up postgres::

    $ sudo systemctl restart postgresql.service

Become the postgres user (again) and run the psql command.  Use that psql
shell to setup the DB, the user, and privileges::

    $ sudo su - postgres
    $ psql
    # create database datanommer;
    # create user datanommer with password 'bunbunbun';
    # grant all privileges on database datanommer to datanommer;
    # \q

Back in the bash shell (but still as the `postgres` user), grab a DB dump and
restore it::

    $ wget http://infrastructure.fedoraproject.org/infra/db-dumps/datanommer.dump.xz
    $ xzcat datanommer.dump.xz | psql datanommer

Last step, run datagrepper
~~~~~~~~~~~~~~~~~~~~~~~~~~

You have to configure your development datagrepper instance to talk to
postgres (by default, it looks for a sqlite database).  Edit
``fedmsg.d/example-datagrepper.py`` and give it these contents:

.. code-block:: python

    config = {
        'datanommer.enabled': False,
        'datanommer.sqlalchemy.url': 'postgresql+psycopg2://datanommer:bunbunbun@localhost:5432/datanommer',
        'fedmsg.consumers.datagrepper-runner.enabled': True,
    }

As your normal old user self, run the development server::

    $ workon datagrepper
    $ python runserver.py

In a browser, visit http://localhost:5000 to see the docs.

You can quick test that you can get data by running::

    $ sudo yum install -y httpie
    $ http get localhost:5000/raw delta==1000000 rows_per_page==1
