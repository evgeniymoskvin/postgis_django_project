from django import template
from ..models import PolygonsModel

register = template.Library()


@register.simple_tag()
def get_coordinates(polygon_data):
    """Получение списка координат"""
    points = polygon_data[0]
    result_polygon = []

    for i in range(len(points)):
        result_polygon.append((points.x[i], points.y[i]))
    return result_polygon
