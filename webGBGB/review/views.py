from django.shortcuts import render, redirect
from review.models import Review
from review.models import ReviewImage
from member.models import Member
from booksearch.models import Book
from django.contrib import messages


# Create your views here.
def review_create(request):
    if request.method == 'POST':
        member_id = request.session.get('user_id')
        if not member_id:
            messages.error(request, "로그인이 필요합니다.")
            return redirect('/member/login/')
        
        try:
            member = Member.objects.get(id=member_id)  # Member 객체 가져오기
        except Member.DoesNotExist:
            messages.error(request, "회원 정보가 없습니다.")
            return redirect('/member/login/')


        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(book_id=book_id)  # Book 객체 가져오기
        except Book.DoesNotExist:
            messages.error(request, "책 정보가 없습니다.")
            return redirect('/')

        rating = int(request.POST.get('rating', 0))
        tag = request.POST.get('tag', '')
        comments = request.POST.get('reviewText', '')

        review = Review.objects.create(
            member_id=member,
            book_id=book,
            rating=rating,
            tag=tag,
            content=comments,
        )

        print("넘어온 데이터 : ", member_id, book_id, rating, tag, comments)
        
        images = request.FILES.getlist('review_image', '')  # 단일 이미지 (ImageField 단일)
        for i, img in enumerate(images):
            if i>=3:
                break
            ReviewImage.objects.create(review_id=review, image=img)

        print("FILES:", request.FILES)
        print("IMAGES:", request.FILES.getlist('review_image'))

        # 리뷰 저장 후
        return redirect(f'/booksearch/detail/{book.title}/{book.author}/')
