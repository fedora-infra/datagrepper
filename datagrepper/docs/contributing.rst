============
Contributing
============

Thanks for considering contributing to datagrepper, we really appreciate it!

Quickstart:

1. Look for an `existing issue
   <https://github.com/fedora-infra/datagrepper/issues>`_ about the bug or
   feature you're interested in. If you can't find an existing issue, create a
   `new one <https://github.com/fedora-infra/datagrepper/issues/new>`_.

2. Fork the `repository on GitHub
   <https://github.com/fedora-infra/datagrepper>`_.

3. Fix the bug or add the feature, and then write one or more tests which show
   the bug is fixed or the feature works.

4. Submit a pull request and wait for a maintainer to review it.

More detailed guidelines to help ensure your submission goes smoothly are
below.

.. note:: If you do not wish to use GitHub, please send patches to
          infrastructure@lists.fedoraproject.org.

Development Environment
=======================
Vagrant allows contributors to get quickly up and running with a datagrepper development environment by
automatically configuring a virtual machine. This virtual machine also includes a running datanommer
service to make it easy to test your changes. To get started, first install the Vagrant and Virtualization
packages needed, and start the libvirt service::

    $ sudo dnf install ansible libvirt vagrant-libvirt vagrant-sshfs vagrant-hostmanager
    $ sudo systemctl enable libvirtd
    $ sudo systemctl start libvirtd

Check out the code and run ``vagrant up``::

    $ git clone https://github.com/fedora-infra/datagrepper
    $ cd datagrepper
    $ vagrant up

Next, SSH into your newly provisioned development environment::

    $ vagrant ssh

where you can run the following commands::

    $ datagrepper-start
    $ datagrepper-logs
    $ datagrepper-restart
    $ datagrepper-stop

to interact with the datagrepper service. Or::

    $ datanommer-consumer-start
    $ datanommer-consumer-logs
    $ datanommer-consumer-restart
    $ datanommer-consumer-stop

to interact with the datanommer consumer.

The datagrepper web application should be running automatically. To access it,
go to http://datagrepper.test:5000/ in the browser on your host machine to see the web application.

Note that the ``/vagrant/`` folder contains the source of the git checkout on your host. Any changes
to the files in that directory on the host will be automatically synced to the VM.


Guidelines
==========

Python Support
--------------
Datagrepper supports Python 3.7 or greater. This is automatically enforced by the
continuous integration (CI) suite.


Code Style
----------
We follow the `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ style guide
for Python. This is automatically enforced by the CI suite.

We are using `Black <https://github.com/ambv/black>` to automatically format
the source code. It is also checked in CI. The Black webpage contains
instructions to configure your editor to run it on the files you edit.


Tests
-----
The test suites can be run using `tox <http://tox.readthedocs.io/>`_ by simply
running ``tox`` from the repository root. All code must have test coverage or
be explicitly marked as not covered using the ``# pragma: no cover`` comment. This should
only be done if there is a good reason to not write tests.

Your pull request should contain tests for your new feature or bug fix. If
you're not certain how to write tests, we will be happy to help you.


Release Notes
-------------

To add entries to the release notes, create a file in the ``news`` directory in the
``source.type`` name format, where the ``source`` part of the filename is:

* ``42`` when the change is described in issue ``42``
* ``PR42`` when the change has been implemented in pull request ``42``, and
  there is no associated issue
* ``Cabcdef`` when the change has been implemented in changeset ``abcdef``, and
  there is no associated issue or pull request.

And where the extension ``type`` is one of:

* ``bic``: for backwards incompatible changes
* ``dependency``: for dependency changes
* ``feature``: for new features
* ``bug``: for bug fixes
* ``dev``: for development improvements
* ``docs``: for documentation improvements
* ``other``: for other changes

The content of the file will end up in the release notes. It should not end with a ``.``
(full stop).

If it is not present already, add a file in the ``news`` directory named ``username.author``
where ``username`` is the first part of your commit's email address, and containing the name
you want to be credited as. There is a script to generate a list of authors that we run
before releasing, but creating the file manually allows you to set a custom name.

A preview of the release notes can be generated with
``towncrier build --draft``.


Licensing
---------

Your commit messages must include a Signed-off-by tag with your name and e-mail
address, indicating that you agree to the `Developer Certificate of Origin
<https://developercertificate.org/>`_ version 1.1::

	Developer Certificate of Origin
	Version 1.1

	Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
	1 Letterman Drive
	Suite D4700
	San Francisco, CA, 94129

	Everyone is permitted to copy and distribute verbatim copies of this
	license document, but changing it is not allowed.


	Developer's Certificate of Origin 1.1

	By making a contribution to this project, I certify that:

	(a) The contribution was created in whole or in part by me and I
	    have the right to submit it under the open source license
	    indicated in the file; or

	(b) The contribution is based upon previous work that, to the best
	    of my knowledge, is covered under an appropriate open source
	    license and I have the right under that license to submit that
	    work with modifications, whether created in whole or in part
	    by me, under the same open source license (unless I am
	    permitted to submit under a different license), as indicated
	    in the file; or

	(c) The contribution was provided directly to me by some other
	    person who certified (a), (b) or (c) and I have not modified
	    it.

	(d) I understand and agree that this project and the contribution
	    are public and that a record of the contribution (including all
	    personal information I submit with it, including my sign-off) is
	    maintained indefinitely and may be redistributed consistent with
	    this project or the open source license(s) involved.

Use ``git commit -s`` to add the Signed-off-by tag.


Releasing
---------

When cutting a new release, follow these steps:

#. Update the version in ``pyproject.toml``
#. Run ``poetry install`` to update the version in the metadata
#. Add missing authors to the release notes fragments by changing to the ``news`` directory and
   running the ``get-authors.py`` script, but check for duplicates and errors
#. Generate the release notes by running ``poetry run towncrier`` (in the base directory)
#. Adjust the release notes in ``docs/release_notes.rst``.
#. Generate the docs with ``tox -e docs`` and check them in ``docs/_build/html``.
#. Commit the changes
#. Push the commit to the upstream Github repository (via a PR or not).
#. Change to the stable branch and cherry-pick the commit (or merge if appropriate)
#. Run the checks one last time to be sure: ``tox``,
#. Tag the commit with ``-s`` to generate a signed tag
#. Push the commit to the upstream Github repository with ``git push``,
   and the new tag with ``git push --tags``
#. Generate a tarball and push to PyPI with the command ``poetry publish --build``
#. Create `the release on GitHub <https://github.com/fedora-infra/datagrepper/tags>`_ and copy the
   release notes in there,
#. Deploy and announce.


