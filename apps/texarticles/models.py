"""\
Models for the texarticles Django application

The texarticles app is intended to provide a simple way to publish articles.
An article is slightly different from a typical blog post. It is typically
longer and is not as much tied to a pulication date.

"""
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.conf import settings

import fnetrest

from template_utils.markup import formatter
# Create your models here.

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
        return ('texarticles_category',(),{'slug':self.slug})
        

class Article(models.Model):
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
    abstract = models.TextField(blank = True,help_text="Optional summary of the article")
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
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Articles"
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return ('texarticles_category',(),{'slug':self.slug})
                
    def save(self):
        # convert body to html
        # extract toc
        # convert links
        if self.markup <> self.NO_MARKUP:
            if self.markup == self.RAW_MARKUP:
                markup_formatter = None
            else:
                markup_formatter = self.markup
            self.body_html = formatter(self.body,filter_name=markup_formatter,
                                **settings.MARKUP_SETTINGS[markup_formatter])
                
        super(Article,self).save()
