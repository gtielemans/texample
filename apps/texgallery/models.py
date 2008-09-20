"""Models for the TikZ and PGF examples gallery"""
from django.db import models
import datetime
from template_utils.markup import formatter
from django.db.models import permalink

class CommonTagInfo(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True,help_text="Optional")
    description_html = models.TextField(blank=True)

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.description_html = formatter(self.description)
        super(CommonTagInfo, self).save()
    
    class Meta:
        ordering = ("title",)
        abstract = True


class Tag(CommonTagInfo):
    
    @permalink    
    def get_absolute_url(self):
        return ('texgallery_tag_detail',(),{'slug':self.slug})
    
class Feature(CommonTagInfo):
    """A specific feature used by an example"""
    
    @permalink    
    def get_absolute_url(self):
        return ('texgallery_feature_detail',(),{'slug':self.slug})


class TechnicalArea(CommonTagInfo):
    """A technical area that an example belongs to"""
    
    @permalink    
    def get_absolute_url(self):
        return ('texgallery_area_detail',(),{'slug':self.slug})


class Author(models.Model):
    first_name = models.CharField(max_length=60,blank=True)
    last_name = models.CharField(max_length=60,blank=True)
    url = models.URLField(verify_exists=False,blank=True)
    email = models.EmailField(blank=True)
    slug = models.SlugField()
    class Meta:
        ordering = ('last_name',)
    
    def _get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    full_name = property(_get_full_name)

    @permalink    
    def get_absolute_url(self):
        return ('texgallery_author_detail',(),{'slug':self.slug})
    
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    
    
class ExampleEntry(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(editable=False)
    description = models.TextField(blank=True,
        help_text="Use raw HTML")
    content = models.TextField(blank=True,
        help_text="Use raw HTML")
    epilog = models.TextField(blank=True,
        help_text="Use raw HTML")
    
    enable_comments = models.BooleanField(default=True,null=True)
    author = models.ManyToManyField(Author, blank=True)
    # Categorization
    features = models.ManyToManyField(Feature, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    technical_areas = models.ManyToManyField(TechnicalArea, blank=True)
    
    class Meta:
        ordering = ("title",)
        verbose_name_plural = "Example entries"
    
    #def save(self, force_insert=False, force_update=False):
    #    if not self.id:
    #        self.created = datetime.datetime.now()
    #    self.updated = datetime.datetime.now()
    #    super(ExampleEntry, self).save()
        
    @permalink    
    def get_absolute_url(self):
        return ('texgallery_detail',(),{'slug':self.slug})


    def __unicode__(self):
        return self.title
    
