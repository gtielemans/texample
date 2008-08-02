from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()

from pkgresources.models import Resource

class LatestResources(Feed):
    title = "%s: Latest PGF builds" % current_site.name
    link = "/tikz/resources/"
    description = "sdsdsdf"
    def items(self):
        return Resource.objects.order_by('-pub_date')[:10]