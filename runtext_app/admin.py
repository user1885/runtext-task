from django.contrib import admin
from django.utils.html import format_html
from . import models

# Register your models here.

@admin.register(models.UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    def video_preview(self, obj):
        return format_html(
            '''<video src="{}" controls></video>''', 
            obj.video.url)
    
    video_preview.short_description = 'Video preview'

    list_display = ('text', 'date')
    readonly_fields = ('video_preview',)
    fields = ('text', 'video', 'video_preview', 'date')