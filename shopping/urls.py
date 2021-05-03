from django.urls import path
from . import views
from .views import StoreViewSet, ItemViewSet

store_list = StoreViewSet.as_view({
    'post': 'create',
})

store_detail = StoreViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

item_list = ItemViewSet.as_view({
    'get': 'list',
    'post': 'create',

})

item_detail = ItemViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'

})

urlpatterns = [
    path('stores/', store_list),
    path('stores/<store_name>', store_detail),
    path('login/', views.Login.as_view()),
    path('item', item_list),
    path('item/<int:pk>', item_detail),

]
