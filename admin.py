from django.contrib import admin

from gallery.models import Photo, PhotoSet
from sorl.thumbnail.admin import AdminImageMixin


class PhotoAdmin(AdminImageMixin, admin.TabularInline):
    model = Photo


class PhotoSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    inlines = (PhotoAdmin,)
    list_display = ('__unicode__', 'sort_order',)

admin.site.register(PhotoSet, PhotoSetAdmin)
