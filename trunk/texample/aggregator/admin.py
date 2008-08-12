from django.db import models
from django.contrib import admin

from texample.aggregator.models import Feed, FeedItem

class FeedAdmin(admin.ModelAdmin):
    list_display = ["title", "public_url", "is_defunct"]
    list_filter = ["is_defunct"]
    ordering = ["title"]
    search_fields = ["title", "public_url"]
    list_per_page = 500

class FeedItemAdmin(admin.ModelAdmin):
    list_display = ["title", "feed", "date_modified"]
    list_filter = ["feed"]
    ordering = ["date_modified"]
    list_per_page = 500
    
admin.site.register(FeedItem,FeedItemAdmin)
admin.site.register(Feed,FeedAdmin)



   