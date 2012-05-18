#!/usr/bin/env python 
# -*- coding: iso-8859-15 -*-
from tastypie.authentication import Authentication


class DjangoAuthentication(Authentication):
    """Just check that the request is an authenticated one...
    
    Feels like maybe I missed the point here, but our use-case is simple:
        we just use the API to interact with the front end.

    """
    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()

    def get_identifier(self, request):
        return request.user.username
