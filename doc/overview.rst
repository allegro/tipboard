Overview
--------

Tipboard is a system for creating dashboards, written in JavaScript and Python.
Its widgets ('tiles' in Tipboard's terminology) are completely separated from
data sources, which provides great flexibility and relatively high degree of
possible customizations.

Because of its intended target (displaying various data and statistics in your
office), it is optimized for larger screens.

Similar projects: `Geckoboard <http://www.geckoboard.com/>`_,
`Dashing <http://shopify.github.io/dashing/>`_.

Project assumptions
~~~~~~~~~~~~~~~~~~~

#. Defining a dashboard layout (number of lines, columns, types of tiles etc.).
#. Clear separation between tiles and data sources.
#. Ability to create own tiles and scripts querying data sources (e.g. Jira, Bamboo, Confluence etc.).
#. Feeding tiles via REST API.
