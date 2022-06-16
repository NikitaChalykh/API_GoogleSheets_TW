from django.urls import include, path
from rest_framework import routers

from .views import OrdersViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('orders', OrdersViewSet)

urlpatterns = [
    path('', include(router_api.urls))
]
