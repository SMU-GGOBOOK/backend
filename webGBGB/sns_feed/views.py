from rest_framework import generics, status, serializers # serializers 임포트 추가
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, Http404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from shareMain.models import ReadingGroup
from member.models import Member

# --- HTML 렌더링 뷰 ---
# chat_id를 인자로 받아 해당 독서 모임 정보를 HTML 템플릿에 전달
def sns_feed(request, chat_id):
    reading_group = ReadingGroup.objects.get(id=chat_id)
    tag_list = reading_group.tags_list
    context = {
        'readinggroup': reading_group,
        'tag_list': tag_list
    }
    return render(request, 'chatroom_sns.html', context)


