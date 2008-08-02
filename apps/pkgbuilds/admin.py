
# Admin stuff
from django.contrib import admin
from pkgbuilds.models import Build

class BuildAdmin(admin.ModelAdmin):
    pass

admin.site.register(Build,BuildAdmin)