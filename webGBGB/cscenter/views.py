from django.shortcuts import render

def notice(request):
    return render(request,'cscenter/notice.html')

def view(request,ntcno):
    return render(request,'cscenter/view.html')

def inquiry(request):
    return render(request,'cscenter/inquiry.html')