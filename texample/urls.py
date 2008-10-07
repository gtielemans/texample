"""\
Main URL configuration for TeXample.net

"""

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^tikz/', include('texample.tikz.urls')),
    (r'^articles/', include('texarticles.urls')),
    (r'^weblog/', include('texblog.urls')),
    (r'^contact/', include('contact_form.urls')),
    (r'^community/', include('texample.aggregator.urls')),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    (r'^admin/(.*)', admin.site.root),    
)

### Feed configuration

# TikZ section
from pkgbuilds.feeds import LatestBuilds
from pkgresources.feeds import LatestResources

tikz_feed_dict = {'feed_dict' : {
    'builds' : LatestBuilds,
    'resources' : LatestResources,    
    'examples' : None}
}

from texample.aggregator.feeds import CommunityAggregatorFeed
feed_dict = {'feed_dict' : {
    'community' : CommunityAggregatorFeed,
    }
}


# TODO:
# weblog section
# beamer section

urlpatterns += patterns('',
    url(r'^feeds/tikz/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        tikz_feed_dict, name = 'tikz_feeds'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        feed_dict, name = 'top_feeds'),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)