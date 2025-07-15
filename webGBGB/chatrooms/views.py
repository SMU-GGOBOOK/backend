from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import GroupChatRoom # GroupChatRoom은 새로 정의한 모델
from .serializers import GroupChatRoomSerializer
from django.db import transaction
import os # 파일 업로드 경로를 위해
from django.conf import settings # MEDIA_URL, MEDIA_ROOT 사용을 위해


class ChatRoomDetailView(generics.RetrieveAPIView):
    """
    GET /api/chatroom/{chat_id} - 특정 채팅방의 상세 정보를 조회
    """
    queryset = GroupChatRoom.objects.all()
    serializer_class = GroupChatRoomSerializer
    lookup_field = 'pk' # URL에서 chat_id를 pk로 매칭

class ChatRoomJoinView(APIView):
    """
    POST /api/chatroom/{chat_id}/join - 사용자가 특정 채팅방에 참여
    """
    def post(self, request, pk):
        try:
            with transaction.atomic(): # 원자적 연산으로 데이터 일관성 유지
                chatroom = get_object_or_404(GroupChatRoom, pk=pk)
                user_id = request.data.get('user_id') # 프론트에서 user_id를 body로 보낸다고 가정

                if not user_id:
                    return Response({"detail": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

                if chatroom.current_members >= chatroom.max_members:
                    return Response({"detail": "Maximum members reached for this chatroom"}, status=status.HTTP_400_BAD_REQUEST)

                # TODO: 실제 사용자-그룹 관계 테이블에 추가하는 로직 필요 (예: UserGroup 모델)
                # 현재는 단순히 current_members만 증가
                chatroom.current_members += 1
                chatroom.save()

                serializer = GroupChatRoomSerializer(chatroom)
                return Response({
                    "message": "Successfully joined the chatroom",
                    "current_members": chatroom.current_members,
                    "max_members": chatroom.max_members,
                    "chatroom_details": serializer.data # 업데이트된 채팅방 정보 반환
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileUploadView(APIView):
    """
    POST /api/profile/upload - 사용자 프로필 이미지를 업로드
    """
    def post(self, request, *args, **kwargs):
        # user_id = request.data.get('user_id') # 사용자 ID
        profile_image = request.FILES.get('profile_image') # 업로드된 파일

        if not profile_image:
            return Response({"detail": "No profile image provided."}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: 실제로는 사용자의 프로필 이미지 필드를 업데이트 해야 함
        # 예: user = get_object_or_404(User, id=user_id)
        #     user.profile_image = profile_image
        #     user.save()

        # 파일 저장 경로 설정 (settings.py에 MEDIA_ROOT, MEDIA_URL 설정 필요)
        if not hasattr(settings, 'MEDIA_ROOT') or not settings.MEDIA_ROOT:
             return Response({"detail": "MEDIA_ROOT is not configured in settings.py"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'profiles')
        os.makedirs(upload_dir, exist_ok=True) # 디렉토리가 없으면 생성

        file_name = f"{request.user.id or 'default'}_{profile_image.name}" # 사용자 ID로 파일명 구분
        file_path = os.path.join(upload_dir, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in profile_image.chunks():
                destination.write(chunk)

        # 클라이언트에서 접근할 수 있는 URL 반환
        image_url = os.path.join(settings.MEDIA_URL, 'profiles', file_name)
        return Response({"message": "Profile image uploaded successfully", "imageUrl": image_url}, status=status.HTTP_200_OK)
    
def chatroom_html_view(request):
    """
    chatroom_detail.html 파일을 렌더링하여 반환하는 뷰
    """
    return render(request, 'chatroom_detail.html')