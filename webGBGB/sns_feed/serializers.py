from rest_framework import serializers
from .models import GroupChatRoom, Post, Comment, UserProfile, Like # Like 모델 임포트
from django.contrib.auth import get_user_model # User 모델 임포트

User = get_user_model() # get_user_model()로 User 모델 가져오기


class GroupChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatRoom
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # 댓글 작성자 정보도 함께 보여주기 위해 SerializerMethodField 사용
    author_username = serializers.SerializerMethodField()
    author_profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post', 'created_at', 'updated_at') # 작성자, 게시글, 시간은 읽기 전용

    def get_author_username(self, obj):
        return obj.author.username

    def get_author_profile_image_url(self, obj):
        # UserProfile이 존재하는 경우에만 이미지 URL 반환
        if hasattr(obj.author, 'profile') and obj.author.profile.profile_image:
            return obj.author.profile.profile_image.url
        return None # 프로필 이미지가 없으면 None 반환


class PostSerializer(serializers.ModelSerializer):
    # 게시글 작성자 정보도 함께 보여주기 위해 SerializerMethodField 사용
    author_username = serializers.SerializerMethodField()
    author_profile_image_url = serializers.SerializerMethodField()
    
    # 해당 게시글에 달린 댓글들을 함께 보여주기 위해 CommentSerializer 사용
    comments = CommentSerializer(many=True, read_only=True)

    # 좋아요 수와 현재 유저의 좋아요 여부를 위한 필드 추가
    likes_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField() # 현재 사용자가 좋아요 눌렀는지 여부

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'group', 'created_at', 'updated_at') # 작성자, 그룹, 시간은 읽기 전용

    def get_author_username(self, obj):
        return obj.author.username

    def get_author_profile_image_url(self, obj):
        if hasattr(obj.author, 'profile') and obj.author.profile.profile_image:
            return obj.author.profile.profile_image.url
        return None

    def get_likes_count(self, obj):
        # Post에 연결된 Like 객체들의 수를 세어 반환
        return obj.likes.count()

    def get_is_liked_by_user(self, obj):
        # Serializer context에서 request 객체를 가져와 현재 사용자를 확인
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # 현재 사용자가 이 게시글에 좋아요를 눌렀는지 확인
            return obj.likes.filter(user=request.user).exists()
        return False # 로그인하지 않았거나 요청 객체가 없으면 항상 False


class LikeSerializer(serializers.ModelSerializer):
    """
    좋아요 객체 생성을 위한 Serializer
    """
    class Meta:
        model = Like
        fields = '__all__' # 'user', 'post', 'created_at'
        read_only_fields = ('user', 'created_at') # 좋아요를 누른 사용자 및 시간은 자동으로 설정