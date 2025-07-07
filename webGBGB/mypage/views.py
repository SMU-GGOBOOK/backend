from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import F,Q
from review.models import Review
from member.models import Member



## list : 현재 페이지의 리뷰 목록
#list.paginator.num_pages : 전체 페이지 수
# list.has_previous / list.previous_page_number
# list.has_next / list.next_page_number
# page : 현재 페이지 번호

## 리뷰,멤버만 있으면 가능
def review(request):
    user_id = request.session.get('user_id')  # 로그인된 유저의 ID

    if not user_id:
        return redirect(f'/member/login/?next={request.path}')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        member = Member.objects.get(id=user_id)  # 문자열 ID 기준으로 조회
    except Member.DoesNotExist:
        return redirect(f'/member/login/?next={request.path}')  # 세션은 있는데 유저가 없을 경우도 예외 처리

    page = request.GET.get('page', 1)
    qs = Review.objects.filter(member_id=member).order_by('-created_at')  # member_id는 FK니까 객체로 필터

    paginator = Paginator(qs, 5)
    paginated_reviews = paginator.get_page(page)

    context = {
        'reviews': paginated_reviews,
        'page': int(page),
    }

    return render(request, 'mypage/review.html', context)


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
