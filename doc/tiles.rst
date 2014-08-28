=====
Tiles
=====

Every tile consists of an obligatory ``.html`` file and two optional ``.css``
and ``.js`` files. All three files belonging to a tile should have the same
name that corresponds with the tile name – e.g. with the ``pie_chart`` tile
these are ``pie_chart.html``, ``pie_chart.css`` and ``pie_chart.js`` files
respectively.

Customising tiles
-----------------

If you want to modify a tile (e.g. change a CSS attribute, which obviously
cannot be done via API), copy a desired file in the folder of tiles delivered
with the application (i.e.
``<path_to_your_virtualenv>/lib/python2.7/site-packages/tipboard/tiles``),
paste it in your tile folder (i.e. ``~/.tipboard/custom_tiles``) and edit
according to your needs.

Files in your ``custom_tiles`` folder take precedence over those shipped by
default with the application and thus you can easily replace desired elements
(e.g. if you want to change the text colour, just copy and edit the ``.css``
file – without touching ``.html`` and ``.js`` files). We plan to introduce a
command simplifying this process in the future.

Color palette
-------------

Color palette used by Tipboard's tiles is defined as shown in the table below.
To retain consistency, we strongly suggest sticking to them while customising
tiles.

+-------------+---------------------+
| Value       | Name                |
+=============+=====================+
| ``#000000`` | ``black``           |
+-------------+---------------------+
| ``#FFFFFF`` | ``white``           |
+-------------+---------------------+
| ``#25282D`` | ``tile_background`` |
+-------------+---------------------+
| ``#DC5945`` | ``red``             |
+-------------+---------------------+
| ``#FF9618`` | ``yellow``          |
+-------------+---------------------+
| ``#94C140`` | ``green``           |
+-------------+---------------------+
| ``#12B0C5`` | ``blue``            |
+-------------+---------------------+
| ``#9C4274`` | ``violet``          |
+-------------+---------------------+
| ``#EC663C`` | ``orange``          |
+-------------+---------------------+
| ``#54C5C0`` | ``naval``           |
+-------------+---------------------+

Common elements
---------------

* tile's content (``data`` key) and its configuration (``value`` key) should be
  send as two separate requests - once you have established desired
  configuration it does not make much sense to send it over and over again;
* in order to reset tile's config, you just send an empty ``value`` key (e.g.
  ``value = {}``).

.. _tiles_library:

Library of available tiles
--------------------------

In the following pages we present a "library" of available tiles (i.e. those
bundled with the application), which should serve as a specification how to
send data to them and how to set up its configuration options.

.. toctree::
   :maxdepth: 2

   tile__text
   tile__pie_chart
   tile__line_chart
   tile__cumulative_flow
   tile__simple_percentage
   tile__listing
   tile__bar_chart
   tile__fancy_listing
   tile__big_value
   tile__just_value
   tile__advanced_plot
   tile__norm_chart

.. note::

   In order to keep brevity, all examples presented in specifications above do
   not include any escape characters. Therefore, it's up to you to insert them
   where necessary.

   And also, remember to set all the elements in angle brackets (e.g.
   ``<api_key>``, ``<tile_id>`` etc.) to reflect your configuration.
