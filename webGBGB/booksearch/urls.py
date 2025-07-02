from django.urls import path,include
from . import views

app_name='booksearch'
urlpatterns = [
    path('booksearch/', views.booksearch, name='booksearch'), # list 페이지 연결
    path('detail/', views.detail, name='detail'), # list 페이지 연결
]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)