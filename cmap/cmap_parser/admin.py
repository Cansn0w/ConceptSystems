from django.contrib import admin
from .models import Cmap


@admin.register(Cmap)
class CmapAdmin(admin.ModelAdmin):
    pass
