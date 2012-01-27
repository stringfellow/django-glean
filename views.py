# Create your views here.
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils import simplejson as json

from annoying.decorators import render_to
from glean.registry import registry
from glean.forms import SearchForm, GleanerPicker

from glean.models import Search


@render_to('glean/gleaners.html')
def gleaners(request):
    return {'registry': registry}


@render_to('glean/search_create.html')
def search_create(request):
    """Make new search."""
    
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
            search = Search.objects.get_or_create(
                term=data['term'],
                synonyms=data['synonyms'],
                user=request.user)
        else:
            return HttpResponse(
                json.dumps(search_form.errors),
                status=418,
                mimetype="application/json")
        return HttpResponse("OK")
    else:
        search_form = SearchForm()
    return {
        'form': search_form,
    }


@render_to("glean/gleaner_chooser_snippet.html")
def gleaner_chooser(request):
    """Renders the gleaner chooser."""
    form = GleanerPicker()
    return {
        'form': form,
    }


@render_to("glean/gleaner_form_snippet.html")
def gleaner_form(request, gleaner_class):
    """return the gleaner form rendered nicely."""
    try:
        gleaner = registry.find(gleaner_class)
    except AssertionError:
        return HttpResponse("No feed with that class found.", status=404)
    return {
        'form': gleaner.get_form(),
    }
