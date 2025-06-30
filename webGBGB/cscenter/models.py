from django.db import models

class Notice(models.Model):
    ntcno = models.AutoField(primary_key=True)  # 기본키 등록
    id = models.CharField(max_length=100)     # 작성자
    ntitle = models.CharField(max_length=1000) # 제목
    ncontent = models.TextField()              # 내용

    nhit = models.IntegerField(default=0)      # 조회수
    nfile = models.ImageField(null=True,blank=True,upload_to='customer')
    # FileField : 모든파일 업로드 가능
    ndate = models.DateTimeField(auto_now=True)  # 현재날짜시간자동등록
    
    def __str__(self):
        return f'{self.ntcno},{self.ntitle}'
