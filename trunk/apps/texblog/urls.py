"""\
URL patterns for the texblog application.

"""

from django.conf.urls.defaults import *
from django.views.generic import date_based

from models import Entry, Category

entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
    }

entry_info_dict_all = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
    }


#
#urlpatterns = patterns('',
#    url('^$','django.views.generic.list_detail.object_list',entries_dict,name='texblog_index'),
#    url('^(?P<slug>[-\w]+)/$','django.views.generic.list_detail.object_detail',
#        dict(entries_dict,template_object_name='entry'),name='texblog_detail'),
#    #url('^category/(?P<category>)/$',xxx,xxx,name='texarticles_category'),
#)

urlpatterns = patterns('',
    url(r'^$',
        date_based.archive_index,
        entry_info_dict,
        name='texblog_entry_archive_index'),
    url(r'^(?P<year>\d{4})/$',
        date_based.archive_year,
        dict(entry_info_dict, make_object_list=True),
        name='texblog_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        date_based.archive_month,
        entry_info_dict,
        name='texblog_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        date_based.object_detail,
        dict(entry_info_dict_all, template_object_name = 'entry',slug_field='slug'),
        name='texblog_entry_detail'),
)
