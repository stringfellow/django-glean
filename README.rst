Django-Glean
============

A django app to gather data from various sources, and do useful things with it.


Spec
====

A quick English description:

Django-glean allows a user to track a 'thing', such as a country, sector,
company, product... It will allow the user to manage and sort feeds of data
about their things. It will categorise and pool articles/elements of the feeds.
It will archive the data.

Requirements
------------

 * Have things to search for.
 * Have feeds that relate to these search terms.
 * Allow users to associate with things.
 * Archive any 'article' that is found for a thing.
 * Tag the articles with the thing and any other info that can be gleaned (e.g.
   by NLP).
 * Allow other users to search on a thing, and find the other user's results.
 * Rate the articles with relation to the thing they are intended / the tags to
   feedback to processor.
 * ... 

Definitions
-----------

Feed
````
A feed is an information source. A few obvious ones:
 * Google Alert RSS
 * Twitter search
 * BBC/News RSS

A feed is slightly independent of the search that it is looking for:
 * A Google Alert feed searching for e.g. 'United Kingdom' as the user Dave
   will be able to get info as Dave and Bob who is also looking for the term
   'United Kingdom' could retrieve data from it (?)
 * This is really useful for e.g. twitter where one users's results of a search
   may be different from another due to e.g. rate limiting.
 * So, a user's searches are 'subscribed' to, with attached and configured
   'feeds' that are then pooled (for the collective good!)

A feed exposes the data underneath in a known way:
 * A twitter search result, items are single tweets, the subject and the body
   are probably just the tweet text, the source is the tiwtter handle, the
   date/time/location can be retrieved etc etc.
 * For the result of a GAlert, we might not have the location field available
   but the subject and body will differ greatly.


