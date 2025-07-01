from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from cscenter.models import Notice
from cscenter.models import Inquiry
from django.http import JsonResponse

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
    if request.method == 'GET':
        return render(request,'cscenter/inquiry.html')
    elif request.method == 'POST':
        return redirect('/cscenter/notice/')
    


@require_http_methods(["POST"])
def submit(request):
    try:
        category = request.POST.get('category_inq')
        title = request.POST.get('title_inq')
        content = request.POST.get('content_inq')
        
        # 업로드된 파일s 처리
        uploaded_files = []
        for key, file in request.FILES.items():
            if key.startswith('uploaded_file_'):
                uploaded_files.append(file)
        
        # 모델에 저장 (파일 필드가 어떻게 정의되어 있는지에 따라 다름)
        inquiry = Inquiry.objects.create(
            ictgr=category,
            ititle=title,
            icontent=content,
            id='aaa',
            # user=request.session['session_id'],
        )
        
        # 파일들을 별도로 저장 (파일 개수에 상관없이)
        for i, file in enumerate(uploaded_files[:3]):  # 최대 3개까지만
            if i == 0:
                inquiry.ifile1 = file
            elif i == 1:
                inquiry.ifile2 = file
            elif i == 2:
                inquiry.ifile3 = file
        
        inquiry.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})