#!/usr/bin/env python 
# -*- coding: iso-8859-15 -*-

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError

from tastypie import fields
from tastypie import http
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import Authentication
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse

from glean.models import Search
from glean.api.auth import DjangoAuthentication


class SpineFrontedResource(ModelResource):
    """A base model resource for spine-fronted models.

        * Bins the 'id' that spine sends.
        * Removes 'meta' from the list, returns only objects.

        Subclasses should set `always_return_data = True` in Meta.

        """
    def obj_create(self, bundle, request=None, **kwargs):
        """For spine, ignore the 'id' and use our own."""

        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        del(bundle.data['id'])  # strip spine's id.

        bundle = self.full_hydrate(bundle)

        # Save FKs just in case.
        self.save_related(bundle)

        # Save the main object.
        bundle.obj.save()

        # Now pick up the M2M bits.
        m2m_bundle = self.hydrate_m2m(bundle)
        self.save_m2m(m2m_bundle)
        return bundle


    def get_list(self, request, **kwargs):
        """Returns serialised list of resources, without the meta crap."""

        objects = self.obj_get_list(request=request, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(
            request.GET, sorted_objects,
            resource_uri=self.get_resource_list_uri(),
            limit=self._meta.limit)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [self.build_bundle(obj=obj, request=request) for obj in to_be_serialized['objects']]
        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        # blat the meta, just return the objects
        to_be_serialized = to_be_serialized['objects']
        return self.create_response(request, to_be_serialized)


class SearchResource(SpineFrontedResource):
    user = fields.ForeignKey(
        'glean.api.resources.UserResource', 'user')

    class Meta:
        queryset = Search.objects.all()
        allowed_methods = ['get', 'put', 'post']
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

class UserResource(ModelResource):
    class Meta:
        list_allowed_methods = ['get']
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = DjangoAuthentication()
        authorization = DjangoAuthorization()

