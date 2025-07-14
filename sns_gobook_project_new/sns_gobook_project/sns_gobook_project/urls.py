from django.contrib import admin
from django.urls import path, include, re_path # re_path 추가
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve # serve 추가
from sns_feed.views import sns_html_view # sns_feed 앱의 HTML 뷰 임포트
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sns_feed.urls')), # sns_feed 앱의 API URL 포함
    path('', sns_html_view, name='home'), # 루트 URL (http://127.0.0.1:8000/) 에 SNS HTML 뷰 연결
]

# 개발 모드에서 미디어 및 정적 파일 서빙 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += [
        re_path(r'^css/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/css')}),
        re_path(r'^js/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/js')}),
        re_path(r'^logos/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/logos')}),
        re_path(r'^images/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/images')}),
    ]