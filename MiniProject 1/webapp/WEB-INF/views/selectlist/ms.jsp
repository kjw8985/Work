<%@page import="miniPjoject.dao.miniProjectlist"%>
<%@page import="java.util.List"%>
<%@page import="miniPjoject.dao.miniProjectDAOimply"%>
<%@page import="miniPjoject.dao.miniProjectDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" trimDirectiveWhitespaces="true"%>
<%
List<miniProjectlist> list = (List<miniProjectlist>)request.getAttribute("list");
String category = (String)request.getParameter("category");
String restaurant = (String)request.getParameter("restaurant");
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
		<section class="ftco-section">
			<div class="container">
				<div class="row justify-content-center">
					<div class="col-md-6 text-center mb-5">
						<!-- 텍스트 자리는 앞에 선택한것에 반응시키기 -->
						<br><br>
						<h2 class="heading-section">이거먹을까?</h2>
				</div>
			</div>
				<div class="row">
					<div class="col-md-12">
						<div class="table-wrap">
							<!-- 선택시 가게될 링크 -->
							<form action= "./ms">
							<input type="hidden" name="category" value="<%= category %>">
							<input type="hidden" name="restaurant" value="<%= restaurant %>">
							<table class="table">
						  	<thead class="thead-dark">
						   		<tr>
						    		<!-- 맨위 테이블 -->
						      		<th>메뉴명</th>
						      		<th>이거 먹어야지</th>
						    	</tr>
						  	</thead>
						  	<tbody>
						  		<!-- 반복문 시작 -->
						    	<%
									for (miniProjectlist item: list){
								%>
							<tr>
								<!-- item.get~으로 반응시키기 -->
								<td><%= item.getMenu() %></td>
								<td>				
									<input type='radio'  name = 'menu' value = "<%= item.getMenu() %>"/>
								</td>
							</tr>
								<!-- 반복문 종료 -->
								<%
									}
								%>
								
								
								<input type = 'submit' class="btn btn-primary btn-lg " name='select' value= 'next' style="float: right;">
								<input type = 'submit' class="btn btn-secondary btn-lg" name='select' value= '뒤로 돌아가기' style="float: right;">
						  	</form>
							</tbody>	
							</table>
						</div>
					</div>
				</div>
			</div>
		</section>

	<script src="js/jquery.min.js"></script>
  	<script src="js/popper.js"></script>
  	<script src="js/bootstrap.min.js"></script>
  	<script src="js/main.js"></script>

	</body>
</html>