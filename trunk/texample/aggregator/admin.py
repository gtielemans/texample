from django.db import models
from django.contrib import admin

from texample.aggregator.models import Feed, FeedItem

class FeedAdmin(admin.ModelAdmin):
    list_display = ["title", "public_url", "is_defunct"]
    list_filter = ["is_defunct"]
    ordering = ["title"]
    search_fields = ["title", "public_url"]
    list_per_page = 500
    
admin.site.register(FeedItem)
admin.site.register(Feed,FeedAdmin)



   