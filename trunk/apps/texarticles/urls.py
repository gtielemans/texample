"""\
URL patterns for the texarticles application.

"""

from django.conf.urls.defaults import *

urlpatters = patterns('',
    url('^$',xxx,xxx,name='texarticles_index'),
    url('^(?P<slug>\d+)/$',xxx,xxx,name='texarticles_detail'),
    url('^category/(?P<category>)/$',xxx,xxx,name='texarticles_category'),
)