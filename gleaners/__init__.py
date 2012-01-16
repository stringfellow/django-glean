
class GleanerBase(object):
    """A base gleaner class from which other gleaners inherit."""

    @classmethod
    def description(cls):
        return cls.__doc__

    @classmethod
    def classname(cls):
        return cls.__name__
