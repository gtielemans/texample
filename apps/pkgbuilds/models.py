from django.db import models
from template_utils.markup import formatter
from django.db.models import permalink

import datetime

class Build(models.Model):
    """
    A model representing a package build

    """

    zip_path = models.CharField(max_length=200,
                                help_text = 'Path to zip archive')
    doc_path = models.CharField(max_length=200,blank=True,
                                help_text = 'Path to documentation')
    build_date = models.DateTimeField(u'Build date', default=datetime.datetime.today)
    slug = models.SlugField(unique_for_date='build_date')


    # The actual entry bits.
    changes = models.TextField(u'Changes',blank=True,
                               help_text="Changes since the previous version. Markdown syntax enabled")
    changes_html = models.TextField(editable=False, blank=True)
    changelog = models.TextField(blank=True)


    class Meta:
        verbose_name_plural = 'Builds'
        ordering = ['-build_date']

    def __unicode__(self):
        return str(self.build_date)

    def save(self):
        self.changes_html = formatter(self.changes or ' ')
        super(Build, self).save()
        
        
    @permalink
    def get_absolute_url(self):
        return ('pkgbuilds_detail', (), { 'year': self.build_date.strftime('%Y'),
                                               'month': self.build_date.strftime('%m'),
                                               'day': self.build_date.strftime('%d'),
                                               'slug': self.slug })
    

