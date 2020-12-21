.. image:: https://travis-ci.org/AccordBox/wagtail_cache_block.svg?branch=master
    :target: https://travis-ci.org/AccordBox/wagtail_cache_block

=============================
wagtail_cache_block
=============================

This project add ``HTML fragment cache`` to your StreamField block in easy way

Background
-------------

In Wagtail community, it is popular to use the ``HTML fragment cache`` at page level.

This works fine in most of the time. But what if some different page have the same block data and some DB query need be run multiple times when rendering?

In this case, it make sense to make ``HTML fragment cache`` work on block level instead of page level.

How it works
-------------

1. ``cache_block`` is very similar with Django ``{% cache %}``  templatetag, it would pull data from block automatically and use the value to generate fragment cache key.

2. If value in any block field (even ``descendants of the block``) has changed, new fragment key would be generated and new HTML fragment code would be saved to Cache.

3. ``cache_block`` would check if the page is ``preview`` mode, if the page if in preview mode, the ``HTML fragment cache`` would not be pulled from cache.

I have used it in my projects and the performance has been improved, especially for some page which contains many db query.

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

You can use it in StreamField ``for loop`` iteration

Here ``300`` is the cache timeout, ``request`` is Django ``RequestContext``, and ``block`` is the StreamField block.

.. code-block:: HTML

    {% load wagtailcore_tags cache_block_tags %}

    {% for block in page.body %}
        {% cache_block 300 request block %}
            {% include_block block with request=request %}
        {% endcache_block %}
    {% endfor %}

Or you can use it in block template (For example: ``StructBlock``)

.. code-block:: HTML

    {% load wagtailcore_tags cache_block_tags %}

    {% cache_block 300 request block %}
      <section class="{{ block.block_type }}">

        {{ block.value.heading }}
        {{ block.value.paragraph }}

      </section>
    {% endcache_block %}

