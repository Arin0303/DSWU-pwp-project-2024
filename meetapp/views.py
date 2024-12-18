
from django.shortcuts import render
from .models import SearchedMidpoint 
from django.conf import settings # apu 키를 사용하기 위해 모듈 임포트트
import requests

# 근처 음식점 조회하기 
def get_nearby_restaurants(latitude, longitude):
    url = "https://dapi.kakao.com/v2/local/search/category.json"
    headers = {
        "Authorization": f"KakaoAK {settings.KAKAO_API_KEY}"  # 카카오 REST API 키
    }

    params = {
        "category_group_code": "FD6",  # 음식점 코드
        "x": longitude,  # 경도
        "y": latitude,  # 위도
        "radius": 1500,  # 검색 반경 (최대 20,000m)
        "sort": "distance",  # 거리순 정렬
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        places = response.json().get('documents', [])
        return [{
            "name": place["place_name"],
            "address": place["road_address_name"] or place["address_name"],
            "distance": place["distance"],
        } for place in places]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# 근처 카페 조회하기
def get_nearby_cafe(latitude, longitude):
    url = "https://dapi.kakao.com/v2/local/search/category.json"
    headers = {
        "Authorization": f"KakaoAK {settings.KAKAO_API_KEY}"  # 카카오 REST API 키
    } 
    params = {
        "category_group_code": "CE7",  # 카페 코드
        "x": longitude,  # 경도
        "y": latitude,  # 위도
        "radius": 1500,  # 검색 반경 (최대 20,000m)
        "sort": "distance",  # 거리순 정렬
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        places = response.json().get('documents', [])
        return [{
            "name": place["place_name"],
            "address": place["road_address_name"] or place["address_name"],
            "distance": place["distance"],
        } for place in places]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


def detail(request):
    # 테스트용 세션 설정
    request.session['user_id'] = 'test1'

    # 세션에서 user_id 가져오기
    session_id = request.session.get("user_id")
    if not session_id:
        return render(request, 'result_detail.html', {'error': 'No session ID found in request'})

    # 최신 로그 조회
    latest_log = SearchedMidpoint.objects.filter(user_id=session_id).order_by('-searched_at').first()
    if not latest_log:
        return render(request, 'result_detail.html', {'error': 'No data found for this session.'})

    # 주변 장소 데이터 가져오기
    nearby_restaurants = get_nearby_restaurants(latest_log.latitude, latest_log.longitude)
    nearby_cafe = get_nearby_cafe(latest_log.latitude, latest_log.longitude)

    # 템플릿으로 데이터 렌더링
    context = {
        'place_name': latest_log.place_name,  # 중간 지점 이름
        'nearby_restaurants': nearby_restaurants,  # 근처 식당
        'nearby_cafe': nearby_cafe,  # 근처 카페
    }
    return render(request, 'result_detail.html', context)

# 테스트
latitude = 37.5665  # 서울 중심 위도
longitude = 126.9780  # 서울 중심 경도
nearby_restaurants = get_nearby_restaurants(latitude, longitude)
print("API 응답 결과:", nearby_restaurants)  # 함수 호출 결과 출력
for restaurant in nearby_restaurants:
    print(restaurant)
    if not restaurant:
        print('null')
