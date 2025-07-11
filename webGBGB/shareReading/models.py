from django.db import models
from member.models import Member
from booksearch.models import Book

class ReadingGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    max_member = models.IntegerField(default=2)
    admin = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='reading_owned_groups')  # 세션아이디 로그인중인 유저로 방장 설정
    member = models.ManyToManyField(Member,related_name='reading_reading_groups')  # 방장 제외 나머지 멤버가 들어옴, null이어도 ok
    description = models.TextField()
    tag = models.CharField(max_length=100,null=True,blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,default=1, related_name='reading_owned_groups')
    is_public = models.IntegerField(default=0)
    password = models.IntegerField(default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.group_id}, {self.group_name}'