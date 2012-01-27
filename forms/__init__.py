from bootstrap import forms
from chosen import forms as chosenforms

from glean.models import Search
from glean.forms.rss import RSSFeedForm


class SearchForm(forms.BootstrapModelForm):
    """Basic search form."""

    class Meta:
        model = Search
        exclude = ('user',)


class GleanerPicker(forms.BootstrapForm):
    """List of feeds"""
    feed_type = chosenforms.ChosenChoiceField(
        overlay="Choose feed type...",
        choices=(('glean.models.rss.RSSFeed', 'RSS Feed'),))
