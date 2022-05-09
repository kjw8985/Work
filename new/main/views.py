from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
# 메인 페이지로 가는 뷰
# @login_required(login_url='common:login')
def index(request):
    # page = request.GET.get('page', '1')  # 페이지
    # question_list = Question.objects.order_by('-create_date')
    # paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    # page_obj = paginator.get_page(page)
    # context = {'question_list': page_obj}
    return render(request, 'index.html')

# 청약정보 가는 뷰
# @login_required(login_url='common:login')
def joomo(request):
    return render(request, 'main/sub_division.html')

# 가격변동 가는 뷰
def variable_predict(request):
    return render(request, 'main/variable_predict.html')

# 가격변동 예측결과 가는 뷰
def variable_result(request):
    return render(request, 'main/variable_result.html')

# 가격지도 가는 뷰
def averageprice(request):
    return render(request, 'main/averageprice.html')

