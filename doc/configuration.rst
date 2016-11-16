=============
Configuration
=============

The description below assumes that you have installed Tipboard correctly and
use a default configuration that is the starting point for steps presented
below (see section :ref:`installation`).

Default configuration
---------------------

First thing that you need to do after a successful installation is to create an
empty config that will provide a base for your customizations. Type in this
command::

  (tb-env)$ tipboard create_project <name_of_project>

It will create ``~/.tipboard`` directory with the following content:

* ``settings-local.yaml`` file that defines the layout of tiles on the
  dashboard you are creating;

* ``settings-local.py`` file in which you can overwrite default (global)
  application settings; a description of options and their default values has
  been presented in `this file
  <https://github.com/allegro/tipboard/blob/develop/tipboard/settings.py>`_;

* ``custom_tiles`` subdir to place your own tiles.

.. note::

   Before you send anything to your tiles, you have to get your API key
   first, which is described in the :ref:`api_key` section.

Launching Tipboard app
----------------------

Having default config in place, you may launch Tipboard with the command::

  (tb-env)$ tipboard runserver [<host>] [<port>]

...where ``host`` and ``port`` parameters are optional (by default these are
``localhost`` and ``7272``; if you want the application to listen on all the
network interfaces, set ``host`` to ``0.0.0.0``).

You can now point your web browser to ``http://localhost:7272`` - you should
see a basic, empty layout with tiles in 2 lines of 4 columns each.

Customising tile layout
-----------------------

As mentioned previously, the layout of tiles in a dashboard is defined by
``layout_config.yaml`` file. The file is in the `YAML <http://yaml.org>`_
format, the description of which is beyond the scope of this manual. However,
it is worth indicating that YAML has certain format requirements –
**indentation should have a unified structure** (be a multiplication of a
number, e.g. 4), when creating indentations **spaces should not be mixed with
tabs**.

Below you can find a list of options that can be saved in the file.
Indentations indicate the position of a given option in the configuration (e.g.
``details`` are superior to ``page_title``).

::

  details
      page_tile
  layout
      row_X_of_Y
      col_X_of_Y
          tile_template
          tile_id
          tile
          timeout

where:

.. describe:: details

   A section that contains additional configuration parameters; for the time
   being it is only ‘page_title’; depending on his needs, the users add other
   elements.

.. describe:: page_tile

   A section that defines the title of a page to appear in the web browser
   after entering the dashboard.

.. describe:: layout

   A section that contains a proper configuration of the tile layout.

.. describe:: row_X_of_Y

   Defines a row hight; a sum of Xs should equal Y.

.. describe:: col_X_of_Y

   Similar to above but concerns a column width in a given row.

.. describe:: tile_template

   The name of a tile template to be displayed (e.g.  ``pie_chart``,
   ``line_chart``, ``cumulative_flow``)

.. describe:: tile_id

   A tile identifier in a HTML document and key identifier in Redis.

.. describe:: title

   A title to be displayed in the upper part of the tile.

.. describe:: timeout

   The length (in seconds) of data life (if data is not sent during this time,
   you will be informed that the data is stalled). Since interval used by the
   application to check for those timeouts is 5 seconds, it doesn't make sense
   to set this value smaller than this.

   .. versionadded:: 1.3.0

The method of using ``row_X_of_Y`` and ``col_X_of_Y`` has been presented in the
examples below. If you want to see how it's done "from the kitchen", and you
have some basic knowledge of CSS styling, have a look `here
<https://github.com/allegro/tipboard/blob/develop/tipboard/static/css/layout.css>`_;

.. note::

   If you want to present a lot of data on your dashboard, consider dividing
   all your tiles into two (or more) separate dashboards. Tiles offer a limited
   capacity and if you "feed" them with too much data (e.g. long lines of
   text), it is possible the dashboard will get broken.

Setting tiles' rotation
~~~~~~~~~~~~~~~~~~~~~~~

One of the most useful functions is defining tiles to rotate. In a single
container (i.e. in one of the fields indicated by ``col_X_of_Y`` and
``row_X_of_Y``), you may define a few tiles to be displayed in this location as
items rotating at intervals defined in the configuration (similar to ads
rotating on bus/tram stops, so-called citylights). To achieve that:

* add the ``flip-time-xx`` class to a container, where ``xx`` is rotation
  interval in seconds;
* add tile to the container.

The example below presents a container with two tiles (one of the ``empty`` type,
the other of the ``text`` type) to rotate every 2 seconds (``flip-time-2``).
The rotation will start with the ``empty`` type tile::

  layout:
    - row_1_of_2:
      - col_1_of_4 flip-time-2:
        - tile_template: empty
          tile_id: empty
          title: Empty Tile 2

        - tile_template: text
          tile_id: text
          title: Empty Tile

Sample layout
~~~~~~~~~~~~~

Let's assume we want to define a layout as on the scheme below (i.e. a division
into 2 equal rows, with the upper one divided into 4 columns, and the lower one
divided into 3 columns)::

  +-------+--------+--------+-------+
  |       |        |        |       |
  |       |        |        |       |
  |       |        |        |       |
  |       |        |        |       |
  +-------+--+-----+----+---+-------+
  |          |          |           |
  |          |          |           |
  |          |          |           |
  |          |          |           |
  +----------+----------+-----------+

...its corresponding configuration file should look as follows (for brevity, I
will present only the ``layout`` section, skipping the ``tile_template``,
``title_id``, etc.)::

  layout:
      row_1_of_2:
          col_1_of_4:
          col_1_of_4:
          col_1_of_4:
          col_1_of_4:
      row_1_of_2:
          col_1_of_3:
          col_1_of_3:
          col_1_of_3:

Multiple dashboards per application's instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. versionadded:: 1.3.0

It is possible to define multiple dashboards per application's instance. In
order to achieve that, you just create separate layout config files (one per
every dashboard) - having done that, your dashboards will be available at::

  http://localhost:7272/<name_of_layout_config_file>

For example, having two layout config files ``my_first_dashboard.yaml`` and
``my_second_dashboard.yaml``, the corresponding dashboards can be accessed
via::

  http://localhost:7272/my_first_dashboard
  http://localhost:7272/my_second_dashboard

.. note::

   You have to strip the ``.yaml`` file extension when constructing your URLs.

When it comes to feeding those dashboards with data, the future data location
is specified by tile IDs (unique within application instance). Therefore, there
is no need to specify different URLs for different dashboards - having tiles'
IDs, Tipboard will make sure that your data is delivered where it should be.

Multiple rotating dashboards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.3.0

If you have defined several dashboards (as described above), you may want to
rotate (flip) them periodically. If you are unsure what that means, think of
extensions like Revolver (Chrome) or Tab Slideshow (Firefox).

To achieve that, you need:

* at least two dashboards (well, that's kind of obvious)
* in the file ``settings-local.py`` add the variable ``FLIPBOARD_INTERVAL =
  <seconds>`` (e.g. ``FLIPBOARD_INTERVAL = 5``)

The above solution will make all your dashboards rotate - if you want to limit
this behavior and rotate only certain dashboards, just add another parameter
``FLIPBOARD_SEQUENCE`` which is just a list of dashboard names that should be
taken into account, e.g.::

  FLIPBOARD_SEQUENCE = ['my_first_dashboard', 'my_third_dashboard']

.. note::

   Every change in ``settings-local.py`` file requires restart of the
   application.
