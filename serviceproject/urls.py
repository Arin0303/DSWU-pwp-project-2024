from django.contrib import admin
from django.urls import path, include
from meetapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include('meetapp.urls')),
]
