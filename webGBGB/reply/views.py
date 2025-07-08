from django.shortcuts import render, redirect
from django.contrib import messages
from member.models import Member
from reply.models import Reply
from booksearch.models import Book
from review.models import Review

# Create your views here.
def reply_create(request):
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
        
        review_id = request.POST.get('review_id')
        try:
            review = Review.objects.get(review_id=review_id)  # review 객체 가져오기
        except Review.DoesNotExist:
            messages.error(request, "리뷰 정보가 없습니다.")
            return redirect('/')
        
        try:
            book = Book.objects.get(book_id=review.book_id.book_id)
        except Book.DoesNotExist:
            messages.error(request, "책 정보가 없습니다.")
            return redirect('/')
            
        comments = request.POST.get('replyText', '')
        
        Reply.objects.create(
            member_id=member,
            review_id=review,
            content=comments
        )
        review.comments = Review.objects.filter(pk=review.pk).values_list('comments',flat=True)[0]+1
        review.save()
        
        print("넘어온 데이터 : ", member_id, comments)
        
        return redirect(f'/booksearch/detail/{book.book_id}/')

        
        