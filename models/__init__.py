#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from glean.models.gleaners import GleanerBase
from glean.models.rss import RSSFeed


class Search(models.Model):
    """A user's configured search profile,"""
    user = models.ForeignKey(User)
    term = models.CharField(max_length=255)
    synonyms = models.TextField(default="", help_text="One per line")

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

    def __unicode__(self):
        return u"%s seeks '%s'" % (self.user, self.term)
#
#
#class Feed(models.Model):
#    """A user's connection to a service for a search."""
#    user = models.ForeignKey(User)
#    search = models.ForeignKey(Search)
#
#    connector = models.CharField(max_length=255, choices=_get_connectors())
#
#    # the meta field is populated by whatever the feed needs...
#    force_term_filter = models.BooleanField(
#        default=False,
#        help_text="If this is a general feed, force it to filter for the term."
#    )
#    meta = models.TextField(blank=True, default="")
#
#    last_updated = models.DateTimeField()
#
#    def __unicode__(self):
#        gleaner = self.get_connector()
#        return u"[%s - %s] %s" % (
#            gleaner.classname(), gleaner, self.search)
#
#    def get_connector(self):
#        if hasattr(self, '_connector'):
#            return self._connector
#        else:
#            self._connector = registry.find(self.connector)(self.meta, self)
#            return self._connector
#
#    def update(self):
#        """Using the initialised connector, update me!"""
#        return self.get_connector().update()


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
