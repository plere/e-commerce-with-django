from django.urls import path
from . import views


urlpatterns = [
    path('create', views.Registration.as_view()),
    path('login', views.Login.as_view()),
    path('info', views.Info.as_view()),
    path('modify', views.Modify.as_view()),
    path('delete', views.Delete.as_view()),
]
