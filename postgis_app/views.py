import json
import logging


import folium
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.gis.geos import Polygon

from .models import PolygonsModel

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
# Create your views here.


class AboutView(View):
    """Приветственная страница"""

    def get(self, request):
        content = {}
        return render(request, "postgis_app/about.html", content)


class IndexView(View):
    """Главная страница добавления полигонов"""

    def get(self, request):
        content = {}
        return render(request, "postgis_app/index.html", content)

    def post(self, request):
        logging.info(f"request.POST: {request.POST}")
        send_text = str(request.POST.get("sendText"))
        data_from_json = json.loads(send_text)
        name_polygon = str(request.POST.get("namePolygon"))
        # Список координат для внесения в бд
        result_list = []
        antimeridian = False
        for el in data_from_json:
            # В случае если забыли указать широту или долготу, устанавливаем значение 0
            # Проверка широты
            if len(el[0]) > 0:
                latitude = float(el[0])
            else:
                latitude = float(0)
            # Проверка долготы
            if len(el[1]) > 0:
                longitude = float(el[1])
                # Проверка на антимеридиан
                if longitude > 180:
                    longitude = longitude - 360
                    antimeridian = True
            else:
                longitude = float(0)
            result_list.append((latitude, longitude))
        logging.info(f"result_list: {result_list}")
        # Для построения полигона необходимо 4 точки, а также чтобы 1 и последняя были равного значения
        if len(result_list) == 3 or result_list[0] != result_list[-1]:
            result_list.append(result_list[0])
        polygon = Polygon(result_list)
        new_polygon = PolygonsModel(
            name_of_polygon=name_polygon, polygon=polygon, antimeridian=antimeridian
        )
        new_polygon.save()
        # Возвращаем id записи, для редиректа на стороне клиента
        return HttpResponse(new_polygon.id)


class ShowListPolygonsView(View):
    """Отображения списка всех полигонов хранящихся в бд"""

    def get(self, request):
        polygons = PolygonsModel.objects.get_queryset().order_by("id")
        content = {
            "polygons": polygons,
        }
        return render(request, "postgis_app/all_polygons.html", content)


class ShowOnMapView(View):
    """Отображение полигона на карте"""

    def get(self, request, pk):
        polygon_data = PolygonsModel.objects.get(id=pk)
        # Получение списка координат
        points = polygon_data.polygon[0]
        result_polygon = []
        # Формируем список координат для folium
        for i in range(len(points)):
            result_polygon.append((points.y[i], points.x[i]))

        map_details = folium.Map(location=(0, 0), zoom_start=2)
        folium.PolyLine(result_polygon, color="red", fillcolor="red").add_to(
            map_details
        )
        folium.LayerControl().add_to(map_details)
        map_details = map_details._repr_html_()
        content = {
            "polygon_name": polygon_data.name_of_polygon,
            "polygon_id": polygon_data.id,
            "polygon_antimeridian": polygon_data.antimeridian,
            "map_details": map_details,
        }
        return render(request, "postgis_app/on_map.html", content)

    def post(self, request, pk):
        """Удаление полигона"""
        polygon_data = PolygonsModel.objects.get(id=pk)
        polygon_data.delete()
        return redirect("all-polygons")
