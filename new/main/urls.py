from django.urls import path
from . import views
# from board.views import *
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('joomo/',views.joomo, name='joomo'), # 청약분양
    path('common/', TemplateView.as_view(template_name='signup.html')), # 회원가입
    path('variable_pd/', views.variable_predict, name='variable_pd'), # 가격변동
    path('variable_rs/', views.variable_result, name='variable_rs'), # 가격변동 결과
    path('averageprice/', views.averageprice, name='avg'), #
    #path('board/', TemplateView.as_view(template_name='trade_boardwriting.html')),
]





