from turtle import update
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from board import models
from .models import Question, Question2, Answer, Answer2, BoardNews
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm, AnswerForm, Question2Form, Answer2Form, BoardNewsForm
from django.core.paginator import Paginator
from main.models import Subscription
from django.contrib.auth.decorators import login_required  # 로그인한 유저만 접근가능하게 하는 클래스
from django.contrib import messages
from django.db.models import F
from datetime import datetime, timedelta

# 메인 페이지 뷰 (게시판 글 표시 함수)
def index(request):
    page = request.GET.get('page2', '1')  # 페이지
    page2 = request.GET.get('page3', '1')
    question = Question.objects.all()
    question2 = Question2.objects.all()
    boardnews = BoardNews.objects.all()
    trade_board = Question.objects.order_by('-create_date')
    longmonth_board = Question2.objects.order_by('-create_date')
    paginator = Paginator(trade_board, 5)   # 페이지당 5개씩 보여주기
    paginator2 = Paginator(longmonth_board, 5)
    page_obj = paginator.get_page(page)
    page_obj2 = paginator2.get_page(page2)
    page3 = request.GET.get('page1', '1')
    board_news = BoardNews.objects.order_by('-id')
    paginator3 = Paginator(board_news, 5)
    page_obj3 = paginator3.get_page(page3)
    page4 = request.GET.get('page4', '1')
    subscription =  Subscription.objects.all()
    subscription_board = Subscription.objects.order_by('-id')
    paginator4 = Paginator(subscription_board, 5)
    page_obj4 = paginator4.get_page(page4)
    context = {'trade_board': page_obj, 'longmonth_board': page_obj2, ' question': question, 'question2': question2, 'board_news': page_obj3, 'boardnews': boardnews,
               'subscription_board':page_obj4,'subscription': subscription}
    return render(request, 'board/index.html', context)


########################################################################################################################
########################################################################################################################


# 개인 거래 게시판 가는 뷰
def trade(request):
    page = request.GET.get('page', '1')  # 페이지
    trade_board = Question.objects.order_by('-create_date')
    paginator = Paginator(trade_board, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'trade_board': page_obj}
    return render(request, 'board/trade_board.html', context)


# 개인거래 게시판 글작성 가는 뷰
@login_required(login_url='common:login')
def trade_writi(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.imgfile = request.FILES.get('imgfile','')
            question.create_date = timezone.now()
            question.save()
            return redirect('board:trade')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'board/trade_boardwriting.html', context)


# 개인거래 게시판 글수정 뷰
@login_required(login_url='common:login')
def trade_writi_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('board:trade_result', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'question': question, 'form': form}
    return render(request, 'board/trade_board_modify.html', context)


@login_required(login_url= 'common:login')
# 개인거래 게시판 글삭제 뷰
def trade_writi_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('board:trade')


# 개인거래 게시판 댓글 뷰
@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    board 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('board:trade_result', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'board/trade_board_result.html', context)




# 개인거래 댓글 수정 뷰
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('board:treade_result', question_id=answer.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('board:trade_result', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'board/trade_board_answer_modify.html', context)


# 개인거래 댓글 삭제 뷰
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('board:trade_result', question_id=answer.question.id)


# 개인거래 게시판 글작성 확인 뷰
def trade_board_result(request, question_id):
    answer = Answer.objects.filter(question_id=question_id).order_by('-create_date')
    page = request.GET.get('page', '1')  # 페이지
    paginator = Paginator(answer, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == "GET":
        context = {'question': question, 'answer': answer, 'answer': page_obj}
        q_id : str = str(question_id)
        # 로그인 한 경우
        if request.user.is_authenticated is True:
            cookie_hits_key = f'hits_{request.user.id}'
        # 비로그인 경우
        else:
            cookie_hits_key = 'hits_0'

         # 쿠키로부터 방문기록 로드
        cookie_hits_value: str = request.COOKIES.get(cookie_hits_key, '')
        # 쿠키에 cookie_hits_key 항목이 있는 경우
        if cookie_hits_value != '':
            q_id_list = cookie_hits_value.split('|')
            # 방문한 경우는 그대로 응답
            if q_id in q_id_list:
                return render(request, 'board/trade_board_result.html', context)
            # 방문하지 않은 경우
            else:
                new_hits_dict = (cookie_hits_key, cookie_hits_value+f'|{q_id}')
                question.hit = F('hit') + 1
                question.save()
                question.refresh_from_db()
        # hits 가 없는 경우
        else:
            new_hits_dict = (cookie_hits_key, q_id)
            question.hit = F('hit') + 1
            question.save()
            question.refresh_from_db()

        response = render(request, 'board/trade_board_result.html', context)
        # 만료시간 설정
        midnight_kst = datetime.replace(datetime.utcnow() + timedelta(days=1, hours=9), hour=0, minute=0, second=0)
        midnight_kst_to_utc = midnight_kst - timedelta(hours=9)

        response.set_cookie(*new_hits_dict,
                            expires=midnight_kst_to_utc,
                            # secure=True,
                            httponly=True,
                            samesite='Strict')
        return response
    context = {'question': question, 'answer': answer, 'answer': page_obj}
    return render(request, 'board/trade_board_result.html', context)


########################################################################################################################
########################################################################################################################


# 전월세 게시판 가는뷰
def longmonth_board(request):
    page = request.GET.get('page', '1')  # 페이지
    longmonth_board = Question2.objects.order_by('-create_date')
    paginator = Paginator(longmonth_board, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'longmonth_board': page_obj}
    return render(request, 'board/longmonth_board.html', context)


@login_required(login_url='common:login')
# 전월세 게시판 작성 뷰
def longmonth_writi(request):
    if request.method == 'POST':
        form = Question2Form(request.POST)
        if form.is_valid():
            question2 = form.save(commit=False)
            question2.author = request.user
            question2.longmonth_img = request.FILES.get('longmonth_img','')
            question2.create_date = timezone.now()
            question2.save()
            return redirect('board:long_board')
    else:
        form = Question2Form()
    context = {'form': form}
    return render(request, 'board/longmonth_boardwriting.html', context)


# 전월세 게시판 글수정 뷰
def longmonth_writi_modify(request, question2_id):
    question2 = get_object_or_404(Question2, pk=question2_id)
    if request.method == 'POST':
        form = Question2Form(request.POST, instance=question2)
        if form.is_valid():
            question2 = form.save(commit=False)
            question2.modify_date = timezone.now()
            question2.save()
            return redirect('board:long_result', question2_id=question2.id)
    else:
        form = Question2Form(instance=question2)
    context = {'question2':question2,'form': form}
    return render(request, 'board/longmonth_board_modify.html', context)


# 전원세 게시판 글삭제 뷰
def longmonth_writi_delete(request, question2_id):
    question2 = get_object_or_404(Question2, pk=question2_id)
    question2.delete()
    return redirect('board:long_board')


@login_required(login_url='common:login')
# 전월세 게시판 댓글 뷰
def answer_create2(request, question2_id):
    """
    board 답변등록
    """
    question2 = get_object_or_404(Question2, pk=question2_id)
    if request.method == 'POST':
        form = Answer2Form(request.POST)
        if form.is_valid():
            answer2 = form.save(commit=False)
            answer2.author = request.user    # author 속성에 로그인 계정 저장
            answer2.create_date = timezone.now()
            answer2.question = question2
            answer2.save()
            return redirect('board:long_result', question2_id=question2.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question2': question2, 'form': form}
    return render(request, 'board/longmonth_board_result.html', context)


# 전월세 게시판 댓글 수정 뷰
def answer_modify2(request, answer2_id):
    answer2 = get_object_or_404(Answer2, pk=answer2_id)
    if request.user != answer2.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('board:long_result', question2_id=answer2.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer2)
        if form.is_valid():
            answer2 = form.save(commit=False)
            answer2.modify_date = timezone.now()
            answer2.save()
            return redirect('board:long_result', question2_id=answer2.question.id)
    else:
        form = AnswerForm(instance=answer2)
    context = {'answer2': answer2, 'form': form}
    return render(request, 'board/longmonth_board_answer_modify.html', context)


# 개인거래 댓글 삭제 뷰
def answer_delete2(request, answer2_id):
    answer2 = get_object_or_404(Answer2, pk=answer2_id)
    answer2.delete()
    return redirect('board:long_result', question2_id=answer2.question.id)


# 전월세 게시판 글작성 확인 뷰
def longmonth_board_result(request, question2_id):

    answer2 = Answer2.objects.filter(question_id=question2_id).order_by('-create_date')
    page = request.GET.get('page', '1')  # 페이지
    paginator = Paginator(answer2, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)
    question2 = get_object_or_404(Question2, pk=question2_id)
    if request.method == "GET":
        context = {'question2': question2, 'answer2': answer2, 'answer2': page_obj}
        q_id : str = str(question2_id)
        # e로그인 한 경우
        if request.user.is_authenticated is True:
            cookie_hits_key = f'hits_{request.user.id}'
        # 비로그인 경우
        else:
            cookie_hits_key = 'hits_0'

         # 쿠키로부터 방문기록 로드
        cookie_hits_value: str = request.COOKIES.get(cookie_hits_key, '')
        # 쿠키에 cookie_hits_key 항목이 있는 경우
        if cookie_hits_value != '':
            q_id_list = cookie_hits_value.split('|')
            # 방문한 경우는 그대로 응답
            if q_id in q_id_list:
                return render(request, 'board/longmonth_board_result.html', context)
            # 방문하지 않은 경우
            else:
                new_hits_dict = (cookie_hits_key, cookie_hits_value+f'|{q_id}')
                question2.hit = F('hit') + 1
                question2.save()
                question2.refresh_from_db()
        # hits 가 없는 경우
        else:
            new_hits_dict = (cookie_hits_key, q_id)
            question2.hit = F('hit') + 1
            question2.save()
            question2.refresh_from_db()

        response = render(request, 'board/longmonth_board_result.html', context)
        # 만료시간 설정
        midnight_kst = datetime.replace(datetime.utcnow() + timedelta(days=1, hours=9), hour=0, minute=0, second=0)
        midnight_kst_to_utc = midnight_kst - timedelta(hours=9)

        response.set_cookie(*new_hits_dict,
                            expires=midnight_kst_to_utc,
                            # secure=True,
                            httponly=True,
                            samesite='Strict')
        return response
    
    context = {'question2': question2, 'answer2': answer2, 'answer2':page_obj}
    return render(request, 'board/longmonth_board_result.html', context)


###############################################################################
###############################################################################

def board_news(request):
    page = request.GET.get('page', '1')
    board_news = BoardNews.objects.order_by('-id')
    paginator = Paginator(board_news, 12)
    page_obj = paginator.get_page(page)
    context = {'board_news': page_obj}
    return render(request, 'board/news_board.html', context)



