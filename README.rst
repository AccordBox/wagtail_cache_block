.. image:: https://travis-ci.org/AccordBox/wagtail_cache_block.svg?branch=master
    :target: https://travis-ci.org/AccordBox/wagtail_cache_block

=============================
wagtail_cache_block
=============================

This project adds ``HTML fragment cache`` to your StreamField block in an easy way

Background
-------------

In the Wagtail community, it is popular to use the ``HTML fragment cache`` at page level.

This works fine most of the time. But what if different pages have the same block data and a DB query needs be run multiple times when rendering?

In this case, it makes sense to make ``HTML fragment cache`` work on block level instead of page level.

How it works
-------------

1. ``cache_block`` is very similar to the Django ``{% cache %}``  templatetag. It pulls data from the block automatically and uses the value to generate a fragment cache key.

2. If the value in any block field (even ``descendants of the block``) has changed, a new fragment key will be generated and a new HTML fragment code will be stored in the cache.

3. ``cache_block`` checks if the page is ``preview`` mode; if the page is in preview mode, the ``HTML fragment cache`` will not be pulled from cache.

I have used it in my projects and the performance has improved, especially for pages which contain many db queries.

Quickstart
----------

Install wagtail_cache_block::

    pip install wagtail_cache_block

Add it to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail_cache_block.apps.WagtailCacheBlockConfig',
        ...
    )

You can use it in the StreamField ``for loop`` iteration

Here ``300`` is the cache timeout, ``page`` is the Wagtail page instance, and ``block`` is the StreamField block.

.. code-block:: HTML

    {% load wagtailcore_tags cache_block_tags %}

    {% for block in page.body %}
      {% cache_block 300 page block %}
        {% include_block block %}
      {% endcache_block %}
    {% endfor %}

Or you can use it in your block template (For example: ``StructBlock``)

.. code-block:: HTML

    {% load wagtailcore_tags cache_block_tags %}

    {% cache_block 300 page block %}
      <section class="{{ block.block_type }}">

        {{ block.value.heading }}
        {{ block.value.paragraph }}

      </section>
    {% endcache_block %}

