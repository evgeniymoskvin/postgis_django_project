from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/all', views.ListPolygonsApiView.as_view(), name='api-all'),
    path('api/create', views.CreatePolygonApiView.as_view(), name='api-create'),
    path('api/polygon/<int:pk>', views.OnePolygonApiGenericView.as_view(), name='api-one-gen'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
