
from django.urls import path,include
from . import views

app_name = 'review'

urlpatterns = [
    path('create/',views.review_create,name='review_create'),
    path('delete/<int:review_id>/',views.review_delete,name='review_delete'),
]