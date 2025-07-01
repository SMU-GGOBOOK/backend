from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from cscenter.models import Notice

def list(request):
    # 요청하는 page번호 가져오기, str타입 -> int타입
    page = int(request.GET.get('page',1))
    # db에서 데이터 가져오기
    qs = Notice.objects.all().order_by('-ntcno')
    # 10개단위로 qs로 분리시킴
    paginator = Paginator(qs,10)
    
    # 가져올 페이지 선택
    noticeList = paginator.get_page(page)
    print('-----------------')
    print(noticeList)
    print('-----------------')
    
    # 게시글 10개, 현재페이지 보냄
    context = {'notice':qs,'list':noticeList,'page':page}
    return render(request,'cscenter/list.html',context)

def view(request,ntcno):
    qs = Notice.objects.get(ntcno=ntcno)
    context={'notice':qs}
    return render(request,'cscenter/view.html',context)

def inquiry(request):
    return render(request,'cscenter/inquiry.html')