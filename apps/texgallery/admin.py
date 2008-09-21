
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
    list_filter = ('features','author','tags','technical_areas')

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