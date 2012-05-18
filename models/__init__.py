#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from glean.models.gleaners import GleanerBase
from glean.models.rss import RSSFeed

GLEANERS = [
    'glean.RSSFeed',
]

class Search(models.Model):
    """A user's configured search profile,"""
    user = models.ForeignKey(User)
    term = models.CharField(max_length=255, help_text="Search term")
    synonyms = models.TextField(
        default="", blank=True, null=True,
        help_text="One per line")

    def get_feeds(self):
        """Get all feeds for this search.
        
        A little introspection here as feeds are children of an ABC.

        """
        # TODO: find a more elegant way to do this.
        getters = [
            r.model.search.field.related_query_name()
            for r in self._meta.get_all_related_objects()
            if issubclass(r.model, GleanerBase)]
        feeds = []
        for getter in getters:
            mgr = getattr(self, getter)
            feeds.extend(mgr.all())
        return feeds

    def get_synonyms(self):
        """Just get synonyms from list."""
        return map(lambda s: s.strip().lower(),
                   filter(lambda s: len(s), self.synonyms.split('\n')))

    def print_synonyms(self):
        """Just for list display, really."""
        return ", ".join(self.get_synonyms())

    def all_terms(self):
        """Set of all term, synonyms."""
        terms = self.get_synonyms()
        terms.append(self.term)
        return set(terms)

    def latest_update(self):
        """Return the last date that an article was found."""
        latest = None
        for feed in self.get_feeds():
            articles = feed.articles.order_by('-found_date')
            if articles.count():
                _a = articles[0]
                if not latest or latest.found_date < _a.found_date:
                    latest = _a
        return latest.found_date if latest else None

    def __unicode__(self):
        return u"%s seeks '%s'" % (self.user, self.term)


class Article(models.Model):
    """A found thing."""
    found_date = models.DateTimeField()
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    
    extra_meta = models.TextField(null=True, blank=True)

    tags = TaggableManager()

    def __unicode__(self):
        return self.title


class Snapshot(models.Model):
    """A snapshot of an article."""
    datetime = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article)
    body = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="snapshots", null=True, blank=True)

    def __unicode__(self):
        return "[%s] %s" % (self.datetime, self.article)
