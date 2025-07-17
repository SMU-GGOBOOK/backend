from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import HttpResponse # 추가
from django.contrib.auth import get_user_model # 추가
from django.db import transaction # 추가
from django.db.models import F # 추가
from shareMain.models import ReadingGroup # ReadingGroup 모델 임포트
from member.models import Member # Member 모델 임포트
from .models import Post, Comment # Post와 Comment 모델 임포트 (댓글 업로드라면 Comment만)
from django.contrib import messages # 메시지 프레임워크 사용 (만약 views.py에 없다면 추가)

# --- HTML 렌더링 뷰 ---
# chat_id를 인자로 받아 해당 독서 모임 정보를 HTML 템플릿에 전달
def sns_feed(request, chat_id):
    reading_group = get_object_or_404(ReadingGroup, id=chat_id) # 그룹이 없으면 404
    tag_list = reading_group.tag.split(",") if reading_group.tag else [] # tags_list 대신 tag 필드 직접 처리

    # 현재 로그인한 멤버 정보 가져오기 (이전 chatroom_detail 뷰 로직 참고)
    member = None
    member_id = request.session.get('member_id')
    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
        except Member.DoesNotExist:
            messages.warning(request, '로그인이 필요합니다.')
            return redirect('member:login') # 'member:login'은 로그인 페이지의 URL 이름

    if request.method == 'POST':
        # 어떤 종류의 폼인지 (게시글인지, 댓글인지) 명확하지 않지만,
        # chatroom_sns.html의 'post-box'와 'ccontent', 'post-file-input'을 보면
        # 새로운 게시글/댓글을 작성하는 것으로 보입니다.
        # 여기서는 Post 모델을 사용하는 예시로 작성합니다.
        # 만약 Comment 모델에 직접 연결하고 싶다면 Post 대신 Comment 모델을 사용하세요.

        content = request.POST.get('ccontent') # 텍스트 내용 가져오기
        uploaded_file = request.FILES.get('post-file-input') # 업로드된 파일 가져오기 (input name과 일치)

        if content or uploaded_file: # 내용이나 파일이 있을 때만 처리
            try:
                # Post 모델에 새 객체 생성 (models.py의 Post 모델 구조에 따라 필드명 조정)
                # 만약 Post 모델에 'author'나 'member_id' 필드가 있다면 해당 객체를 사용해야 합니다.
                # 예시에서는 현재 로그인한 'member'를 'member_id'로 사용합니다.
                # 'author'는 settings.AUTH_USER_MODEL을 따르므로, 해당 유저 객체도 필요할 수 있습니다.
                # 이 예시는 member_id만 사용합니다.
                new_post = Post.objects.create(
                    member_id=member, # 현재 로그인한 멤버 객체
                    group=reading_group, # 현재 그룹 객체
                    content=content,
                    # Post 모델에 이미지 필드가 있다면 여기에 추가합니다. (현재 models.py의 Post에는 없음)
                    # 예를 들어, image_field=uploaded_file
                )

                # 만약 파일 업로드가 Comment 모델용이라면 (models.py의 Comment 모델에 cfile이 있음)
                # 아래와 같이 Comment 객체를 생성해야 합니다.
                # new_comment = Comment.objects.create(
                #     post=new_post, # 게시글에 대한 댓글이라면 해당 게시글 객체
                #     author=member.user_field_or_none, # Comment 모델의 author 필드에 맞는 유저 객체
                #     content=content,
                #     cfile=uploaded_file, # 파일 필드
                # )

                messages.success(request, '게시글이 성공적으로 작성되었습니다!')
                return redirect('sns-page', chat_id=chat_id) # 새로고침하여 목록 반영

            except Exception as e:
                messages.error(request, f'게시글 작성 중 오류가 발생했습니다: {e}')
        else:
            messages.warning(request, '내용을 입력하거나 파일을 첨부해주세요.')

    # GET 요청이거나 POST 처리 후 다시 렌더링할 때
    posts = Post.objects.filter(group=reading_group).order_by('-created_at') # 해당 그룹의 게시글 가져오기
    
    context = {
        'readinggroup': reading_group,
        'tag_list': tag_list,
        'posts': posts, # 게시글 목록을 템플릿으로 전달
    }
    return render(request, 'chatroom_sns.html', context)
