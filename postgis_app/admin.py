from django.contrib import admin

from postgis_app.models import PolygonsModel


class PolygonAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['name_of_polygon']


admin.site.register(PolygonsModel, PolygonAdmin)
