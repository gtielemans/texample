"""Models for the TikZ and PGF examples gallery"""
from django.db import models
import datetime
from template_utils.markup import formatter
from django.db.models import permalink
from comment_utils.moderation import CommentModerator, moderator

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager,self).get_query_set().filter(is_live=True)

class CommonTagInfo(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True,help_text="Optional")
    description_html = models.TextField(blank=True)
    # Denormalization field to store number of entries assigned to the tag.
    entry_count = models.IntegerField(blank=True,null=True,default=0)

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.description_html = formatter(self.description)
        #if self.exampleentry_set:
        #    self.entry_count= self.exampleentry_set.count()
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
    # Denormalization field to store number of entries assigned to the author.
    entry_count = models.IntegerField(blank=True,default=0)
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
    updated = models.DateTimeField(editable=False,blank=True,null=True)
    description = models.TextField(blank=True,
        help_text="Use raw HTML")
    content = models.TextField(blank=True,
        help_text="Use raw HTML")
    epilog = models.TextField(blank=True,
        help_text="Use raw HTML")
    
    enable_comments = models.NullBooleanField(default=True,null=True)
    is_live = models.BooleanField(default=False)
    author = models.ManyToManyField(Author, blank=True)
    is_zipped = models.BooleanField(default=False)
    # Categorization
    features = models.ManyToManyField(Feature, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    technical_areas = models.ManyToManyField(TechnicalArea, blank=True)
    
    # Managers
    objects = models.Manager()
    live = LiveEntryManager()
    
    
    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Example entries"
    
    #def save(self, force_insert=False, force_update=False):
    #    
    #    ll = self.features.all()
    #    print "savepre", ll
    ##    if not self.id:
    ##        #self.created = datetime.datetime.now()
    ##        pass
    ##    else:
    ##        pass
    ##
    ##    #self.updated = datetime.datetime.now()
    #    super(ExampleEntry, self).save(force_insert, force_update)
    #    in_db = ExampleEntry.objects.filter(id=self.id)[0]
    #    
    #    print "savepost", [e for e in in_db.features.all()]
    #    
    @permalink    
    def get_absolute_url(self):
        return ('texgallery_detail',(),{'slug':self.slug})


    def __unicode__(self):
        return self.title
    


class TexgalleryModerator(CommentModerator):
    akismet = True
    email_notification = True
    enable_field = 'enable_comments'
    
moderator.register(ExampleEntry,TexgalleryModerator)    
    


#def denormalize_entries(sender, instance, created=False, **kwargs):
#    """"""
#    if created:
#        #self.created = datetime.datetime.now()
#        dbtags = set()
#        print "created"
#        pass
#    else:
#        in_db = ExampleEntry.objects.get(pk=instance.id)
#        dbtags = set(in_db.tags.all()) | set(in_db.features.all()) | \
#                    set(in_db.technical_areas.all()) | set(in_db.author.all())
#        
#    tags = set(instance.tags.all()) | set(instance.features.all()) | \
#                set(instance.technical_areas.all()) | set(instance.author.all())
#    print "*********\n"
#    print "instance",kwargs['raw']
#    print "tags", tags
#    print "dbtags", dbtags
#    new_tags = tags & dbtags
#    removed_tags = dbtags - tags
#    print "New tags",new_tags
#    print "Removed_tags",removed_tags 

#models.signals.pre_save.connect(denormalize_entries, sender=ExampleEntry)
#models.signals.post_save.connect(denormalize_entries, sender=ExampleEntry)
#models.signals.post_delete.connect(denormalize_votes, sender=ExampleEntry)

