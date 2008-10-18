from django.conf.urls.defaults import *
from texgallery.models import ExampleEntry, Tag, Feature, Author,TechnicalArea

from django.conf import settings

latest_dict = {
    'queryset': ExampleEntry.live.order_by('-created')[:4],
    'extra_context' : {
        'tags' : Tag.objects.all,
        'features' : Feature.objects.all,
        'authors' : Author.objects.all,
        'technical_areas' : TechnicalArea.objects.all,
        'gallery_url' : settings.MEDIA_URL + 'tikz/examples/',
    },
    #'template_object_name' : 'category',
}

all_dict_alpha = {
    'queryset': ExampleEntry.live.order_by('title'),
    'paginate_by': 18,
    'extra_context' : {
        'tags' : Tag.objects.all,
        'features' : Feature.objects.all,
        'authors' : Author.objects.all,
        'technical_areas' : TechnicalArea.objects.all,
        'gallery_url' : settings.MEDIA_URL + 'tikz/examples/',
    },
    #'template_object_name' : 'category',
}

all_dict_date = {
    'queryset': ExampleEntry.live.order_by('-created'),
    'paginate_by': 18,
    'extra_context' : {
        'tags' : Tag.objects.all,
        'features' : Feature.objects.all,
        'authors' : Author.objects.all,
        'technical_areas' : TechnicalArea.objects.all,
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
        'technical_areas' : TechnicalArea.objects.all,
        
    }
}

tag_dict = dict(tag_dict_base, queryset =  Tag.objects.all())
feature_dict = dict(tag_dict_base, queryset =  Feature.objects.all())
author_dict = dict(tag_dict_base, queryset =  Author.objects.all())
area_dict = dict(tag_dict_base, queryset =  TechnicalArea.objects.all())



urlpatterns = patterns('',
    url(r'^$','django.views.generic.list_detail.object_list',
        dict(latest_dict,template_name="texgallery/texgallery_main.html"),name='texgallery_index'),

    url(r'^feature/(?P<slug>\w[-\w]+)/$','django.views.generic.list_detail.object_detail',
        dict(feature_dict, slug_field="slug", template_object_name="tag",
        template_name="texgallery/texgallery_feature_detail.html"), name='texgallery_feature_detail'),

    url(r'^tag/(?P<slug>\w[-\w]+)/$','django.views.generic.list_detail.object_detail',
        dict(tag_dict, slug_field="slug", template_object_name="tag",
        template_name="texgallery/texgallery_tag_detail.html"), name='texgallery_tag_detail'),
    
    url(r'^area/(?P<slug>\w[-\w]+)/$','django.views.generic.list_detail.object_detail',
        dict(area_dict, slug_field="slug", template_object_name="tag",
        template_name="texgallery/texgallery_area_detail.html"), name='texgallery_area_detail'),
    
    url(r'^all/$','django.views.generic.list_detail.object_list',
        dict(all_dict_alpha, 
        template_name="texgallery/texgallery_examples_all.html"), name='texgallery_all_alpha'),
    url(r'^all/date/$','django.views.generic.list_detail.object_list',
        dict(all_dict_date, 
        template_name="texgallery/texgallery_examples_all.html"), name='texgallery_all_date'),
    url(r'^all/list/$','django.views.generic.list_detail.object_list',
        dict(all_dict_alpha, paginate_by=1000,
        template_name="texgallery/texgallery_examples_list.html"), name='texgallery_all_list'),
    
    url(r'^author/(?P<slug>\w[-\w]+)/','django.views.generic.list_detail.object_detail',
        dict(author_dict, slug_field="slug", template_object_name="tag",
        template_name="texgallery/texgallery_author_detail.html"), name='texgallery_author_detail'),
    
    url(r'^about/$','django.views.generic.simple.direct_to_template',
        {'template': 'texgallery/texgallery_about.html'},name='texgallery_about'),
    url(r'^contribute/$','django.views.generic.simple.direct_to_template',
        {'template': 'texgallery/texgallery_contribute.html'},name='texgallery_contribute'),

    url(r'(?P<slug>\w[-\w]+)/',
        'django.views.generic.list_detail.object_detail',
        dict(entry_dict, slug_field="slug",template_object_name="entry",
            template_name="texgallery/texgallery_detail.html"),name='texgallery_detail'),
    
)