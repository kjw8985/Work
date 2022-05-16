from django.db import models
from django.contrib.auth.models import User

# 개인거래 게시판 모델
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

# 개인 게시판 댓글 모델
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

#   전월세 게시판 모델
class Question2(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

# 전월세 게시판 댓글 모델
class Answer2(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question2, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

# 뉴스 게시판
class BoardNews(models.Model):
    title = models.CharField(max_length=80, null=False)
    href = models.CharField(max_length=200, null=False)
    datecreated = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.title

