from django.db import models
from member.models import Member
from booksearch.models import Book

# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True) # db 설계에는 INT로 명시 
    member_id = models.ForeignKey(Member,on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    tag = models.CharField(max_length=20) 
    content = models.CharField(max_length=3000) 
    file = models.ImageField(upload_to='review_images/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)        # 좋아요 수
    comments = models.PositiveIntegerField(default=0)     # 댓글 수

    def __str__(self):
        return f"{self.Member.member_id}, {self.Book.title}"
    