=====
Usage
=====

To use wagtail_cache_block in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail_cache_block.apps.WagtailCacheBlockConfig',
        ...
    )

Add wagtail_cache_block's URL patterns:

.. code-block:: python

    from wagtail_cache_block import urls as wagtail_cache_block_urls


    urlpatterns = [
        ...
        url(r'^', include(wagtail_cache_block_urls)),
        ...
    ]
