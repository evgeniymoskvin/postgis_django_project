# from django.db import models
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PolygonsModel(models.Model):
    """Таблица полигонов"""
    name_of_polygon = models.CharField(verbose_name="Название полигона", null=False, max_length=100, blank=False)
    polygon = models.PolygonField(verbose_name="Полигон")
    antimeridian = models.BooleanField(verbose_name="Aнтимеридиан", default=False)

    class Meta:
        verbose_name = _('полигон')
        verbose_name_plural = _('полигоны')

    def __str__(self):
        return f'{self.name_of_polygon} - {self.polygon}'
