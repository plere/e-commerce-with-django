from django.urls import path
from . import views
from .views import UserViewSet

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('create', views.Registration.as_view()),
    path('login', views.Login.as_view()),
    path('<username>', user_detail),
]
