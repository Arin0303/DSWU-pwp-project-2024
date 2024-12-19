from django.urls import path
from serviceproject import views
from django.contrib import admin


urlpatterns = [
    path('', views.index, name='index'),  # 출발지점 입력 페이지
    path('result/', views.result, name='result'),  # 결과 페이지
    path('result/<str:location>/', views.result_detail, name='result_detail'),  
    # 결과 상세 페이지
    path('profile/', views.midpoint_list, name='midpoint_list'),
]
