#!/usr/bin/env python 
# -*- coding: iso-8859-15 -*-
from django.core.management.base import BaseCommand
from glean.models import Search
from glean import FeedCannotUpdate

class Command(BaseCommand):
    def handle(self, *args, **opts):
        count = 0
        success = 0
        searches = 0
        too_soon = 0
        for search in Search.objects.all():
            searches += 1
            for feed in search.get_feeds():
                count += 1
                try:
                    feed.update()
                    success += 1
                except FeedCannotUpdate:
                    too_soon += 1
        print "Updated %s feeds out of %s, across %s searches" % (
            success, count, searches)
            
