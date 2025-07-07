from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('time_create',) 
    prepopulated_fields = {'slug': ("title",)} 

    def get_photo(self,object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ("name",)  
    prepopulated_fields = {'slug': ("name",)} 




admin.site.register(library, LibraryAdmin)  
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)

admin.site.site_header='Адміністрування сайту'
admin.site.site_title= 'Адміністрування сайта'
