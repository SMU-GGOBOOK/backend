from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sns_feed'

urlpatterns = [
    path('sns_feed/<int:chat_id>/', views.sns_feed, name='sns_feed'),
    path('create/', views.create, name='create'),
    path('reply/create/', views.reply_create, name='reply_create'),
    path('like/',views.post_like,name='post_like'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)