#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from bootstrap import forms

from glean.models.rss import RSSFeed

class RSSFeedForm(forms.BootstrapModelForm):
    """Present the fields for the RSSFeed"""
    class Meta:
        model = RSSFeed 
