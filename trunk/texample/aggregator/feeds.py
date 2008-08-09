from django.contrib.syndication.feeds import Feed
from texample.aggregator.models import FeedItem

class CommunityAggregatorFeed(Feed):
    title = "The TeX community aggregator"
    link = "http://www.texample.net/community/"
    description = "Aggregated feeds from the TeX community."

    def items(self):
        return FeedItem.objects.all()[:50]
