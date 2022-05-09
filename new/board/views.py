from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Question2, Answer
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm, AnswerForm, Question2Form
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  # 로그인한 유저만 접근가능하게 하는 클래스
from django.contrib import messages


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
            return redirect('board:result', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'board/trade_board_result.html', context)


# 개인 거래 게시판 가는 뷰
def trade(request):
    page = request.GET.get('page', '1')  # 페이지
    trade_board = Question.objects.order_by('-create_date')
    paginator = Paginator(trade_board, 5)  # 페이지당 5개씩 보여주기
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
    context = {'form': form}
    return render(request, 'board/trade_boardwriting.html', context)


# 개인거래 게시판 글삭제 뷰
def trade_writi_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('board:trade')


# 개인거래 게시판 글작성 확인 뷰
def trade_board_result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'board/trade_board_result.html', context)


# 전월세 게시판 가는뷰
def longmonth_board(request):
    page = request.GET.get('page', '1')  # 페이지
    longmonth_board = Question2.objects.order_by('-create_date')
    paginator = Paginator(longmonth_board, 5)  # 페이지당 5개씩 보여주기
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
    context = {'form': form}
    return render(request, 'board/longmonth_boardwriting.html', context)


# 전원세 게시판 글삭제
def longmonth_writi_delete(request, question2_id):
    question2 = get_object_or_404(Question2, pk=question2_id)
    question2.delete()
    return redirect('board:long_board')


# 전월세 게시판 글작성 확인 뷰
def longmonth_board_result(request, question2_id):
    question2 = get_object_or_404(Question2, pk=question2_id)
    context = {'question2': question2}
    return render(request, 'board/longmonth_board_result.html', context)