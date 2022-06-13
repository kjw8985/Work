from datetime import datetime, timedelta, timezone
from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse



# 개인거래 게시판 모델
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    hit = models.PositiveIntegerField(null=True, blank=True, default=0)
    imgfile = models.FileField(upload_to='Uploaded_Files/%y/%m/%d/',blank=True)
    uploadDate = models.DateField(auto_now = True)

    def __str__(self):
        return self.subject

    @property
    def question_created_string(self):
        time = datetime.now(tz=timezone.utc) - self.create_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.create_date.date()
            return str(time.days) + '일 전'
        else:
            return False

# 개인 게시판 댓글 모델
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content

#   전월세 게시판 모델
class Question2(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    hit = models.PositiveIntegerField(null=True, blank=True, default=0)
    longmonth_img = models.FileField(upload_to='Uploaded_Files/%y/%m/%d/',blank=True)
    uploadDate = models.DateField(auto_now = True)

    def __str__(self):
        return self.subject
    
    @property
    def question2_created_string(self):
        time = datetime.now(tz=timezone.utc) - self.create_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.create_date.date()
            return str(time.days) + '일 전'
        else:
            return False
# 전월세 게시판 댓글 모델
class Answer2(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question2, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content

# 뉴스 게시판
class BoardNews(models.Model):
    title = models.CharField(max_length=80, null=False)
    href = models.CharField(max_length=200, null=False)
    datecreated = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.title

