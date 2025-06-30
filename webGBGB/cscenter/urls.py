from django.urls import path,include
from . import views

app_name = 'cscenter'

urlpatterns = [
    path('notice/', views.notice,name='notice'),
    path('view/<int:ntcno>/', views.view,name='view'),
    path('inquiry/', views.inquiry,name='inquiry'),
]