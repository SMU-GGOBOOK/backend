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
    qs = Notice.objects.filter(ntcno=ntcno)
    
    # 다음글: ntcno가 현재글보다 큰것 중 가장 작은거(역순정렬했을때 바로 위글)
    next_qs = Notice.objects.filter(
        ntcno__gt = qs[0].ntcno
    ).order_by('ntcno').first()
    
    # 이전글: ntcno가 현재글보다 작은것 중 가장 큰거(역순정렬했을때 바로 아래글)
    pre_qs = Notice.objects.filter(
        ntcno__lt = qs[0].ntcno
    ).order_by('-ntcno').first()
    
    
    
    context={'notice':qs[0],'next_ntc':next_qs,'pre_ntc':pre_qs}
    return render(request,'cscenter/view.html',context)

def inquiry(request):
    return render(request,'cscenter/inquiry.html')