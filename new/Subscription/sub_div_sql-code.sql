# 사용하실 db명 쓰시면됩니다
use myhome;
# 만들어두신 table명 쓰시면됩니다
ALTER TABLE testtable ADD(
    date_start DATE NOT null,
    date_finish DATE NOT null,
    size_one DECIMAL(8,4) NOT null,
    size_two DECIMAL(8,4),
    price_one CHAR(20) NOT null,
    price_two CHAR(20)
)
load data infile '여기에 csv파일경로 적으시면됩니다' into table testtable fields terminated by','; 
# 불러올 경로설정필요(미설정시 error:1290) 
# https://2dowon.netlify.app/database/error-code-1290/