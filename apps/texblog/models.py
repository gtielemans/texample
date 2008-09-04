"""\
Models for the texblog Django application


"""
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.conf import settings
from django.db.models import permalink


from texpubutils.utils import publish_parts
from template_utils.markup import formatter
import re

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager,self).get_query_set().filter(status=self.model.LIVE_STATUS)

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
        

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS,'Live'),
        (DRAFT_STATUS,'Draft'),
        (HIDDEN_STATUS,'Hidden'),
        
    )
    REST_MARKUP = 'restructuredtext'
    MARKDOWN_MARKUP = 'markdown'
    RAW_MARKUP = 'raw'
    NO_MARKUP = 'nomarkup'
    MARKUP_CHOICES = (
        (REST_MARKUP,'ReStructuredText'),
        (MARKDOWN_MARKUP,'Markdown'),
        (RAW_MARKUP,'Raw/HTML'),
        (NO_MARKUP,'Ignore')
    )
    title = models.CharField(max_length=250)
    abstract = models.TextField(blank = True,help_text="Optional summary of the entry")
    slug = models.SlugField(unique=True)
    
    body = models.TextField(help_text="Content is transformed to HTML when saved unless Markup is set to 'Ignore'")
    
    pub_date = models.DateField('Published')
    updated_date = models.DateField('Updated',blank=True,null=True)
    
    author = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS_CHOICES,default=LIVE_STATUS)
    markup = models.CharField(max_length=100,choices=MARKUP_CHOICES,default=MARKDOWN_MARKUP)
    
    featured = models.BooleanField(default=False)
    enable_comments = models.BooleanField(default=True)
    
    categories = models.ManyToManyField(Category)
    tags = TagField()
    
    # html version
    body_html = models.TextField(blank=True)
    abstract_html = models.TextField(blank=True)
    #toc = models.TextField(blank=True,help_text="Table of contents. Usually autogenerated")
    extra_content = models.TextField(blank=True)
    
    # Managers
    live = LiveEntryManager()
    objects = models.Manager()
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Entries"
    
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('texblog_detail',(),{'slug':self.slug})
                
    def save(self, force_insert=False, force_update=False):
        if self.markup <> self.NO_MARKUP:
            if self.markup == self.RAW_MARKUP:
                markup_formatter = None
            else:
                markup_formatter = self.markup
           
            media_url = settings.MEDIA_URL + self.get_absolute_url()[1:]
           
        
            parts = publish_parts(self.body,markup_formatter,media_url=media_url)
            #self.toc = parts['toc']
            if self.abstract:
                self.abstract_html = formatter(self.abstract,filter_name=markup_formatter,
                                **settings.MARKUP_SETTINGS[markup_formatter])
            else:
                if parts['summary']:
                    self.abstract_html = parts['summary']
            self.body_html = parts['body']
            
        super(Entry,self).save()
