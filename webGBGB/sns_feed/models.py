from django.db import models
from django.conf import settings


class GroupChatRoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_members = models.IntegerField(default=10)
    current_members = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author.username} in {self.group.name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # 필요한 경우 추가 필드 (예: bio, website 등)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Like(models.Model):
    """
    사용자가 게시글에 '좋아요'를 누른 것을 기록하는 모델.
    한 사용자가 한 게시글에 중복으로 좋아요를 누를 수 없도록 unique_together 제약을 설정합니다.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 한 사용자가 한 게시글에 한 번만 좋아요를 누를 수 있도록 중복 방지 제약
        unique_together = ('user', 'post')
        # Django Admin 등에서 보여질 때 'Like' 대신 '좋아요'로 표시
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'

    def __str__(self):
        # 게시글 내용이 너무 길면 잘라서 표시
        post_content_snippet = self.post.content[:20] + "..." if len(self.post.content) > 20 else self.post.content
        return f"{self.user.username} liked '{post_content_snippet}'"