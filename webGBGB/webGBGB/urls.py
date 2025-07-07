from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('member/', include('member.urls')),
    path('booksearch/', include('booksearch.urls')),
    path('review/', include('review.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('mypage/', include('mypage.urls')),
    path('', include('dummyhome.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)