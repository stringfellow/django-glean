#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^$',
        'glean.views.home',
        name='glean-home'),

    # GLEANERS
    url(r'^gleaners/$',
        'glean.views.gleaners',
        name="glean-gleaners"),


    # SEARCHES
    url(r'^search/create/$',
        'glean.views.search_create',
        name='glean-search-create'),
    url(r'^search/gleaner/chooser/$',
        'glean.views.gleaner_chooser',
        name='glean-gleaner-chooser'),
    url(r'^search/gleaner/form/(?P<gleaner_class>[^/]+)/$',
        'glean.views.gleaner_form',
        name='glean-gleaner-form'),
)
