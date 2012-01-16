#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.contrib import admin

from glean.models import Search, Feed, Article

admin.site.register(Search)
admin.site.register(Feed)
admin.site.register(Article)
