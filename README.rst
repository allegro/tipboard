========
Tipboard
========

|docs|

Introduction
------------

Tipboard is a system for creating dashboards, written in JavaScript and Python.
Its widgets ('tiles' in Tipboard's terminology) are completely separated from
data sources, which provides great flexibility and relatively high degree of
possible customizations.

Because of its intended target (displaying various data and statistics in your
office), it is optimized for larger screens.

Similar projects: `Geckoboard <http://www.geckoboard.com/>`_,
`Dashing <http://shopify.github.io/dashing/>`_.

A detailed, technical documentation for Tipboard can be found
`here <http://tipboard.readthedocs.org/en/latest/>`_.


Quick start
-----------

Requirements
~~~~~~~~~~~~

Assuming Ubuntu or similar Linux distribution, some required packages need
to be installed first::

  $ sudo apt-get install python-dev python-virtualenv redis-server

Virtual environment
~~~~~~~~~~~~~~~~~~~

Continue by creating a virtual environment that will help you conveniently
separate your instance from what you already have installed in the system
(let's say we will name it "tb-env")::

  $ virtualenv tb-env

Activate the created virtual environment with the following command::

  $ source tb-env/bin/activate

Installation with pip
~~~~~~~~~~~~~~~~~~~~~

After creating and activating virtualenv, install the latest (current) version
of Tipboard package available on `pypi <https://pypi.python.org/pypi>`_
("Python Package Index") with the following command::

  (tb-env)$ pip install tipboard

Next, you need to create a configuration template for your dashboard - let's
say we will call it 'my_test_dashboard'::

  (tb-env)$ tipboard create_project my_test_dashboard

This command will create ``.tipboard`` directory in your home dir and will
fill it with default settings for your dashboard.

Verification
~~~~~~~~~~~~

To verify your installation, launch this command::

  (tb-env)$ tipboard runserver

If you see the message ``Listening on port...`` instead of any errors, it means
that installation was successful and you may now
`configure <http://tipboard.readthedocs.org/en/latest/configuration.html>`_
your newly installed Tipboard instance. You may also point your favorite
web browser to ``http://localhost:7272`` to see the current state of your
dashboard.


License
-------

Tipboard is licensed under the `Apache License, v2.0 <http://tipboard.readthedocs.org/en/latest/license.html>`_.

Copyright (c) 2013-2017 `Allegro Group <http://allegrogroup.com>`_.

.. |docs| image:: https://readthedocs.org/projects/tipboard/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/tipboard/
