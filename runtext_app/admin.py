from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('text', 'file_name', 'date')
