
# Admin stuff
from django.contrib import admin
from models import Category, Resource
      
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_date')
    list_filter = ['category']

admin.site.register(Category)
admin.site.register(Resource,ResourceAdmin)
