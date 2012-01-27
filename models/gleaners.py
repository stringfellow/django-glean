#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from datetime import datetime, timedelta
from django.db import models


class InvalidMetaError(Exception):
    pass


class GleanerBase(models.Model):
    """A base gleaner class from which other gleaners inherit."""
    search = models.ForeignKey(
        'Search', related_name="%(app_label)s_%(class)s_feeds")

    force_term_filter = models.BooleanField(
        default=False,
        help_text="If this is a general feed, force it to filter for the term."
    )

    max_update_frequency = models.FloatField(default=1)
    last_updated = models.DateTimeField()
    articles = models.ManyToManyField(
        'Article', related_name="%(app_label)s_%(class)s_sources",
        null=True, blank=True)

    class Meta:
        abstract = True
        app_label="glean"

    @classmethod
    def description(cls):
        return cls.__doc__

    @classmethod
    def classname(cls):
        return cls.__name__

    def __unicode__(self):
        """A (unique?) name."""
        return u"Unknown"

    def next_update(self):
        """What is the next update date?"""
        delta = timedelta(minutes=self.max_update_frequency)
        return self.last_updated + delta

    def can_update(self):
        """Can we update? Check the feed's last update..."""
        return datetime.now() > self.next_update()

    def filter(self, entries):
        """If we need to, filter the entries."""
        if self.force_term_filter:
            raise NotImplemented
        return entries

    def update(self):
        """Gets/creates articles using own method, adds to feed.

        1. Find articles in stream
        2. Get/create them
        3. Update them with the feed object
        4. Return True, or bubble up Exception

        """
        raise NotImplemented
