from django.urls import path
from . import views
from .views import StoreViewSet


store_list = StoreViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'patch': 'partial_update'
})


urlpatterns = [
    path('stores/', store_list),
    path('login/', views.Login.as_view())
]
