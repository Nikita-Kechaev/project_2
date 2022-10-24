from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck/', lambda r: HttpResponse()),
    path('api/', include('api.urls')),
    path('api/auth/social/', include('rest_framework_social_oauth2.urls')),
]
