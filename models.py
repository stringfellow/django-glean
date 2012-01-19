from django.db import models
from django.contrib.auth.models import User

from glean.registry import registry, autodiscover

try:
    # if the admin gets hit before the URLS then we need to reg.
    if len(registry.keys()) == 0:
        autodiscover()
except:
    pass


def _get_connectors():
    """Some mechanism to retrieve all available connectors."""
    for key, cls in registry.items():
        yield (key, cls.description())


class Search(models.Model):
    """A user's configured search profile,"""
    user = models.ForeignKey(User)
    term = models.CharField(max_length=255)
    synonyms = models.TextField(default="", help_text="One per line")

    def get_synonyms(self):
        """Just get synonyms from list."""
        return filter(lambda s: len(s), self.synonyms.split('\n'))

    def all_terms(self):
        """Set of all term, synonyms."""
        terms = self.get_synonyms()
        terms.append(self.term)
        return set(terms)

    def __unicode__(self):
        return u"%s seeks '%s'" % (self.user, self.term)


class Feed(models.Model):
    """A user's connection to a service for a search."""
    user = models.ForeignKey(User)
    search = models.ForeignKey(Search)

    connector = models.CharField(max_length=255, choices=_get_connectors())

    # the meta field is populated by whatever the feed needs...
    force_term_filter = models.BooleanField(
        default=False,
        help_text="If this is a general feed, force it to filter for the term."
    )
    meta = models.TextField(blank=True, default="")

    last_updated = models.DateTimeField()

    def __unicode__(self):
        gleaner = self.get_connector()
        return u"[%s - %s] %s" % (
            gleaner.classname(), gleaner, self.search)

    def get_connector(self):
        if hasattr(self, '_connector'):
            return self._connector
        else:
            self._connector = registry.find(self.connector)(self.meta, self)
            return self._connector

    def update(self):
        """Using the initialised connector, update me!"""
        return self.get_connector().update()


class Article(models.Model):
    """A found thing."""
    found_date = models.DateTimeField()
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    feed_sources = models.ManyToManyField(Feed, null=True, blank=True)
    
    extra_meta = models.TextField(null=True, blank=True)

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
