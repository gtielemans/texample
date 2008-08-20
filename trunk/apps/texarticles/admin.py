
# Admin stuff
from django.contrib import admin
from models import Category, Article
      
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_date')
    list_filter = ['category']

class ArticleAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("css/admin_styles.css",)
        }

    fieldsets = (
        ('Meta',{'fields': ('title','slug','pub_date','updated_date',
                            'author','status','featured','enable_comments',
                            'categories','tags'),
            }
        ),
        ('Content',{'fields': ('markup','abstract','body'),
            'classes' :('fixedwidth',)}),
        ('Advanced',{'fields':('abstract_html','body_html'),
            'classes': ('collapse','fixedwidth')})
    )

admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
