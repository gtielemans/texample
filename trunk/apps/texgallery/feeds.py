from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

current_site = Site.objects.get_current()

from texgallery.models import ExampleEntry

class LatestExamples(Feed):
    title = "Latest additions to the TikZ and PGF examples gallery" 
    link = "http://www.texample.net/tikz/examples/"
    description = ""
    def items(self):
        return ExampleEntry.live.all()[:10]
    
    def item_pubdate(self, item):
        return item.created