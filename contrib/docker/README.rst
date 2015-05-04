===============
Tipboard Docker
===============


Development
-----------

Build Docker base image::

    $ docker build --tag=tipboard-base base

Build tipboard Docker dev image::

    $ cd dev
    $ docker-compose build

Create sample project::

    $ docker-compose run --no-deps tipboard /opt/tipboard/bin/tipboard create_project dev

Add Redis host config to settings::

    $ echo "REDIS_HOST = 'redis'" >> .tipboard/settings-local.py

Run services::

    $ docker-compose up


Production (open-source)
------------------------

Build production tipboard Docker images (by developers)::

    $ docker build --tag=tipboard-base base
    $ docker build --tag=tipboard prod


Usage with docker-compose
~~~~~~~~~~~~~~~~~~~~~~~~~

Create sample project::

    $ cd prod
    $ docker-compose run --no-deps tipboard /opt/tipboard/bin/tipboard create_project sample

Add redis host config to settings::

    $ echo "REDIS_HOST = 'redis'" >> .tipboard/settings-local.py

Run services::

    $ docker-compose up


Usage without docker-compose (recommended for simple tests)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create sample project::

    $ docker run --rm --volume=<CONFIG-DIRECTORY>:/root/.tipboard tipboard /opt/tipboard/bin/tipboard create_project sample

Run tipboard (with redis-server built-in)::

    $ docker run -d --name=tipboard -P -p 7272:7272 --volume=<CONFIG-DIRECTORY>:/root/.tipboard tipboard

Notice to replace `<CONFIG-DIRECTORY>` with directory in your host system where
tipboard's config files will be stored.
