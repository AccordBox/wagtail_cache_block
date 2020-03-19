# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from django.conf.urls import url, include


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    # url(r'^', include('wagtail_cache_block.urls', namespace='wagtail_cache_block')),
]

urlpatterns += [
    url(r'', include(wagtail_urls)),
]
