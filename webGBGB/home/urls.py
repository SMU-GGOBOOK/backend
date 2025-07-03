
from django.urls import path,include
from . import views

app_name = ''
urlpatterns = [
    
    path('base',views.base,name='base'),
    path('',views.iiii,name='iiii'),
    
    
]
