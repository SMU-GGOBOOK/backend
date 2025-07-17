from django.shortcuts import render, redirect
from shareMain.models import ReadingGroup
from django.contrib import messages
from member.models import Member
from sns_feed.models import Post
from sns_feed.models import Comment
from sns_feed.models import PostImage
from sns_feed.models import PostLike
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect



def sns_feed(request, chat_id):
    print("넘어온 chat_id : ", chat_id)
    reading_group = ReadingGroup.objects.get(id=chat_id)
    member_id = request.session.get('user_id')
    post = Post.objects.filter(group_id=reading_group.id).order_by('-created_at')
    for p in post:
        p.comment_list = Comment.objects.filter(post_id=p).order_by('created_at')
        
    likes = set()
    if member_id:
        try:
            member = Member.objects.get(id=member_id)
            from sns_feed.models import PostLike
            likes = set(
                PostLike.objects.filter(member_id=member)   # <-- 핵심! 반드시 member 객체로!
                .values_list('post_id', flat=True)
            )
        except Member.DoesNotExist:
            member = None
            
    print("likes : ", likes)
        
    tag_list = reading_group.tags_list
    context = {
        'readinggroup': reading_group,
        'tag_list': tag_list,
        'post': post,
        'likes': likes,
    }
    return render(request, 'chatroom_sns.html', context)

def create(request):
    if request.method == 'POST':
        member_id = request.session.get('user_id')
        member = Member.objects.get(id=member_id)  # Member 객체 가져오기

        content = request.POST.get('post-input',"")
        group_id = request.POST.get('readinggroup_id',"")
        try:
            group = ReadingGroup.objects.get(id=group_id)
        except ReadingGroup.DoesNotExist:
            messages.error(request, "그룹 정보가 없습니다.")
            return redirect('/')


        post = Post.objects.create(
            member_id=member,
            group_id=group,
            content=content,
            image=""
        )
        post.save()
        
        img = request.FILES.get('post_file')   # 없으면 None이므로 에러 안남!
        if img:
            PostImage.objects.create(post_id=post, image=img)

        
        print("넘어온 데이터 : ", member_id, group, content)
                
        # 리뷰 저장 후
        return redirect(f'/feedpage/sns_feed/{group.id}/')

def reply_create(request):
    if request.method == 'POST':
        member_id = request.session.get('user_id')
        member = Member.objects.get(id=member_id)  # Member 객체 가져오기
        content = request.POST.get('replytext',"")
        post_id = request.POST.get('post_id',"")
        
        try:
            post = Post.objects.get(id=post_id)
        except ReadingGroup.DoesNotExist:
            messages.error(request, "그룹 정보가 없습니다.")
            return redirect('/')

        comment = Comment.objects.create(
            member_id=member,
            post_id=post,
            content=content,
        )
        comment.save()
        
        group_id = post.group_id.id
        print("넘어온 데이터 : ", member_id, post_id, content)
                
        # 리뷰 저장 후
        return redirect(f'/feedpage/sns_feed/{group_id}/')
    
@csrf_protect
@require_POST
def post_like(request):
    user_id = request.session.get('user_id')
    try:
        member = Member.objects.get(id=user_id)
    except Member.DoesNotExist:
        return JsonResponse({'error': '회원 정보가 없습니다.'}, status=404)

    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
    except Exception:
        return JsonResponse({'error': '잘못된 요청 데이터입니다.'}, status=400)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': '리뷰 정보가 없습니다.'}, status=404)
    
    print("member :", member, "post : ", post)

    # 좋아요 토글
    like_obj, created = PostLike.objects.get_or_create(member_id=member, post_id=post)
    if not created:
        # 이미 좋아요 누른 상태 -> 취소
        like_obj.delete()
        liked = False
    else:
        # 좋아요 추가
        liked = True

    # 좋아요 총합
    total_likes = PostLike.objects.filter(post_id=post).count()
    return JsonResponse({'liked': liked, 'like_count': total_likes})

   

    

