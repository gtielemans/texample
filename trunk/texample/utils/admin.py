"""Add batchadmin to contrib.comments admin page"""

from django.contrib import admin
from django.conf import settings
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _

from batchadmin.admin import BatchModelAdmin,CHECKBOX_NAME

# Copied from contrib.comments
class CommentsAdmin(BatchModelAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
     )

    list_display = ('name', 'content_type', 'object_pk', 'ip_address', 'submit_date', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed')
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)
    search_fields = ('comment', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')
    
    batch_actions = ['delete_selected','disable_public','enable_public']
    
    def disable_public(self, request,changelist):
        selected = request.POST.getlist(CHECKBOX_NAME)
        objects = changelist.get_query_set().filter(pk__in=selected)
        for obj in objects:
            obj.is_public = False
            obj.save()
        self.message_user(request, "Comments set non-public.")

    def enable_public(self, request,changelist):
        selected = request.POST.getlist(CHECKBOX_NAME)
        objects = changelist.get_query_set().filter(pk__in=selected)
        for obj in objects:
            obj.is_public = True
            obj.save()
        self.message_user(request, "Comments set public.")


# Unregister the default admin object first
admin.site.unregister(Comment)
admin.site.register(Comment, CommentsAdmin)
