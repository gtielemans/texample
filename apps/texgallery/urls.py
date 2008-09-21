from django.conf.urls.defaults import *
from texgallery.models import ExampleEntry, Tag, Feature, Author

from django.conf import settings

latest_dict = {
    'queryset': ExampleEntry.objects.order_by('-created')[:4],
    'extra_context' : {
        'tags' : Tag.objects.all,
        'features' : Feature.objects.all,
        'authors' : Author.objects.all,
        'gallery_url' : settings.MEDIA_URL + 'tikz/examples/',
    },
    #'template_object_name' : 'category',
}

all_dict = {
    'queryset': ExampleEntry.objects.order_by('-created'),
    'extra_context' : {
        'tags' : Tag.objects.all,
        'features' : Feature.objects.all,
        'authors' : Author.objects.all,
        'gallery_url' : settings.MEDIA_URL + 'tikz/examples/',
    },
    #'template_object_name' : 'category',
}

entry_dict = {
    'queryset' : ExampleEntry.objects.all(),
    'extra_context' : {
        'gallery_url' : settings.MEDIA_URL + 'tikz/examples/',
    },
}

tag_dict_base = {
    'extra_context' : {
        'gallery_url' : settings.MEDIA_URL + 'tikz/examples/',
        'tags' : Tag.objects.all,
        'features' : Feature.objects.all,
    }
}

tag_dict = dict(tag_dict_base, queryset =  Tag.objects.all())
feature_dict = dict(tag_dict_base, queryset =  Feature.objects.all())
author_dict = dict(tag_dict_base, queryset =  Author.objects.all())



urlpatterns = patterns('',
    url(r'^$','django.views.generic.list_detail.object_list',
        dict(latest_dict,template_name="texgallery/main.html"),name='texgallery_index'),

    url(r'^feature/(?P<slug>\w[-\w]+)/','django.views.generic.list_detail.object_detail',
        dict(feature_dict, slug_field="slug", template_object_name="tag",
        template_name="texgallery/feature_detail.html"), name='texgallery_feature_detail'),

    url(r'^tag/(?P<slug>\w[-\w]+)/','django.views.generic.list_detail.object_detail',
        dict(tag_dict, slug_field="slug", template_object_name="tag",
        template_name="texgallery/tag_detail.html"), name='texgallery_tag_detail'),
    
    url(r'^all/$','django.views.generic.list_detail.object_list',
        dict(all_dict, 
        template_name="texgallery/examples_all.html"), name='texgallery_all'),
    
    url(r'^author/(?P<slug>\w[-\w]+)/','django.views.generic.list_detail.object_detail',
        dict(author_dict, slug_field="slug", template_object_name="tag",
        template_name="texgallery/author_detail.html"), name='texgallery_author_detail'),

    url(r'(?P<slug>\w[-\w]+)/',
        'django.views.generic.list_detail.object_detail',
        dict(entry_dict, slug_field="slug",template_object_name="entry",
            template_name="texgallery/exgallery_detail.html"),name='texgallery_detail'),
)