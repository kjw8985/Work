from django.db import models


# Create your models here.
# 청약 모델 (공고 일정)
class Subscription(models.Model):
    title = models.CharField(max_length=20) # 청약하는곳 이름
    location = models.TextField() # 지역/위치
    scale = models.CharField(max_length=20) # 세대 규모
    inquiry = models.TextField() # 문의처
    tel = models.IntegerField(null=True) # 문의연락처
    Announcement_date = models.DateField() #모집공고일
    receipt_date = models.DateField() # 청약접수일
    release_date = models.DateField() # 당첨발표일
    contract_date = models.DateField() # 계약일
    division = models.CharField(max_length=20) # 청약순위자(특별, 1~2순위)
    local = models.DateField() #해당지역 접수일자
    etc = models.DateField() # 기타지역 접수일자
    Reception_place = models.CharField(max_length=10) # 접수장소
    division = models.CharField(max_length=10) # 주택구분(민영 및 기타)
    acreage = models.CharField(max_length=10, null=True) # 평형
    supply_area = models.DecimalField(max_digits=3, decimal_places=2) # 주택공급 면적
    supply_normal = models.IntegerField() #일반 공급세대수
    supply_special = models.IntegerField() # 특별 공급세대수
    supply_total = models.IntegerField() #공급계
    price = models.CharField(max_length=20, null=True) # 금액
    views = models.IntegerField() # 조회수

    def __str__(self):
        return self.title






