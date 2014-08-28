.. _installation:

==============
How to install
==============

You can install Tipboard on a variety of sensible operating systems. This guide
assumes **Ubuntu Server 12.04 LTS** and presents shell command examples
accordingly.

Prerequisites
-------------

Tipboard requires Python 2.7 which can be installed with this command::

  $ sudo apt-get install python-dev python-virtualenv

Another dependency which needs to be satisfied  before proceeding further is
`Redis <http://redis.io/>`_ server::

  $ sudo apt-get install redis-server

Optional yet recommended packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of such packages is ``supervisor`` - it facilitates program administration
(e.g. its reboot), especially if there are a few instances launched on the
machine.

Based on the Tornado framework, Tipboard has a built-in server available, but
a typical use case assumes communication with the world via reverse proxy (e.g.
using ``nginx`` or ``apache``).

.. note::

   Although configuration of reverse proxy is out of scope of this manual, we
   would like to emphasise that Tipboard use Web Sockets – a relatively new
   mechanism – and thus you should ensure a server in a version that will
   support it (e.g. ``nginx`` >= 1.3.13 or ``apache2`` >= 2.4.6). By default
   Ubuntu 12.04 offers older versions – you may then use backports.

.. note::

   It will be useful to have an updated version of ``pip`` (i.e. >= 1.4) and
   ``virtualenv`` (i.e. >= 1.10).

Preparing environment for installation
--------------------------------------

Start by creating a user, the privileges of whom will be used by the
application (for the needs of this manual, let's create the user "pylabs")::

  $ sudo adduser pylabs --home /home/pylabs --shell /bin/bash
  $ sudo su - pylabs

Virtual environment
~~~~~~~~~~~~~~~~~~~

Continue by creating a virtual environment that will help you conveniently
separate your instance from what you already have installed in the system
(let's say we name it "tb-env")::

  $ cd /home/pylabs
  $ virtualenv tb-env

Activate the created virtual environment with the following command::

  $ source /home/pylabs/tb-env/bin/activate

.. note::

   It is worth saving the above line in the ``~/.profile`` file. As a result,
   the virtual environment will be activated automatically whenever you log in
   on the machine.

.. note::

   Further setup assumes an activated virtual environment, which is denoted by
   ``(tb-env)`` prefix in your shell prompt.

Installing with pip
-------------------

After creating and activating virtualenv, install the latest (current) version
of Tipboard package available on pypi ("Python Package Index") with the
following command::

  (tb-env)$ pip install tipboard

Verification
------------

To verify if installation has been successful, launch this command::

  (tb-env)$ tipboard runserver

If you see the message "Listening on port..." instead of errors, it means that
installation was successful and you may proceed to the next section.
