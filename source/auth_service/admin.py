from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','email','first_name','last_name','joined_at',)
    list_display_links = ('email',)
