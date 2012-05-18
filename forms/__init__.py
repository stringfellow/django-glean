from django.conf import settings

from bootstrap import forms
from chosen import forms as chosenforms

from glean.models import Search, GLEANERS
from glean.forms.rss import RSSFeedForm


def _get_gleaners():
    installed_gleaners = getattr(settings, 'INSTALLED_GLEANERS', GLEANERS)
    return [(gleaner, gleaner) for gleaner in installed_gleaners]


class SearchForm(forms.BootstrapModelForm):
    """Basic search form."""

    class Meta:
        model = Search
        exclude = ('user',)


class GleanerPicker(forms.BootstrapForm):
    """List of feeds"""
    feed_type = chosenforms.ChosenChoiceField(
        overlay="Choose feed type...",
        choices=[(None, "")] + _get_gleaners())
