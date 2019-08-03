========
Tipboard
========

|docker modebuild| |docker build|  |docker stars|  |docs|

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


Execution by python
~~~~~~~~~~~~~~~~~~~

Install requirements
  $ sudo apt-get install python-dev python-virtualenv redis-server

Install with python dependencies on virtual env::

  $ virtualenv tb-env                       # create virtual env
  $ source tb-env/bin/activate              # activate virtual env
  $ (tb-env)$ install -r requirements.txt   # install python lib
  $ (tb-env)$ tipboard create_project my_test_dashboard
  $ (tb-env)$ python manage.py runserver    # start webserver

Install with python dependencies on system::

  $ pip install -r requirements.txt
  $ python manage.py runserver

Execution by docker
~~~~~~~~~~~~~~~~~~~

It's a non-root bitnami python3.7 image, contening a redis-server and the tipboard application

From docker hub::

  $ docker pull themaux/tipboard
  $ docker run -p 8080:8080 themaux/tipboard

From local source::

  $ docker build -t tipboard:local .
  $ docker run -p 8080:8080 tipboard:local

If you want to externalise the redis-server you want to::

    - In Dockerfile, comment line 3 `RUN apt-get update && apt-get install redis-server -y`
    - In entrypoint.sh, comment line 2 `nohup redis-server &`
    - Change the value *REDIS_HOST* & *REDIS_PASSWORD* in the tipboard/Config/properties.json

Execution on openshift
~~~~~~~~~~~~~~~~~~~~~~

I need to finish the helm template first and the exemple /!\

to deploy with oc::

    rm -Rvf manifests/*
    helm dependency update
    helm template --values ./values/op.yaml --name tipboard  --output-dir ./manifests .


Verification
~~~~~~~~~~~~

Go to  your favorite web browser to ``http://0.0.0.0:8080`` to see the current state of your
dashboard.

License
-------

Tipboard is licensed under the `Apache License, v2.0 <http://tipboard.readthedocs.org/en/latest/license.html>`_.

Copyright (c) 2013-2017 `Allegro Group <http://allegrogroup.com>`_.

.. |docs| image:: https://readthedocs.org/projects/tipboard/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/tipboard/

.. |docker stars| image:: https://img.shields.io/docker/stars/themaux/tipboard
    :alt: Docker stars
    :scale: 100%
    :target: https://readthedocs.org/projects/tipboard/
    
.. |docker modebuild| image:: https://img.shields.io/docker/cloud/automated/themaux/tipboard
    :alt: Docker stars
    :scale: 100%
    :target: https://readthedocs.org/projects/tipboard/

.. |docker build| image:: https://img.shields.io/docker/cloud/build/themaux/tipboard.svg
    :alt: Docker stars
    :scale: 100%
    :target: https://readthedocs.org/projects/tipboard/

<img src="http://91.121.142.202/piwik/matomo.php?idsite=1&amp;rec=1" style="border:0" alt="" />
