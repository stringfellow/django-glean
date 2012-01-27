from bootstrap import forms
from chosen import forms as chosenforms

from glean.models import Search
from glean.forms.rss import RSSFeedForm
from glean.registry import registry, autodiscover

def _get_gleaners():
    if registry.is_empty():
        autodiscover("models")
    return registry.choices()


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
