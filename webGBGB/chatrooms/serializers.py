from rest_framework import serializers
from .models import GroupChatRoom, ChatMessage # GroupChatRoom은 새로 정의한 모델

class GroupChatRoomSerializer(serializers.ModelSerializer):
    tags = serializers.JSONField() # JSONField는 Django REST Framework에서 기본 지원

    class Meta:
        model = GroupChatRoom
        fields = '__all__' # 모든 필드를 포함

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'