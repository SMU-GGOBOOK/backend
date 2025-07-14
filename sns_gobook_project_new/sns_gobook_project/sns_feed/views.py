from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, Http404
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F

# Like 모델 임포트 추가
from .models import GroupChatRoom, Post, Comment, UserProfile, Like
# LikeSerializer 임포트 추가
from .serializers import GroupChatRoomSerializer, PostSerializer, CommentSerializer, UserProfileSerializer, LikeSerializer


User = get_user_model() # get_user_model()로 User 모델 가져오기

# --- HTML 렌더링 뷰 ---
def sns_html_view(request):
    return render(request, 'chatroom_sns.html') # chatroom_sns.html 렌더링

# --- API View ---

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def get_serializer_context(self):
        # PostSerializer에 request 객체를 context로 전달하여 is_liked_by_user 계산에 사용
        return {'request': self.request}

    def perform_create(self, serializer):
        author = self.request.user if self.request.user.is_authenticated else None
        if not author:
            try:
                author = User.objects.get(id=1)
            except User.DoesNotExist:
                author = User.objects.first()
                if not author:
                    raise Http404("게시글을 작성할 사용자가 없습니다. 관리자 페이지에서 사용자를 생성해주세요.")

        group = None
        try:
            group = get_object_or_404(GroupChatRoom, id=1)
        except Http404:
            group = GroupChatRoom.objects.first()
            if not group:
                raise Http404("게시글을 작성할 그룹이 없습니다. 관리자 페이지에서 그룹을 생성해주세요.")

        serializer.save(author=author, group=group)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        # PostSerializer에 request 객체를 context로 전달
        return {'request': self.request}


class PostLikeView(APIView):
    """
    게시글 좋아요/취소 API View
    """
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # 좋아요를 누르는 사용자 (인증된 사용자 또는 임시로 id=1 사용자)
        user = request.user if request.user.is_authenticated else None
        if not user:
            try:
                user = User.objects.get(id=1)
            except User.DoesNotExist:
                return Response({"detail": "좋아요를 누를 사용자를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 좋아요 객체 생성 시도: 이미 좋아요가 있다면 created는 False
        like, created = Like.objects.get_or_create(user=user, post=post)

        if created:
            # 좋아요가 새로 생성됨 (좋아요 성공)
            message = "Post liked successfully."
            status_code = status.HTTP_201_CREATED
        else:
            # 이미 좋아요가 존재했으므로, 좋아요 취소로 간주하고 Like 객체 삭제
            like.delete()
            message = "Post unliked successfully."
            status_code = status.HTTP_200_OK
        
        # 좋아요/취소 후, 게시글의 최신 정보를 다시 시리얼라이즈하여 반환
        # 이때, request context를 전달하여 is_liked_by_user를 계산하도록 함
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status_code)


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_id).order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = get_object_or_404(Post, id=post_id)
        
        author = self.request.user if self.request.user.is_authenticated else None
        if not author:
            try:
                author = User.objects.get(id=1)
            except User.DoesNotExist:
                author = User.objects.first()
                if not author:
                    raise Http404("댓글을 작성할 사용자가 없습니다. 관리자 페이지에서 사용자를 생성해주세요.")
        
        serializer.save(post=post, author=author)

class ProfileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        if not user:
            try:
                user = User.objects.get(id=1)
            except User.DoesNotExist:
                user = User.objects.first()
                if not user:
                    return Response({"detail": "프로필 이미지를 업로드할 사용자가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        profile_image = request.FILES.get('profile_image')

        if not profile_image:
            return Response({"detail": "No profile image provided."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.profile_image = profile_image
        user_profile.save()

        image_url = user_profile.profile_image.url
        return Response({"message": "Profile image uploaded successfully", "imageUrl": image_url}, status=status.HTTP_200_OK)

class ChatRoomDetailView(generics.RetrieveAPIView):
    queryset = GroupChatRoom.objects.all()
    serializer_class = GroupChatRoomSerializer
    lookup_field = 'pk'

class ChatRoomJoinView(APIView):
    def post(self, request, pk):
        try:
            with transaction.atomic():
                chatroom = get_object_or_404(GroupChatRoom, pk=pk)
                user_id = request.data.get('user_id')
                
                if not user_id:
                    return Response({"detail": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
                
                if chatroom.current_members >= chatroom.max_members:
                    return Response({"detail": "Maximum members reached for this chatroom"}, status=status.HTTP_400_BAD_REQUEST)
                
                chatroom.current_members += 1
                chatroom.save()
                serializer = GroupChatRoomSerializer(chatroom)
                return Response({
                    "message": "Successfully joined the chatroom",
                    "current_members": chatroom.current_members,
                    "max_members": chatroom.max_members,
                    "chatroom_details": serializer.data
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)