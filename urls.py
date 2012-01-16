#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.conf.urls.defaults import patterns, include, url

from glean import registry

registry.autodiscover()

urlpatterns = patterns('',
    url(r'^gleaners/$',
        'glean.views.gleaners',
        name="glean-gleaners"),
)
