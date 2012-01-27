#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""The connector registry.

A lot like admin, this contains a Register class (like AdminSite) that loads
and stores the registered connectors.

"""
import os
import sys
import pkgutil
import inspect
import logging

from django.utils.importlib import import_module


log = logging.getLogger(__name__)

class Registry(object):
    """A class for registering connectors to.

    This should be used to prevent random code-loading and for pre-load
    importing.

    """

    def __init__(self):
        self._register = {}

    def register_by_qualified_name(self, name):
        """Add the gleaner by name, if it isn't already there."""
        if name in self._register:
            return
        path = name.split('.')
        module_name = ".".join(path[:-1])
        class_name = path[-1]
        # import the module if needed
        if module_name not in sys.modules:
            __import__(module_name)
        module = sys.modules[module_name]
        assert class_name in module.__dict__, \
            "Gleaner '%s' not found in module: %s" % (name, module.__name__)
        gleaner_class = module.__dict__[class_name]
        self._register[name] = gleaner_class

    def _add_classes(self, app_name, glean_noun, modnm=None):
        """Add the module's classes to the registry."""
        from glean.models import GleanerBase
        gleaner_path = ".".join([app_name, glean_noun])
        if modnm:  # if the gleaners is a 'package' then there'll be modnm too
            gleaner_path = gleaner_path + "." + modnm
        gleaner_module = import_module(gleaner_path)
        for name, obj in inspect.getmembers(gleaner_module):
            if (inspect.isclass(obj) and  # check it's a class
                issubclass(obj, GleanerBase) and
                obj.__module__ == gleaner_path):  # and from this module
                # the name as it appears in the import tag:
                fully_qualified_gleaner = ".".join([gleaner_path, name])
                # add it to the registry
                self._register.setdefault(fully_qualified_gleaner, obj)

    def register(self, app_name, glean_noun='gleaners'):
        """Try and add this app's gleaners to the registry."""
        package = __import__(app_name)
        for _, modnm1, ispkg1 in pkgutil.iter_modules(package.__path__):
            if modnm1 == glean_noun:  # see if the gleaners module exists
                if ispkg1:  # if it is a package, then descend in...
                    for _, modnm2, ispkg2 in pkgutil.iter_modules([
                    os.path.join(package.__path__[0], glean_noun)]):
                        self._add_classes(app_name, glean_noun, modnm2)
                else:  # its just a gleaners.py file.
                    self._add_classes(app_name, glean_noun)

    def register_main(self, app_name):
        """Try and add this app's gleaners to the registry."""
        package = __import__(app_name)
        for _, modnm1, ispkg1 in pkgutil.iter_modules(package.__path__):
            self._add_classes(app_name, modnm1)

    def gleaners_by_app(self):
        """Return an app->[gleaners] dict."""
        apps = {}
        for cls, gleaner in self._register.items():
            app = cls.split('.')[0]
            apps.setdefault(app, []).append(gleaner)
        return apps

    def find(self, classname):
        """Return a registered gleaner or register and return by classname."""
        if classname in self._register:
            return self._register[classname]
        else:
            self.register_by_qualified_name(classname)
            assert classname in self._register
            return self._register[classname]

    def items(self):
        return self._register.items()

    def keys(self):
        return self._register.keys()

    def choices(self):
        return [
            (k, v.__name__)
            for k, v in self.items()]

    def is_empty(self):
        return len(self._register.keys()) == 0


# This global object will hold all registered gleaners.
registry = Registry()


def autodiscover(glean_noun='gleaners'):
    """Like admin's autodiscover.

    gleaners is the name of the module containing connectors.

    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's gleaners module.
        try:
            before_import_register = copy.copy(registry._register)
            registry.register(app, glean_noun)
        except Exception, e:
            print e
            log.error(e)
            registry._register = before_import_register

            # Decide whether to bubble up this error. If the app just
            # doesn't have a gleaners module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, glean_noun):
                raise e
    print "Registered %s gleaners" % len(registry.keys())
