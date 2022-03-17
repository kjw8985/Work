<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>먹고 싶은 음식 종류</title>
<!-- bootstrap css위치명시 -->
<link rel="stylesheet"
	href="resource/css/bootstrap.min.css">
</head>
<body>
	<style>
		.navbar-brand {font-size :38px}
		.fv {text-align: center; font-size : 30px}
		.button{width: 20px; height:20px}
	</style>
	<nav class="navbar navbar-dark bg-dark">
  		<div class="container-fluid">
    	<a class="navbar-brand" >오늘 먹고 싶은 음식 종류는?</a><br>  
    	</div>
	</nav>
	<br><br>
	<form action = "./fs">
		<div class="container marketing">
			<input type = 'submit' class="btn btn-primary btn-lg " name='select' value= '너로 정했다' style="float: right;">
			<input type = 'submit' class="btn btn-secondary btn-lg" name='select' value= '뒤로 돌아가기' style="float: right;">
			<br><br><br>
    		<div class="row">
      			<div class="col-lg-4">
        			<img src = "image/krfood.jpg" class="bd-placeholder-img rounded-circle" width="140" height="140">
        			<h2><input class = button type='radio' name='category' value='한식' checked/>한식</h2>
        			<p>한국식 음식점이 땡겨요</p>
        			<br>
     			</div>
      
      			<div class="col-lg-4">
        			<img src = "image/usfood.jpg" class="bd-placeholder-img rounded-circle" width="140" height="140">
        			<h2><input class = button type='radio' name='category' value='양식' />양식</h2>
        			<p>서양식 음식점이 땡겨요</p>
        			<br>
      			</div>
      
      			<div class="col-lg-4">
        			<img src = "image/jpfood.jpg" class="bd-placeholder-img rounded-circle" width="140" height="140">
        			<h2><input class = button type='radio' name='category' value='일식' />일식</h2>
        			<p>일본식 음식점이 땡겨요</p>
        			<br>
      			</div>
      
      			<div class="col-lg-4">
        			<img src = "image/cnfood.jpg" class="bd-placeholder-img rounded-circle" width="140" height="140">        
        			<h2><input class = button type='radio' name='category' value='중식' />중식</h2>
        			<p>중국식 음식점이 땡겨요</p>
        			<br>
      			</div>
      			</div>
    		</div>
  		</div>
	</form>
</body>
</html>