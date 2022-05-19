from django.shortcuts import render
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
import folium
from folium.plugins import MarkerCluster
from .funtion import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from main.models import Subscription
from django.contrib.auth.decorators import login_required  # 로그인한 유저만 접근가능하게 하는 클래스
from django.contrib import messages
from django.db.models import Q 

# # Create your views here.
# # 메인 페이지로 가는 뷰
# # @login_required(login_url='common:login')
# def index(request):
#     # page = request.GET.get('page', '1')  # 페이지
#     # question_list = Question.objects.order_by('-create_date')
#     # paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
#     # page_obj = paginator.get_page(page)
#     # context = {'question_list': page_obj}
#     return render(request, 'index.html')

# 청약정보 가는 뷰
# @login_required(login_url='common:login')
def joomo(request):
    page = request.GET.get('page', '1')
    subscription =  Subscription.objects.all()
    subscription_board = Subscription.objects.order_by('-id')
    paginator = Paginator(subscription_board, 7)
    page_obj = paginator.get_page(page)
    context = {'subscription_board':page_obj,'subscription': subscription}
    return render(request, 'main/sub_division.html', context)

# 가격변동 가는 뷰
def variable_predict(request):
    return render(request, 'main/variable_predict.html')

# 가격변동 예측결과 가는 뷰
def variable_result(request):
    reset_dir() # 폴더 초기화
    
    locate = request.POST['locate']
    size = request.POST['size']
    print(locate, size)
    if len(locate)==0 or len(size)==0:
        context = {"alert":'평형대와 주소값을 입력하세요.'}
        return render(request,"main/variable_predict.html", context)
    
    model_result = model(locate, size) # 데이터 가져오기
    if model_result==0:
        context = {"alert":'잘못된 주소값을 입력하였습니다.'}
        return render(request,"main/variable_predict.html", context)
    model_result = model_result + (locate, size)
    print(model_result)
    context = {'model' : model_result}
    return render(request, 'main/variable_result.html', context)

# 가격지도 가는 뷰
def averageprice(request):
    return render(request, 'main/averageprice.html')

def map_html(request):
    month = request.POST['month']
    size = request.POST['size']
    # value값이 넘어온다.
    print(month, size)
    m = foliumMap(month, size)
    maps=m._repr_html_()
    context = {'map':maps}
    return render(request, 'main/map.html',context)

# 청약정보 검색기능
def sub_search(request):
    return render(request, 'main/sub_search.html')

def get_queryset(self):
    search_keyword = self.request.GET.get('q', '')
    search_type = self.request.GET.get('type', '')
    notice_list = Subscription.objects.order_by('location') 
    
    if search_keyword :
        if len(search_keyword) > 1 :
            if search_type == 'all':
                search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
            elif search_type == 'title_content':
                search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))

            return search_notice_list
        else:
            messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
    return notice_list

def get_context_data(self, **kwargs):
    search_keyword = self.request.GET.get('q', '')
    search_type = self.request.GET.get('type', '')

    if len(search_keyword) > 1 :
        context['q'] = search_keyword
    context['type'] = search_type

    return context