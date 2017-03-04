from django.contrib import admin

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    """
    Photo for admin
    """

    list_display = ["title", "description", "preview", ]


admin.site.register(Photo, PhotoAdmin)
