from django.views.generic import ListView
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
search = True
def joomo(request):
    page = request.GET.get('page', '1')
    page1 = request.GET.get('page1', '1')
    subscription =  Subscription.objects.all()
    subscription_board = Subscription.objects.order_by('-date_start')
    paginator = Paginator(subscription_board, 7)
    page_obj = paginator.get_page(page)
    
    global search
    
    if (search != request.POST.get('search',False)) and (type(request.POST.get('search',False)) != type(True)): # 다른 검색값이 나오면 검색어 변경
        search = request.POST.get('search',False) 
    if type(search)==type(True) :                  # 검색값이 없으면 검색어 변경
        search = request.POST.get('search',False)
    print(' type(search) : ',type(search))
    if type(search)!=type(True) :                  # 검색값이 있으면 검색된 내용 표시
        subscription1 = search1(search)
        subscription_board = subscription1 #sorted(subscription1,key=lambda x:x[3], reverse=True)
        print('검색페이지가 출력 : type(search) : ',type(search))
        paginator = Paginator(subscription_board, 7)
        page_obj = paginator.get_page(page1)
        print(page1)
        context1 = {'subscription_board1':page_obj,'subscriptions': subscription1, 'search_':'search_'}
        #print('검색 결과',subscription1)
        return render(request, 'main/sub_division.html', context1)
    
    else:
        context = {'subscription_board':page_obj,'subscription': subscription, 'nosearch_':'nosarch_'}
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

#def search(request):
#    #type과 search
    #type = request.POST['type']
#    search = request.POST['search']
    
#    print('POST 결과 출력', search)
#    return render(request, 'main/sub_division.html')


'''
# 청약정보 검색기능
class NoticeListView(ListView):
    model = Subscription
    paginate_by = 15
    template_name = 'main/sub_division.html'         #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'main_list'        #DEFAULT : <app_label>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q','')
        search_keyword.encoding = 'euc-kr'        
        search_type = self.request.GET.get('type','')
        main_list = Subscription.objects.all()#.order_by('-id')
        print('main_list : ',main_list)
        print('subscription : ',Subscription)
        print('keyword type : ', type(search_keyword))
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_notice_list = main_list.filter(Q (title__icontains=search_keyword) | Q (location__icontains=search_keyword) | Q (Announcement_date__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_notice_list = main_list.filter(Q (title__icontains=search_keyword) | Q (location__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = main_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_notice_list = main_list.filter(location__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_notice_list = main_list.filter(Announcement_date__icontains=search_keyword)

                # if not search_notice_list :
                #     messages.error(self.request, '일치하는 검색 결과가 없습니다.')
                messages.error(self.request, '잘했어요')
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return main_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        notice_fixed = Subscription.objects.filter(top_fixed=True).order_by('-registered_date')

        if len(search_keyword) > 1 :
            context['q'] = search_keyword
        context['type'] = search_type
        context['notice_fixed'] = notice_fixed

        return context
'''