from django.urls import path, include
from .views import (
    sns_html_view, # HTML 렌더링 뷰
    PostListView, PostDetailView, PostLikeView, CommentListView,
    ProfileUploadView, # 사용자 프로필 이미지 업로드 뷰 추가
    ChatRoomDetailView, ChatRoomJoinView # GroupChatRoom 관련 뷰
)

urlpatterns = [
    # API 엔드포인트
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('posts/<int:post_pk>/comments/', CommentListView.as_view(), name='comment-list'),
    path('profile/upload/', ProfileUploadView.as_view(), name='profile-upload'), # 프로필 업로드

    # # GroupChatRoom 관련 API
    # path('chatroom/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
    # path('chatroom/<int:pk>/join/', ChatRoomJoinView.as_view(), name='chatroom-join'),

    # 앱 내에서 HTML 뷰를 직접 라우팅할 경우
    # path('sns/', sns_html_view, name='sns-page'),
]