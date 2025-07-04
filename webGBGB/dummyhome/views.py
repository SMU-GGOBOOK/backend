from django.shortcuts import render

# Create your views here.
def dummyhome(request):
    return render(request,"dummyhome.html")