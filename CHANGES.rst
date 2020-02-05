Change Log
----------

2.0.6
~~~~~

2.0.6
~~~~~

* Update archi of package to be compatible with setup.py

* Fix Manifest.in to support new archi

* Fix travis CI

* Circle-CI Workflow, build and push new pypi release when PR #70

* add Gitlab-Ci to push new package on Github and to push image on docker hub

* Create new package Tipboard2.0 on pypi https://pypi.org/project/tipboard2.0/

* cleaning version


2.0.2
~~~~~

* WIP: Readme add deploy exemple

* WIP: add Badge status in Readme to see status of differents CI and CD

* WIP: adding chart helm support to deploy on kubernets cluster, with or without redis in the stack

* WIP: Azure pipeline CI/CD

* Conditional print log, from the properties.json

* WIP: Unit test to be compatible with django

2.0.0
~~~~~

* Merging config_data and tile data over new route /update to answer issue #21

* fix websocket latency

* Change color by Material color


1.5.0
~~~~~

* Migrate Python2.7 to Python3.7 and upgrading all python library
    * Removed libraries:
        * mock==1.0.1
        * requests==1.2.3
        * six>=1.4.1
        * tornado-redis==2.4.2
        * tornado==3.0.1
        * docopt==0.6.1
        * raven==3.5.2
        * Sphinx==1.2.2
        * sphinxcontrib-httpdomain==1.3.0

    * Added libraries:
        * django>=2.2.1
        * django-prometheus>=1.0.15
        * django-cors-headers>=3.0.1
        * channels>=2.2.0
        * channels_redis>=2.4.0
        * asgiref>=3.1.4

* Using Django2.0 over tornado now
    * Updating tornado template tiles-.html to template django, moving them in templates directory
    * Using channels_redis.core.RedisChannelLayer over tornadoredis
    * Using channels.generic.websocket over tornado.websocket.WebSocketHandler
    * Using static files from django behavior over tornado.web.StaticFileHandler
    * Moving tornado url routing behavior to the django behavior
    * removing duplicate inner function to a single file utils.py
    * reworking of the file redis_utils.py to a cache.py
    * Config for ASGI_APPLICATION

* Moving the .tipboard directory to ./tipboard/Config/ to make it compatible with bitnami/python

* Adding dockerfile support
    * Using bitnami image in order to be cloud ready
    * Using non root image


* Adding .gitlab-ci to CI with gitlab

* Adding .travis.yml to CI with github

* Minor fixes, improvements, cleanups etc.



1.4.1
~~~~~

Released on November 16, 2016.

* Fixes for tiles: 'advanced_plot', 'simple_percentage' and 'text-tile'.

* Fix for tile keys cache.

* Added support for RequireJS.

* Make use of simplify.js to make charts (in e.g. 'line_chart' tile) more readable.

* Fix for 'Target dimension not set' error when layout 'row_1_of_1' is used.

* Minor fixes, improvements, cleanups etc.


1.4.0
~~~~~

Released on August 28, 2014.

* Tipboard got open-sourced!


1.3.1
~~~~~

Released on July 23, 2014.

* Added extensive documentation.

* Numerous fixes in 'jira-ds' script (e.g added timeouts).

* Fixed definitions of colors available for tiles.

* Fixed checking for expired data (+ made it timezone aware).

* Added integration with Travis.

* Changed default size of the log files.


1.3.0
~~~~~

Released on February 17, 2014.

New features:

* Fading highlighter (for just_value, big_value and simple_percentage tiles).

* Fancy centering options for fancy_listing tile.

* Notifications on data expiration.

* New tile: norm_chart.

* Possibility to define more than one dashboard per application instance.


Bug fixes:

* Tiles no longer vanish when flipping is enabled.

* Characters like '.' or '-' (and some others) in tiles' ids are no longer
  causing problems.

* Renderer names (like OHLCRenderer, MarkerRenderer, ShadowRenderer and
  ShapeRenderer) can now safely be passed to tiles' configs.


Others:

* Error messages displayed on tiles got more emphasis.

* Renderer names (in tiles' configs) are now case insensitive.

* Added frontend tests and selector for tests.


1.2.0
~~~~~

Released on December 19, 2013.

This release brings new features and some minor bugfixes.

* New tiles: big_value, just_value, advanced_plot.

* Rewritten 'jira-ds' script with some new options (e.g. 'maxResults' for JQL).

* Completely new graphic theme - with new colors, fonts etc.

* Fixed existing tests and some new added.

* Exceptions raised by JavaScript are now displayed on the tiles.

* Improved config handling for bar_chart, pie_chart and line_chart.

* Added possibility to specify specialized renderers for almost all plots
  (except cumulative_flow).


1.1.0
~~~~~

Released on November 20, 2013.

This release contains multiple improvements and bugfixes:

* Tiles are no longer packages (i.e. folders).

* Reorganized files/folders structure.

* Massively reduced app's settings.

* Simplified layout config (no more classes, only one keyword needed to get
  tile flips working).

* New tiles: bar_chart, fancy_listing.

* Improved scaling of tiles + some cosmetic changes.

* Unique API key is generated automatically for every project.

* Fabric script for administrative installs


1.0.0
~~~~~

Released on November 06, 2013.

This is the first release of Tipboard.

* initial release
