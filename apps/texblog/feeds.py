from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

import datetime
current_site = Site.objects.get_current()

from texblog.models import Entry

class LatestWeblogEntries(Feed):
    title = "%s Weblog" % current_site.name
    link = "http://www.texamle.net/weblog/"
    description = "sdfsdsdf"
    
    def items(self):
        return Entry.live.all()[:10]
    
    def item_pubdate(self, item):
        t = list(item.pub_date.timetuple()[:6])
        # Set hour. 
        t[3] = 12
        
        return datetime.datetime(*t)
    
    def item_categories(self, item):
        """
        Takes the object returned by get_object() and returns the feed's
        categories as iterable over strings.
        """
        if item:
            return [c.title for c in item.categories.all()]
        else:
            return ['']

    

    
    
