
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
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ('Meta',{'fields': ('title','slug','pub_date','updated_date',
                            'author','draft','featured','enable_comments',
                            ),
            }
        ),
        ('Categorization',{'fields': ('categories','tags')}),
        # Add a fixedwidth style class to the following fieldsets. Gives
        # us a hook for styling the textarea form elements
        ('Content',{'fields': ('markup','abstract','body'),
            'classes' :('fixedwidth',)}),
        ('Advanced',{'fields':('abstract_html','body_html','toc','extra_content'),
            'classes': ('collapse','fixedwidth')})
    )

admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
