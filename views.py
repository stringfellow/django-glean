# Create your views here.
from django.views.generic import TemplateView

from annoying.decorators import render_to
from glean.registry import registry


@render_to('glean/gleaners.html')
def gleaners(request):
    return {'registry': registry}



