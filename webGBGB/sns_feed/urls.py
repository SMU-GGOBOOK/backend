from django.urls import path, include
from . import views

urlpatterns = [
    path('sns_feed/<int:chat_id>/', views.sns_feed, name='sns-page'),

]