from django.urls import path,include
from . import views

<<<<<<<< HEAD:webGBGB/home/urls.py
app_name = ''

urlpatterns = [
    path('', views.index,name='index'),
========
urlpatterns = [
    path('',views.base,name='base'),
>>>>>>>> 7-feat-share_main-addgroup-backend:webGBGB/base/urls.py
]
