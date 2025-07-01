from django.shortcuts import render

# Create your views here.
def booksearch(request):
    return render(request, 'booksearch/booksearch.html')