from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from postgis_app.models import PolygonsModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from . import serializers

class CreatePolygonApiView(CreateAPIView):
    serializer_class = serializers.PolygonsSerializer

class ListPolygonsApiView(ListAPIView):
    queryset = PolygonsModel.objects.all()
    serializer_class = serializers.PolygonsSerializer


class OnePolygonApiGenericView(RetrieveUpdateDestroyAPIView):
    queryset = PolygonsModel.objects.all()
    serializer_class = serializers.PolygonsSerializer
