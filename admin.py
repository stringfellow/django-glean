#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.contrib import admin
from django.contrib import messages

from glean import FeedCannotUpdate
from glean.models import Search, Feed, Article


class FeedAdmin(admin.ModelAdmin):
    actions = ['update']

    def update(self, request, queryset):
        for feed in queryset:
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


admin.site.register(Search, list_display=('user', 'term', 'print_synonyms'))
admin.site.register(Feed, FeedAdmin)
admin.site.register(Article, list_display=('title',))
