from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()

from pkgbuilds.models import Build

class LatestBuilds(Feed):
    title = "%s: Latest PGF builds" % current_site.name
    link = "/tikz/builds/"
    description = "Updates on changes and additions to chicagocrime.org."
    def items(self):
        return Build.objects.all()[:5]