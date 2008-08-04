from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()

from pkgresources.models import Resource

class LatestResources(Feed):
    title = "%s: Latest TikZ and PGF resources" % current_site.name
    link = "/tikz/resources/"
    description = "A growing collection of links to various TikZ and PGF resources."
    def items(self):
        return Resource.objects.order_by('-pub_date')[:10]