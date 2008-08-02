from django.conf.urls.defaults import *
from pkgbuilds.models import Build

from django.views.generic import date_based

builds_dict = {
    'queryset': Build.objects.all(),
    'template_object_name' : 'build',
    'date_field' : 'build_date',
}


urlpatterns = patterns('',
    url(r'^$',
        date_based.archive_index,
        dict(builds_dict, template_object_name="builds",num_latest=100),
        name='pkgbuilds_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        date_based.object_detail,
        dict(builds_dict, slug_field='slug', month_format=r"%m"),
        name='pkgbuilds_detail'),
)