from django.urls import path
from . import views
from .views import StoreViewSet


store_list = StoreViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

store_detail = StoreViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('stores/', store_list),
    path('stores/<store_name>', store_detail),
    path('login/', views.Login.as_view())
]
