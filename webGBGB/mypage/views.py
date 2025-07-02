from django.shortcuts import render

def review(request):
    return render(request,'mypage/review.html')


def Bmark(request):
    return render(request,'mypage/Bmark.html')