"""\
URL configuration for TeXample.net's TikZ section

"""

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^$','django.views.generic.simple.direct_to_template',
        {'template': 'tikz/tikz_index.html'},
        name="tikz_index"),
    
    url(r'^resources/', include('pkgresources.urls')),
    url(r'^builds/', include('pkgbuilds.urls')),
    url(r'^examples/', include('texgallery.urls')),
    url(r'^about/', 'django.views.generic.simple.direct_to_template',
        {'template': 'tikz/tikz_about.html'},
        name="tikz_about"),
    
)
