from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('stop/', views.stop, name='stop'),
    path('info/', views.info, name='info'),
]
