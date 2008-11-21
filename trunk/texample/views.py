from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext


def search(request):    
    mutable_get = request.GET.copy()
    if 'cof' in mutable_get:
        del mutable_get['cof']
    
    return render_to_response('search.html', RequestContext(request, {
        'query': request.GET.get('q'),
        'query_string': mutable_get.urlencode(),
    }))

