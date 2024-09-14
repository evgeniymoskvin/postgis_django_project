import folium
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.gis.geos import Polygon, Point

from .models import PolygonsModel


# Create your views here.
class IndexView(View):
    def get(self, request):
        all_data = PolygonsModel.objects.get_queryset()
        for data_polygons in all_data:
            print(data_polygons.polygon)
        content = {'all_data': all_data}
        return render(request, 'postgis_app/index.html', content)

    def post(self, request):
        print(f'request.POST: {request.POST}')
        send_text = str(request.POST.get('sendText'))
        name_polygon = str(request.POST.get('namePolygon'))
        send_text_list = send_text.split(' ')
        result_list = []
        print(send_text_list)
        antimeridian = False
        for el in send_text_list:
            # Избавляемся от элементов с длиной 0
            if len(el) > 0:
                coordinates = el[1:-1].split(',')
                print(f'coordinates: {coordinates}')
                # Проверяем широту
                if len(coordinates[0]) > 0:
                    latitude = float(coordinates[0])
                else:
                    latitude = float(0)
                # Проверяем долготу
                if len(coordinates[1]) > 0:
                    longitude = float(coordinates[1])
                    # Проверяем антимеридиан
                    if longitude > 180:
                        longitude = longitude - 360
                        antimeridian = True
                else:
                    longitude = float(0)
                result_list.append((latitude, longitude))
        print(result_list)
        if result_list[0] != result_list[-1]:
            result_list.append(result_list[0])
        polygon = Polygon(result_list)
        new_polygon = PolygonsModel(name_of_polygon=name_polygon, polygon=polygon, antimeridian=antimeridian)
        new_polygon.save()
        # Перенаправляем на страницу с созданным полигоном
        return redirect('map', pk=new_polygon.id)


class ShowListPolygonsView(View):
    """Отображения списка всех полигонов в бд"""

    def get(self, request):
        polygons = PolygonsModel.objects.get_queryset()
        content = {
            'polygons': polygons,
        }
        return render(request, 'postgis_app/all_polygons.html', content)


class ShowOnMapView(View):
    """Отображение полигона на карте"""

    def get(self, request, pk):
        polygon_data = PolygonsModel.objects.get(id=pk)
        print(polygon_data.polygon)
        points = polygon_data.polygon[0]
        result_polygon = []

        for i in range(len(points)):
            result_polygon.append((points.y[i], points.x[i]))
        print(result_polygon)

        map_details = folium.Map(location=(0, 0), zoom_start=2)
        folium.PolyLine(result_polygon, color='red').add_to(map_details)
        folium.LayerControl().add_to(map_details)
        map_details = map_details._repr_html_()
        content = {
            'polygon_name': polygon_data.name_of_polygon,
            'polygon_antimeridian': polygon_data.antimeridian,
            'map_details': map_details
        }
        return render(request, 'postgis_app/on_map.html', content)
