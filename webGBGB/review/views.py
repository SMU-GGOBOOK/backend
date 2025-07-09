from django.shortcuts import render, redirect
from review.models import Review
from review.models import ReviewImage
from member.models import Member
from booksearch.models import Book
from django.contrib import messages
from django.http import JsonResponse
import json


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
        
        book.review_count += 1
        book.rating += rating
        book.save()

        print("넘어온 데이터 : ", member_id, book_id, rating, tag, comments)
                
        images = request.FILES.getlist('review_image', '')  # 단일 이미지 (ImageField 단일)
        for i, img in enumerate(images):
            if i>=3:
                break
            ReviewImage.objects.create(review_id=review, image=img)

        print("FILES:", request.FILES)
        print("IMAGES:", request.FILES.getlist('review_image'))

        # 리뷰 저장 후
        return redirect(f'/booksearch/detail/{book.book_id}/')

def review_delete(request, review_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('/member/login/')

    member = Member.objects.get(id=user_id)
    review = Review.objects.get(review_id=review_id)
    
    rating = review.rating
    book = review.book_id
    
    if review.member_id.member_id != member.member_id:
        messages.error(request, "본인이 작성한 리뷰만 삭제할 수 있습니다.")
        return redirect(f'/booksearch/detail/{review.book_id.book_id}/')
    
    print(review.member_id, member.member_id)
    review.delete()
    
    book.review_count = max(0, book.review_count - 1)
    book.rating = max(0, book.rating - rating)
    book.save()
    
    messages.success(request, "리뷰가 삭제되었습니다.")
    
    return redirect(f'/booksearch/detail/{review.book_id.book_id}/')

def review_like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        review_id = data.get('review_id')
        delta = data.get('delta')

        try:
            review = Review.objects.get(review_id=review_id)
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'error': '리뷰 없음'}, status=404)

        # 좋아요 토글 처리
        review.likes = max(0, review.likes + int(delta))
        review.save()

        return JsonResponse({'success': True, 'likes': review.likes})

    return JsonResponse({'success': False, 'error': '잘못된 요청'}, status=400)
