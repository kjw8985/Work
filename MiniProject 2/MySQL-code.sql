use myhome; # db명 적을것
create table testtable(	# 테이블 이름 설정 하면됨
	CN varchar(20) Not null,
    KR varchar(20) Not null,
    EN varchar(20) Not null,
    constraint testtable_PK primary key(CN)	# 테이블이름의 포린키는 코인의 이름으로 설정
    );
load data infile 'E:/Work/MiniProject 2/coin-data.csv' into table testtable fields terminated by','; 
# 불러올 경로, 파일 입출력 경로 설정필요(미설정시 error:1290) 