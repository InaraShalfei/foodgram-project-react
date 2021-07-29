from django.conf.urls import url
from django.urls import include, path

urlpatterns = [
    path('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
