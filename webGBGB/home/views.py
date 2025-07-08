from django.shortcuts import render
from booksearch.models import Book

def index(request):
    review_top5 = Book.objects.all().order_by('-review_count')[:5]
    bookmark_top5 = Book.objects.all().order_by('-bookmark_count')[:5]
    views_top5 = Book.objects.all().order_by('-views')[:5]
    
    context = {'review':review_top5,'bookmark':bookmark_top5,'views':views_top5}
    
    return render(request,'index.html',context)