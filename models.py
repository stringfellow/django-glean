from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def _get_connectors():
    """Some mechanism to retrieve all available connectors."""
    return (
        ('glean.connectors.galert.GAlertConnector', 'Google Alert'),
    )


class Search(models.Model):
    """A user's configured search profile,"""
    user = models.ForeignKey(User)
    term = models.CharField(max_length=255)


class Feed(models.Model):
    """A user's connection to a service for a search."""
    user = models.ForeignKey(User)
    search = models.ForeignKey(Search)

    connector = models.CharField(max_length=255, choices=_get_connectors())

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
