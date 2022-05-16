from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views


app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'), # 메인 페이지


    path('trade/', views.trade, name='trade'),  # 개인 게시판 연결
    path('writi/', views.trade_writi, name='trade_writi'), # 개인 게시판 글쓰기 연결
    path('result/<int:question_id>/', views.trade_board_result, name='trade_result'), # 개인 게시판 글작성 확인
    path('writi/modify/<int:question_id>/', views.trade_writi_modify, name='trade_modify'), # 개인 게시판 글수정
    path('writi/delete/<int:question_id>/', views.trade_writi_delete, name='trade_delete'), # 개인 게시판 글삭제
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'), # 개인 게시판 댓글
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'), # 개인 게시판 댓글 수정
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'), # 개인 게시판 삭제


    path('long_board/', views.longmonth_board, name='long_board'), # 전월세 게시판 가는 뷰
    path('long_writi/', views.longmonth_writi, name='long_writi'), # 전월세 게시판 글작성 뷰
    path('long_result/<int:question2_id>/', views.longmonth_board_result, name='long_result'), # 전월세 게시판 글장성 확인 뷰
    path('long_writi/modify/<int:question2_id>/', views.longmonth_writi_modify, name='long_modify'), # 전월세 게시판 글수정
    path('long_writi/delete/<int:question2_id>/', views.longmonth_writi_delete, name='long_delete'), # 전월세 게시판 삭제
    path('answer2/create2/<int:question2_id>/', views.answer_create2, name='answer_create2'), # 전월세 게시판 댓글
    path('answer2/modify2/<int:answer2_id>/', views.answer_modify2, name='answer_modify2'),  # 전월세 게시판 댓글 수정
    path('answer2/delete2/<int:answer2_id>/', views.answer_delete2, name='answer_delete2'),  # 전월세 게시판 삭제


    path('board_news/', views.board_news, name='board_news')
]