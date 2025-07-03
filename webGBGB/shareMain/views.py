from django.shortcuts import render

# 교환독서_그룹만들기
def Share_AddGroup(request):
    return render(request,'shareMain/Share_AddGroup.html')


# 교환독서_메인페이지
def Share_Main(request):
    return render(request,'shareMain/Share_Main.html')
