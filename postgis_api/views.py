from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from postgis_app.models import PolygonsModel

from . import serializers


class CreatePolygonApiView(CreateAPIView):
    """Создание полигона"""
    serializer_class = serializers.PolygonsSerializer


class ListPolygonsApiView(ListAPIView):
    """Просмотр всех полигонов"""
    queryset = PolygonsModel.objects.all()
    serializer_class = serializers.PolygonsSerializer


class OnePolygonApiGenericView(RetrieveUpdateDestroyAPIView):
    """Редактирование, удаление, просмотр одного полигона"""
    queryset = PolygonsModel.objects.all()
    serializer_class = serializers.PolygonsSerializer
