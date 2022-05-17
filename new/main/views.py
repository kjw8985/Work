from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
import folium
from folium.plugins import MarkerCluster
from .funtion import *


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
    return render(request, 'main/sub_division.html')

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
        return render(request,'main/variable_predict.html')
    
    model_result = model(locate, size) # 데이터 가져오기
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
