from django.contrib import admin

from .models import *

class BlogAdmin(admin.ModelAdmin):
    fieldsets = None
    fields = ['title', 'content']

admin.site.register(Query)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Blog, BlogAdmin)
