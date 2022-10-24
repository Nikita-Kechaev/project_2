from django.urls import include, path
from rest_framework import routers

from .views import GalleryViewSet, JornalViewSet, NewViewSet

app_name = 'api'


router_v1 = routers.DefaultRouter()
router_v1.register("news", NewViewSet, basename="news")
router_v1.register("gallery", GalleryViewSet, basename="gallery")
router_v1.register("journal", JornalViewSet, basename="journal")


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
] + router_v1.urls
