"""\
URL configuration for TeXample.net's tools section

"""

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^$','django.views.generic.simple.direct_to_template',
        {'template': 'tools/tools_index.html'},
        name="tools_index"),
    # blend2sketch
    url('^blend2sketch/$','django.views.generic.simple.direct_to_template',
        {'template': 'tools/blend2sketch/blend2sketch_index.html'},
        name="blend2sketch_index"),
     url('^blend2tikz/doc/$','django.views.generic.simple.direct_to_template',
        {'template': 'tools/blend2sketch/blend2sketch_doc.html'},
        name="blend2sketch_doc"),
    # blend2tikz
    url('^blend2tikz/$','django.views.generic.simple.direct_to_template',
        {'template': 'tools/blend2tikz/blend2tikz_index.html'},
        name="blend2tikz_index"),
     url('^blend2tikz/doc/$','django.views.generic.simple.direct_to_template',
        {'template': 'tools/blend2tikz/blend2tikz_doc.html'},
        name="blend2tikz_doc"),
    #url(r'^blend2tikz/', include('pkgresources.urls')),
    
    
)
