=====
Usage
=====

To use Django Sports Manager in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_sports_manager.apps.DjSportsManagerConfig',
        ...
    )

Add Django Sports Manager's URL patterns:

.. code-block:: python

    from dj_sports_manager import urls as dj_sports_manager_urls


    urlpatterns = [
        ...
        url(r'^', include(dj_sports_manager_urls)),
        ...
    ]
