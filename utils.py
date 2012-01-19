#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import datetime

from glean.models import Article


def get_or_create_article(params, keys=[], tags=[]):
    """Make or create an article, using keys to determine uniqueness."""
    # make a lookup dict of the desired key fields
    lookup_dict = dict([(k, params[k]) for k in keys])
    try:
        article = Article.objects.get(**lookup_dict)
        for k, v in params.items():  # update the article, if needed.
            setattr(article, k, v)
        article.save()
    except Article.DoesNotExist:
        article = Article(**params)
        article.found_date = datetime.datetime.now()
        article.save()

    # add tags passed in, how we found this
    article.tags.add(*tags)
    # update body, snapshot etc.
    update_content(article)
    return article


def update_content(article):
    """A base method that does lots of snapshotting and processing."""
    old_body = article.body
    get_body(article)
    snapshot_article(old_body, article)


def get_body(article):
    """Go to the URL and grab the body."""
    pass


def snapshot_article(old_body, article):
    """Get a PDF snapshot of the article, if the body is different enough"""
    pass


def paged_article_follower(url):
    """For articles that are split, knows to follow the page links & join."""
    pass
