
class GleanerBase(object):
    """A base gleaner class from which other gleaners inherit."""

    @classmethod
    def description(cls):
        return cls.__doc__
