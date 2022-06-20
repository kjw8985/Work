from django import forms
from board.models import Question, Answer, Question2, Answer2, BoardNews

# 개인거래 게시판 폼
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        textarea = {
            'subject': '',
            'content': '',
        }
        
# 개인거래 게시판 댓글 폼
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        textarea = {
            'content': '',
        }

# 전월세 개시판 폼
class Question2Form(forms.ModelForm):
    class Meta:
        model = Question2  # 사용할 모델
        fields = ['subject', 'content']  # Question2Form에서 사용할 Question2 모델의 속성
        textarea = {
            'subject': '',
            'content': '',
        }

# 전월세 게시판 댓글 폼
class Answer2Form(forms.ModelForm):
    class Meta:
        model = Answer2
        fields = ['content']
        textarea = {
            'content': '',
        }

# 뉴스 게시판
class BoardNewsForm(forms.ModelForm):
    class Meta:
        model = BoardNews
        fields = ['title', 'href', 'datecreated']
        textarea = {
            'title': '',
            'href': '',
            'dataCreated': '',
        }