from django.contrib import admin
from .models import Question, Question2, Answer, Answer2, BoardNews

class QuestionAdmin(admin.ModelAdmin):
    list_display =  ['subject', 'content', 'author', 'create_date']

class Question2Admin(admin.ModelAdmin):
    list_display =  ['subject', 'content', 'author', 'create_date']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'content', 'author', 'create_date']

class Answer2Admin(admin.ModelAdmin):
    list_display = ['question', 'content', 'author', 'create_date']

class BoardNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'datecreated']

admin.site.register(Question, QuestionAdmin)

admin.site.register(Question2, Question2Admin)

admin.site.register(Answer, AnswerAdmin)

admin.site.register(Answer2, Answer2Admin)

admin.site.register(BoardNews, BoardNewsAdmin)

