#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import datetime
import feedparser

from glean import FeedCannotUpdate
from glean.doc_inherit import doc_inherit
from glean.gleaners import GleanerBase


class RSSFeed(GleanerBase):
    """Grabs stories from an RSS feed."""

    @doc_inherit
    def meta(self):
        return (
            'URL',
        )

    @doc_inherit
    def update(self, feed):
        if not self.can_update(feed):
            raise FeedCannotUpdate 
        _f = feedparser.parse(self.URL)
        feed.last_updated = datetime.datetime.now()
        feed.save()
        return True
