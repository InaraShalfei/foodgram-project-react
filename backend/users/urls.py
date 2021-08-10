from django.conf.urls import url
from django.urls import include, path

from users.views import UserViewSet

subscribe = UserViewSet.as_view({
    'get': 'subscribe',
    'delete': 'subscribe'
})

subscriptions = UserViewSet.as_view({
    'get': 'subscriptions',
   })

urlpatterns = [
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', subscribe, name='subscribe'),
]
