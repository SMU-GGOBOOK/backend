from django.shortcuts import render
from booksearch.models import Book
from shareReading.models import ReadingGroup
from home.models import Mainbanner

def index(request):
    try:
        pop_group = ReadingGroup.objects.all().order_by('-created_at')[:8]
        review_top5 = Book.objects.all().order_by('-review_count')[:5]
        bookmark_top5 = Book.objects.all().order_by('-bookmark_count')[:5]
        views_top5 = Book.objects.all().order_by('-views')[:5]
        mainBanner = Mainbanner.objects.all().order_by('primary')
        
    except:
        pop_group = None
        review_top5 = None
        bookmark_top5 = None
        views_top5 = None
    
    context = {'sharegroup':pop_group,'review':review_top5,'bookmark':bookmark_top5,'views':views_top5,'mainBanner':mainBanner}
    
    return render(request,'index.html',context)