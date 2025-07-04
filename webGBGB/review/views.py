from django.shortcuts import render, redirect
from .models import Review
from booksearch.models import Book

# Create your views here.
def review_create(request):
    if request.method == 'POST':
        rating = request.POST.get('rating', 0)
        tag = request.POST.get('tag', '')
        comments = request.POST['comments']
        files = request.FILES.getlist("review_image")
        
        Review.objects.create(
            rating=rating,
            tag=tag,
            comments=comments,
            file=files,
        )
        return redirect('booksearch:book_detail')
   