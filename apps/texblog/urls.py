"""\
URL patterns for the texblog application.

"""

from django.conf.urls.defaults import *

from models import Entry, Category

entries_dict = {
    'queryset' : Entry.live.all(),
    'extra_context' : {'categories': Category.objects.all}
}

urlpatterns = patterns('',
    url('^$','django.views.generic.list_detail.object_list',entries_dict,name='texblog_index'),
    url('^(?P<slug>[-\w]+)/$','django.views.generic.list_detail.object_detail',
        dict(entries_dict,template_object_name='entry'),name='texblog_detail'),
    #url('^category/(?P<category>)/$',xxx,xxx,name='texarticles_category'),
)