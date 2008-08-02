from django.conf.urls.defaults import *
from pkgresources.models import Resource, Category


categories_dict = {
    'queryset': Category.objects.all(),
    'extra_context' : {
        'resources' : Resource.objects.order_by('-pub_date'),
    },
    'template_object_name' : 'category',
}

resource_dict = {
    'queryset' : Resource.objects.all(),
    'template_object_name' : 'resource',
}

urlpatterns = patterns('',
    url(r'^$','django.views.generic.list_detail.object_list',
        dict(categories_dict),name='pkgresources_index'),
    url(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
        resource_dict, name='pkgresources_detail'),
    
)