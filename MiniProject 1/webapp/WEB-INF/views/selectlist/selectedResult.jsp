<%@page import="java.sql.SQLException"%>
<%@page import="java.util.ArrayList"%>
<%@page import="miniPjoject.dao.miniProjectlist"%>
<%@page import="miniPjoject.dao.miniProjectDAOimply"%>
<%@page import="miniPjoject.dao.miniProjectDAO"%>
<%@page import="java.sql.PreparedStatement"%>
<%@page import="java.sql.ResultSet"%>
<%@page import="java.sql.Connection"%>
<%@page import="java.util.List"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
List<miniProjectlist> list = (List<miniProjectlist>)request.getAttribute("list");
String category = (String)request.getParameter("category");
String restaurant = (String)request.getParameter("restaurant");
String menu = (String)request.getParameter("menu");
String Polls = (String)request.getParameter("polls");
List<miniProjectlist> countOfPolls = (List<miniProjectlist>)request.getAttribute("countOfPolls");
List<miniProjectlist> specification = (List<miniProjectlist>)request.getAttribute("specification");
%>
<!doctype html>
<html lang="en">
  	<head>
  		<title>음식점 선택</title>
    	<meta charset="utf-8">
    	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    	<link rel="stylesheet" href="resource/css/bootstrap.min.css">
		<link href='https://fonts.googleapis.com/css?family=Roboto:400,100,300,700' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">	
		<link rel="stylesheet" href="css/style.css">
	</head>
	<body>
		<style>
			p {text-align: center; font-size : 35px}
			span {text-align : center; font-size : 30px}
		</style>
		<!-- 음식점 정보 -->
		<section class="ftco-section">
			<div class="container">
				<div class="row justify-content-center">
					<div class="col-md-6 text-center mb-5">
						<!-- 텍스트 자리는 앞에 선택한것에 반응시키기 -->
						<br><br>
						<h2 class="heading-section">가장 인기있는 메뉴</h2>
				</div>
			</div>
				<div class="row">
					<div class="col-md-12">
						<div class="table-wrap">
							<!-- 선택시 가게될 링크 -->
							<table class="table">
						  	<thead class="thead-dark">
						   		<tr>
						    		<th>음식종류</th>
						    		<th>음식점이름</th>
						      		<th>메뉴명</th>
						      		<th>가격</th>
						      		<th>네이버리뷰수</th>
						      		<th>투표받은수</th>
						    	</tr>
						  	</thead>
						  	<tbody>
						  		<!-- 반복문 시작 -->
						    	<%
									for (miniProjectlist item: list){
								%>
							<tr>
								<!-- item.get~으로 반응시키기 -->
								<td><%= item.getCategory() %></td>
								<td><%= item.getRestaurant() %></td>
								<td><%= item.getMenu() %></td>
								<td><%= item.getPrice() %></td>
								<td><%= item.getReviews() %></td>
								<td><%= item.getPolls() %></td>
							</tr>
								<!-- 반복문 종료 -->
								<%
									}
								%>
							</tbody>	
							</table>
						</div>
					</div>
				</div>
			</div>
		</section>
		<br><br>
		
		<p><a href="./index.html" >뒤로 돌아가기</a>

</body>
</html>