from django.shortcuts import render, redirect
from shareMain.models import ReadingGroup
from django.contrib import messages
from member.models import Member
from sns_feed.models import Post
from sns_feed.models import PostImage


def sns_feed(request, chat_id):
    print("넘어온 chat_id : ", chat_id)
    reading_group = ReadingGroup.objects.get(id=chat_id)
    try:
        post = Post.objects.filter(group_id=reading_group.id)
    except Post.DoesNotExist:
        post = None  # 또는 리스트, 또는 '' 등

    tag_list = reading_group.tags_list
    context = {
        'readinggroup': reading_group,
        'tag_list': tag_list,
        'post': post,
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

