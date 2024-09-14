from django.shortcuts import render
from django.views import View
from django.contrib.gis.geos import Polygon

from .models import PolygonsModel


# Create your views here.
class IndexView(View):
    def get(self, request):
        all_data = PolygonsModel.objects.get_queryset()
        for data_polygons in all_data:
            print(data_polygons.polygon)
        content = {}
        return render(request, 'postgis_app/index.html', content)

class AddNewPolygon(View):
    def get(self, request):
        polygon = Polygon(((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)))
        new_polygon = PolygonsModel(name_of_polygon="тест загрузки", polygon=polygon)
        new_polygon.save()
        content = {

        }
        return render(request, 'postgis_app/index.html', content)
