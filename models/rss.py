#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import datetime
import feedparser

from django.db import models

from glean import FeedCannotUpdate
from glean.doc_inherit import doc_inherit
from glean.models.gleaners import GleanerBase
from glean.utils import get_or_create_article


class RSSFeed(GleanerBase):
    """Grabs stories from an RSS feed."""
    url = models.URLField()

    def __unicode__(self):
        try:
            return self.url
        except AttributeError:
            return u"(Uninitialised)"

    def render_setup(self):
        """Renders all info needed to get its meta data."""
        pass

    def _save_entry_to_article(self, entry):
        """Given a feed entry, make an article."""
        matches = entry.pop('MATCHES', [])
        params = dict(
            title=entry.get('title', '--NO TITLE--'),
            url=entry.get('link', '--NO LINK--'),
            summary=entry.get('description', '--NO DESCRIPTION--'),
            # bit blunt, but does the job for now
            extra_meta=str(entry),
        )
        _article = get_or_create_article(params, ['title', 'url'], matches)
        self.articles.add(_article)
        self.save()

    def _match_terms(self, value):
        """Check if term is in value, return matched."""
        try:
            _ = iter(value)
            if type(value) == dict:
                result = set([])
                for k, v in value.items():
                    result |= self._match_terms(v)
                return result
            elif isinstance(value, basestring):
                value = value.lower().split(' ')

            return self.search.all_terms() & set(value)
        except TypeError:
            return set([])

    def _tag_entries(self, entries):
        """Attach the matched terms to the entry."""
        for entry in entries:
            matches = set([])
            for k, v in entry.items():
                matches |= self._match_terms(v)

            entry['MATCHES'] = list(matches)
        return entries

    @doc_inherit
    def filter(self, entries):
        if not self.force_term_filter:
            return entries
        return filter(lambda e: len(e['MATCHES']) > 0, entries)

    @doc_inherit
    def update(self):
        if not self.can_update():
            raise FeedCannotUpdate
        _f = feedparser.parse(self.url)
        entries = self.filter(self._tag_entries(_f.entries))

        for entry in entries:
            self._save_entry_to_article(entry)
        self.last_updated = datetime.datetime.now()
        self.save()
        return True
