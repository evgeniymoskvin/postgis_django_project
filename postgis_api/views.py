from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from postgis_app.models import PolygonsModel

from . import serializers


class CreatePolygonApiView(CreateAPIView):
    serializer_class = serializers.PolygonsSerializer


class ListPolygonsApiView(ListAPIView):
    queryset = PolygonsModel.objects.all()
    serializer_class = serializers.PolygonsSerializer


class OnePolygonApiGenericView(RetrieveUpdateDestroyAPIView):
    queryset = PolygonsModel.objects.all()
    serializer_class = serializers.PolygonsSerializer
