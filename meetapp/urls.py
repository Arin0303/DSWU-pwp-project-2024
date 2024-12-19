from django.contrib import admin
from django.urls import path, include
from meetapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('profile/', views.midpoint_list, name='midpoint_list'),
    
]
