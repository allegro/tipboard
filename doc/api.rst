===
API
===

One of the advantages of Tipboard is flexibility in feeding tiles with data. We
achieve that by providing a simple, REST API - that way, your feeding scripts
may be written in any language (Python, Ruby, Bash, Perl, PHP - you name it).
The only limitation is the format of input data accepted by a given tile type
(see :ref:`tiles_library` for the details).

To experiment with resources specified below you can use tools like `Advanced
REST Client <http://chromerestclient.appspot.com/>`_ (Chrome extension), or
`cURL <http://curl.haxx.se/>`_, if you prefer working from command line. For
Python programmers, there's an excellent `Requests
<http://docs.python-requests.org/en/latest/>`_ library, which we strongly
recommend.

.. _api_key:

API key
-------

To send anything to your tiles, first you have to get your API key. This unique
key is generated for you automatically during Tipboard's installation and may
be read in the ``~/.tipboard/settings-local.py`` file - it is a sequence of
characters starting with ``API_KEY``, e.g.::

  API_KEY = 'e2c3275d0e1a4bc0da360dd225d74a43'

If you can't see any such string, just add the key manually (it doesn't have
to be as long and hard to memorise as the one above, though).

.. note::

   Every change in ``settings-local.py`` file requires restart of the
   application.

Available resources
-------------------

Current API version: **v0.1**

.. note::

   In 99% of cases, probably only ``push`` and ``tileconfig`` will be of
   interest to you.


.. http:post:: /api/(api_version)/(api_key)/push

   Feeds tiles with data. Input data should be provided in the format that
   complies with the one used in a desired tile. **Note:** a tile to which data
   will be sent is defined by the key included in the data sent rather than by
   `tile_id` as in cases below.

   :param api_version: version of API to be used
   :param api_key: your API key

   **Example request**:

   .. sourcecode:: http

      POST /api/v0.1/my_key/push
      Host: localhost:7272
      POST data: tile=text key=id_1 data={"text": "Hello world!"}

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/html; charset=UTF-8

      Tile's data pushed successfully.

.. http:post:: /api/(api_version)/(api_key)/tileconfig/(tile_id)

   Configures tile specified by `tile_id`. The configuration should comply with
   the specification of a given tile type.

   :param api_version: version of API to be used
   :param api_key: your API key
   :param tile_id: unique tile's ID from your ``layout_config.yaml`` file

   **Example request**:

   .. sourcecode:: http

      GET /api/v0.1/my_key/tileconfig/id_1
      Host: localhost:7272
      POST data: value={"font_color": "#00FF00"}

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/html; charset=UTF-8

      Tile's config updated.


.. http:delete:: /api/(api_version)/(api_key)/tileconfig/(tile_id)

   Resets configuration of the tile specified by `tile_id`.

   :param api_version: version of API to be used
   :param api_key: your API key
   :param tile_id: unique tile's ID from your ``layout_config.yaml`` file

   **Example request**:

   .. sourcecode:: http

      DELETE /api/v0.1/my_key/tileconfig/id_1
      Host: localhost:7272

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/html; charset=UTF-8

      Tile's config deleted.

.. http:get:: /api/(api_version)/(api_key)/tiledata/(tile_id)

   Retrieves data belonging to the tile specified by `tile_id`. May be useful for diagnostics.

   :param api_version: version of API to be used
   :param api_key: your API key
   :param tile_id: unique tile's ID from your ``layout_config.yaml`` file

   **Example request**:

   .. sourcecode:: http

      GET /api/v0.1/my_key/tiledata/id_1
      Host: localhost:7272

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=UTF-8

      {
          "tile_template": "text",
          "meta": {
              "font_color": "#ff9618",
              "font_size": "45px"
          },
          "data": {
              "text": "Lorem ipsum."
          },
          "id": "id_1"
      }

.. http:delete:: /api/(api_version)/(api_key)/tiledata/(tile_id)

   Removes everything belonging to the tile given by `tile_id` from Redis.

   :param api_version: version of API to be used
   :param api_key: your API key
   :param tile_id: unique tile's ID from your ``layout_config.yaml`` file

   **Example request**:

   .. sourcecode:: http

      DELETE /api/v0.1/my_key/tiledata/id_1
      Host: localhost:7272

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/html; charset=UTF-8

      Tile's data deleted.

.. http:get:: /api/(api_version)/(api_key)/info

   Provides information on project and user configuration. This resource has
   been created for debugging purposes.

   :param api_version: version of API to be used
   :param api_key: your API key

   **Example request**:

   .. sourcecode:: http

      GET /api/v0.1/my_key/info
      Host: localhost:7272

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=UTF-8

      {
          "tipboard_version": "1.3.0",
          "project_layout_config": "/home/pylabs/.tipboard/layout_config.yaml",
          "redis_db": {
              "host": "localhost",
              "db": 4,
              "port": 6379
          },
          "project_name": "pylabs"
      }
