from django.shortcuts import render, redirect
from . models import ReadingGroup  # 그룹 모델
# from django.contrib.auth.models import User  # 로그인 안 쓸 경우 생략 가능


# 교환독서_메인페이지 | Share_Main
def Share_Main(request):
    groups = ReadingGroup.objects.all().order_by('-id')  # 최신순 정렬
    
    for group in groups:
        group.tags_list = group.tag.split(",")
    
    return render(request, 'shareMain/Share_Main.html', {'groups':groups})


# 교환독서_그룹만들기 | Share_AddGroup
def Share_AddGroup(request):
    if request.method == 'GET':
        return render(request,'shareMain/Share_AddGroup.html')
    elif request.method == 'POST' :
        # 회원정보 DB저장
        group_name = request.POST.get('group_name')
        member_count = int(request.POST.get('member_count'))
        description = request.POST.get('description','')
        book = request.POST.get('book')
        tag = request.POST.get('tag')
        is_public = int(request.POST.get('is_public'))  # 체크 안 하면 0
        password = request.POST.get('password')
    
        ReadingGroup.objects.create(
            group_name=group_name,
            member_count=member_count,
            description=description,
            book=book,
            tag=tag,
            is_public=is_public,
            password=password,
        )
        return redirect('shareMain:Share_Main')  # 생성 후 메인으로 이동

