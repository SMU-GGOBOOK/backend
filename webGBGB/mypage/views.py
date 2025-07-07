from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import F,Q
# from review.models import Review
# from django.contrib.auth.decorators import login_required

# @login_required

## list : 현재 페이지의 리뷰 목록
#list.paginator.num_pages : 전체 페이지 수
# list.has_previous / list.previous_page_number
# list.has_next / list.next_page_number
# page : 현재 페이지 번호

## 리뷰,멤버만 있으면 가능
def review(request):
    # page = request.GET.get('page',1)
    # # 현재 로그인한 유저의 리뷰만 가져오기
    # qs = Review.objects.filter(id=request.id).order_by('-created_at')
    
    # # 페이지네이션
    # paginator = Paginator(qs, 5)  # 5개씩 자르기
    # paginated_reviews = paginator.get_page(page)  # 현재 페이지에 해당하는 리뷰 가져오기

    # context = {
    #     'list': paginated_reviews,  # 💡 list로 넘겨줘서 템플릿에서 {% for review in list %} 가능
    #     'page': int(page),          # 현재 페이지 번호 넘겨주기
    # }

    # return render(request, 'mypage/review.html', context)
    return render(request, 'mypage/review.html')

def Bmark(request):
    return render(request,'mypage/Bmark.html')

def mygroup(request):
    return render(request,'mypage/mygroup.html')

# def review_delete(request):
#     if request.method =='POST':
#         review_id = request.POST.get('review_id')
        
#         ## 나중에 db 연결되면 실제 삭제처리 들어갈 자리 
            
#         return JsonResponse({"result":"success"})



#     return JsonResponse({'result':'error','message':'invalid method'},status=400)
