from django.db import models
from template_utils.markup import formatter
from django.db.models import permalink

import datetime

# Create your models here.

class Category(models.Model):
    """
    A category that a Resource can belong to.

    """
    title = models.CharField(max_length=250,core=True)
    description = models.TextField(help_text=u'A short description of the category, to be used in list pages.',blank=True)
    description_html = models.TextField(editable=False, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def save(self):
        self.description_html = formatter(self.description)
        super(Category, self).save()


class Resource(models.Model):
    """
    A resource
    """

    title = models.CharField(max_length=250,core=True)
    url = models.URLField(verify_exists=False)
    pub_date = models.DateTimeField(u'Date posted', default=datetime.datetime.today)

    # The actual entry bits.
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)

    # Categorization.
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = 'Resources'
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def save(self):
        self.description_html = formatter(self.description)
        super(Resource, self).save()
    
    @permalink    
    def get_absolute_url(self):
        return ('pkgresources_detail',(),{'object_id':self.id})
 
