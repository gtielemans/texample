
# Admin stuff
from django.contrib import admin
from models import ExampleEntry,Tag,Feature,Author, TechnicalArea

#try:
#    appname = __name__.split('.')[-2]
#except:
#    appname = 'texgallery'
#
#modu = __import__('%s.models' % appname,{}, {}, [''])#, globals(), locals(), ['Example'],-1)
#admin.site.register(getattr(modu,'Example'))

class ExampleAdmin(admin.ModelAdmin):
    list_display = ('title','created')
    list_filter = ('features','tags','technical_areas','author')
    ordering = ('title',)
    
    def save_model(self, request, obj, form, change):
        # Code for denormalization of entry_count. Initially I wanted to use
        # signals to do this, but the m2m relations are updated by the admin
        # *after* a model has been saved. It is therefore not possible to
        # detect changes in the ExampleEntry's save method or in a signal handler.
        
        # Take a snapshot of the existing tags
        try:
            dbtags = set(obj.tags.all()) | set(obj.features.all()) | \
                    set(obj.technical_areas.all()) | set(obj.author.all())
        except:
            dbtags = set()
        pass
        obj.save()
        # Get the new set of tags
        tags = set(form.cleaned_data['features']) | \
               set(form.cleaned_data['tags']) | \
               set(form.cleaned_data['technical_areas'])| \
               set(form.cleaned_data['author'])
        # I love sets...
        added_tags = tags - dbtags
        removed_tags = dbtags - tags
        # update entry_count
        for tag in added_tags:
            tag.entry_count += 1
            tag.save()
        for tag in removed_tags:
            tag.entry_count -= 1
            tag.save()
        

        

class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}
   
    
    
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name","last_name")}

      
#class ResourceAdmin(admin.ModelAdmin):
#    list_display = ('title','category','pub_date')
#    list_filter = ['category']

admin.site.register(Tag,TagAdmin)
admin.site.register(TechnicalArea,TagAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(ExampleEntry,ExampleAdmin)
admin.site.register(Feature,TagAdmin)
#admin.site.register(Resource,ResourceAdmin)
