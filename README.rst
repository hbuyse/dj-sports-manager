=============================
Django Sports Manager
=============================

.. image:: https://badge.fury.io/py/dj-sports-manager.svg
    :target: https://badge.fury.io/py/dj-sports-manager

.. image:: https://travis-ci.org/hbuyse/dj-sports-manager.svg?branch=master
    :target: https://travis-ci.org/hbuyse/dj-sports-manager

.. image:: https://codecov.io/gh/hbuyse/dj-sports-manager/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/hbuyse/dj-sports-manager

Your project description goes here

Documentation
-------------

The full documentation is at https://dj-sports-manager.readthedocs.io.

Quickstart
----------

Install Django Sports Manager::

    pip install dj-sports-manager

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'sports_manager.apps.DjSportsManagerConfig',
        ...
    )

Add Django Sports Manager's URL patterns:

.. code-block:: python

    from sports_manager import urls as sports_manager_urls


    urlpatterns = [
        ...
        url(r'^', include(sports_manager_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
