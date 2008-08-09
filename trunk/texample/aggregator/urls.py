"""\
URL configuration for TeXample.net's community section

"""

from django.conf.urls.defaults import *

from texample.aggregator.models import FeedItem

aggregator_info_dict = {
    'queryset': FeedItem.objects.select_related(),
    'paginate_by': 15,
}


urlpatterns = patterns('',
    url('^$','django.views.generic.list_detail.object_list',
        aggregator_info_dict,
        name="aggregator_index"),
)
