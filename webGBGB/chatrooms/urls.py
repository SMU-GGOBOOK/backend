from django.urls import path
from .views import ChatRoomDetailView, ChatRoomJoinView, ProfileUploadView

urlpatterns = [
    path('chatroom/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('chatroom/<int:pk>/join/', ChatRoomJoinView.as_view(), name='chatroom-join'),
    path('profile/upload/', ProfileUploadView.as_view(), name='profile-upload'),
]