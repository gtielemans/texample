"""\
URL patterns for the texarticles application.

"""

from django.conf.urls.defaults import *

from models import Article, Category

articles_dict = {
    'queryset' : Article.live.all(),
    'extra_context' : {'categories': Category.objects.all}
}

urlpatterns = patterns('',
    url('^$','django.views.generic.list_detail.object_list',articles_dict,name='texarticles_index'),
    url('^(?P<slug>[-\w]+)/$','django.views.generic.list_detail.object_detail',
        dict(articles_dict,template_object_name='article'),name='texarticles_detail'),
    #url('^category/(?P<category>)/$',xxx,xxx,name='texarticles_category'),
)