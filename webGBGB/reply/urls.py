
from django.urls import path,include
from . import views

app_name = 'reply'

urlpatterns = [
    path('create/',views.reply_create,name='reply_create'),
    path('delete/<int:reply_id>/',views.reply_delete,name='reply_delete'),
]