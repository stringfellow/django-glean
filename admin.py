#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.contrib import admin
from django.contrib import messages

from glean import FeedCannotUpdate
from glean.models import Search, Article
from glean.models import RSSFeed


class SearchAdmin(admin.ModelAdmin):
    actions = ['update']
    list_display=('user', 'term', 'print_synonyms')

    def update(self, request, queryset):
        for search in queryset:
            feeds = search.get_feeds()

            for feed in feeds:
                try:
                    if feed.update():
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            '%s updated.' % feed)
                except FeedCannotUpdate:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        '%s cannot update - too soon!' % feed)
    update.short_description = "Update feeds"


admin.site.register(RSSFeed)
admin.site.register(Search, SearchAdmin)
admin.site.register(Article, list_display=('title',))
