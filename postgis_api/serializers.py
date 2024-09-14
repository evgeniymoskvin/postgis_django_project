from rest_framework import serializers

from postgis_app.models import PolygonsModel


class PolygonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonsModel
        fields = "__all__"
