"""Models for the TikZ and PGF examples gallery"""
from django.db import models
import datetime

class CommonTagInfo(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True,help_text="Optional")

    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ("title",)
        abstract = True


class Tag(CommonTagInfo):
    
    def get_absolute_url(self):
        return u"/pgftikzexamples/tag/%s/" % (self.slug)

class Feature(CommonTagInfo):
    """A specific feature used by an example"""
    
    def get_absolute_url(self):
        return u"/pgftikzexamples/tag/%s/" % (self.slug)


class TechnicalArea(CommonTagInfo):
    """A technical area that an example belongs to"""
    
    def get_absolute_url(self):
        return u"/area/tag/%s/" % (self.slug)


class Author(models.Model):
    first_name = models.CharField(max_length=60,blank=True)
    last_name = models.CharField(max_length=60,blank=True)
    url = models.URLField(verify_exists=False,blank=True)
    email = models.EmailField(blank=True)
    
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
        
    def get_absolute_url(self):
        return u"/pgftikzexamples/%s/" % (self.slug)


    def __unicode__(self):
        return self.title
    
