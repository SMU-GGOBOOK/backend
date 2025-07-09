
from django.urls import path,include
from . import views

app_name = 'shareReading'

urlpatterns = [
    path('main/',views.main,name='main'),
    path('addgroup/',views.addgroup,name='addgroup'),
]