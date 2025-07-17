from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sns_feed'

urlpatterns = [
    path('sns_feed/<int:chat_id>/', views.sns_feed, name='sns_feed'),
    path('create/', views.create, name='create'),
    path('/reply/create/', views.create, name='create'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)