from django.urls import path,include
from . import views

app_name='mypage'

urlpatterns = [
    path('review/', views.review,name='review'),
    path('Bmark/', views.Bmark,name='Bmark'),
    path('mygroup/', views.mygroup,name='mygroup'),
    path('mygroup/review_delete/', views.review_delete,name='review_delete'),
]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)