from django.db import models
import requests
from django.conf import settings  # API 키를 가져오기 위해 필요

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)  # 아이디(pk)
    user_pw = models.IntegerField(null=False)  # 비밀번호

    def __str__(self):
        return self.user_id


class SearchedMidpoint(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='searched_midpoints')  # 아이디(fk)
    latitude = models.FloatField()  # 위도
    longitude = models.FloatField()  # 경도
    searched_at = models.DateTimeField(auto_now_add=True)  # 조회 날짜 및 시간
    place_name = models.CharField(max_length=255, blank=True, null=True)  # 장소명

    # 오버라이드
    def save(self, *args, **kwargs):
        if not self.place_name:
            self.place_name = self.get_place_name()
        super().save(*args, **kwargs) # 부모 클래스인 models.Model의 save() 호출되면서 객체의 데이터가 데이터베이스에 저장됨

    def get_place_name(self):
        """카카오맵 Reverse Geocoding API를 사용해 위도, 경도로 장소명 반환"""
        api_key = settings.KAKAO_API_KEY  # settings.py에 저장된 API 키
        headers = {
            "Authorization": f"KakaoAK {api_key}"  # 카카오 API 인증 헤더
        }
        url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
        params = {
            "x": self.longitude,  # 경도
            "y": self.latitude,   # 위도
            "input_coord": "WGS84"  # 입력 좌표계 (기본값: WGS84)
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['documents']:
                address_info = data['documents'][0]['address']
                return address_info['address_name']  # 주소 반환
        return "알 수 없는 위치"

    def __str__(self):
        return f"{self.place_name} (at {self.latitude}, {self.longitude} on {self.searched_at})"
