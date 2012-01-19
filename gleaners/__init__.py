from datetime import datetime, timedelta
from django.utils import simplejson as json


class InvalidMetaError(Exception):
    pass


class GleanerBase(object):
    """A base gleaner class from which other gleaners inherit."""
    max_update_frequency = 1  # minutes

    @classmethod
    def description(cls):
        return cls.__doc__

    @classmethod
    def classname(cls):
        return cls.__name__

    def meta(self):
        """A set of keys for which we need values."""
        return []

    def __unicode__(self):
        """A (unique?) name."""
        return u"Unknown"

    def __getattr__(self, name):
        """Quick access to opts. May be dangerous..."""
        if name in self._options:
            return self._options[name]
        raise AttributeError

    def __init__(self, meta, feed):
        self.feed = feed
        self._options = {}
        if type(meta) == dict:
            self._options = meta
        elif type(meta) == unicode:
            self._options = json.loads(meta)
        else:
            raise InvalidMetaError("Want dict or string, got %s" % type(meta))

    def can_update(self):
        """Can we update? Check the feed's last update..."""
        last_updated = self.feed.last_updated
        delta = datetime.now() - last_updated
        return delta >= timedelta(minutes=self.max_update_frequency)

    def filter(self, entries):
        """If we need to, filter the entries."""
        if self.feed.force_term_filter:
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
