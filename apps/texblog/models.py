"""\
Models for the texblog Django application


"""
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.conf import settings
from django.db.models import permalink

from texarticles.models import CommonArticleInfo
from comment_utils.moderation import CommentModerator, moderator

from texpubutils.utils import publish_parts
from template_utils.markup import formatter
import re

class Category(models.Model):
    description = models.TextField()
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=250)
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return ('texblog_category',(),{'slug':self.slug})
        

class Entry(CommonArticleInfo):
    categories = models.ManyToManyField(Category)
   
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Entries"
    
    def get_media_url(self):
        """Retrun url to entry media"""
        return settings.MEDIA_URL + 'weblog/'+self.slug+'/'
 
    @permalink
    def get_absolute_url(self):
        return ('texblog_entry_detail',(),{ 'year': self.pub_date.strftime('%Y'),
                                            'month': self.pub_date.strftime('%b').lower(),
                                            'day': self.pub_date.strftime('%d'),
                                            'slug': self.slug })
                
class TexblogModerator(CommentModerator):
    akismet = True
    email_notification = True
    enable_field = 'enable_comments'
    
moderator.register(Entry,TexblogModerator)    
