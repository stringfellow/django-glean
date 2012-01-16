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

    def __unicode__(self):
        return u"%s seeks '%s'" % (self.user, self.term)


class Feed(models.Model):
    """A user's connection to a service for a search."""
    user = models.ForeignKey(User)
    search = models.ForeignKey(Search)

    connector = models.CharField(max_length=255, choices=_get_connectors())

    def __unicode__(self):
        return u"[%s] %s" % (
            self.get_connector().classname(), self.search)

    def get_connector(self):
        if hasattr(self, '_connector'):
            return self._connector
        else:
            self._connector = registry.find(self.connector)
            return self._connector

    def update(self):
        pass


class Article(models.Model):
    """A found thing."""
    found_date = models.DateTimeField()
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    feed_sources = models.ManyToManyField(Feed, null=True, blank=True)
    snapshot = models.FileField(upload_to="snapshots", null=True, blank=True)
    
    extra_meta = models.TextField(null=True, blank=True)
