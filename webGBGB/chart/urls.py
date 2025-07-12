from django.urls import path,include
from . import views

<<<<<<<< HEAD:webGBGB/chart/urls.py
app_name='chart'
urlpatterns = [
    path('chajax/', views.chajax, name='chajax')
]
========
urlpatterns = [
    path('',views.base,name='base'),
]
>>>>>>>> origin/5-feat-mypage01_backend:webGBGB/base/urls.py
