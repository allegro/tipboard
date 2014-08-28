======
Extras
======

Here you will find description of components which are not a part of the
Tipboard project *per se*, although they may be useful to some of its users.
Assuming standard installation, you can find them here::

  <path_to_your_virtualenv>/lib/python2.7/site-packages/tipboard/extras

.. note::

   If you have developed something of similar nature and you are willing to
   share it, we encourage you to make a pull request to our repo. Thanks!

``jira-ds.py``
--------------

Script for fetching frequently used data from `JIRA
<https://www.atlassian.com/software/jira>`_ issue tracker, in order to present
it on your dashboards.  Returns requested data to stdout in JSON format. For
the list of available options see ``jira-ds.py --help``.

This script is basically a wrapper around ``jira-ds.js``, so those two files
shouldn't be separated. Requires `CasperJS <http://casperjs.org/>`_ and
`PhantomJS <http://phantomjs.org/>`_ installed somewhere in your path (we
suggest using `npm <http://nodejs.org/>`_ for that).

Before you start using them, remember to fill in ``JIRA_CREDENTIALS`` and
``JIRA_BASE_URL`` (in ``jira-ds.py``) as well as ``url_jira`` and
``url_jira_login`` (in ``jira-ds.js``) with the your JIRA credentials, location
of your JIRA instance and its login page.

Tested with JIRA 6.1.x.


``client_code_example.py``
--------------------------

Simple Python script targeted to novice users serving as an example how to glue
together three steps: fetching data, processing it and then sending it to the
tile. See comments in the source code for further explaination.


``fabfile.py``
--------------

Script for quick, automated installations on remote machines.

You need to have `fabric <https://github.com/ronnix/fabtools>`_ and
`fabtools <http://fabtools.readthedocs.org>`_ to use remote install script.

Run::

  fab -H root@host install

-- it will install all needed ``.deb`` packages, create virualenv and set up
Tipboard service using master branch from our main repo.
