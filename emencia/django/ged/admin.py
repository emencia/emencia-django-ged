"""Admin for emencia.django.ged"""
from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.defaultfilters import slugify

from emencia.django.ged.models import Path
from emencia.django.ged.models import Document

class PathAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('name', '__unicode__', 'creator', 'creation_date')
    fields = ('parent', 'name')
    search_fields = ('name', 'slug')
    list_filter = ('creation_date',)

    def save_model(self, request, path, form, change):
        user = request.user
        try:
            e = path.creator
        except:
            path.creator = user
            path.slug = slugify(path.name)
        path.save()

admin.site.register(Path, PathAdmin)

class DocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('name', 'slug', 'path', 'status',
                    'creator', 'creation_date', 'modifier', 'modification_date')
    search_fields = ('name', 'slug')
    list_filter = ('status', 'path', 'creation_date', 'modification_date')
    fieldsets = ((None, {'fields': ('name', 'description', 'document')}),
                 (None, {'fields': ('language', 'tags', 'path', 'status')}),
                 )

    def save_model(self, request, document, form, change):
        user = request.user
        try:
            e = document.creator
        except:
            document.creator = user
            document.slug = slugify(document.name)
        document.modifier = user
        
        document.save()

admin.site.register(Document, DocumentAdmin)
