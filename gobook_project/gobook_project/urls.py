from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chatrooms.views import chatroom_html_view # 새로 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatrooms.urls')), # API 엔드포인트는 그대로 유지
    path('', chatroom_html_view, name='home'), # 루트 URL (http://127.0.0.1:8000/) 에 이 뷰 연결
    path('chatroom/', chatroom_html_view, name='chatroom-page'), # 또는 /chatroom/ 경로로도 연결 가능
]

# 개발 모드에서 미디어 파일 서빙 설정 (기존 설정 유지)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)