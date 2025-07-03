from django.shortcuts import render
from django.http import JsonResponse

def review(request):
    return render(request,'mypage/review.html')

def Bmark(request):
    return render(request,'mypage/Bmark.html')

def mygroup(request):
    return render(request,'mypage/mygroup.html')

def review_delete(request):
    if request.method =='POST':
        review_id = request.POST.get('review_id')
        
        ## 나중에 db 연결되면 실제 삭제처리 들어갈 자리 
            
        return JsonResponse({"result":"success"})


    return JsonResponse({'result':'error','message':'invalid method'},status=400)

