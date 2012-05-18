#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api
from glean.api.resources import SearchResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(SearchResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
    url(r'^$',
        'glean.views.home',
        name='glean-home'),

    # PERSISTENCE
    url(r'^api/', include(v1_api.urls)),
    url(r'^persist$',
        'glean.views.persist',
        name='glean-persist'),
    url(r'^persist/(?P<search_id>\d+)$',
        'glean.views.persist',
        name='glean-persist'),

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
