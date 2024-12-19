from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.conf import settings
from .models import SearchedMidpoint

KAKAO_API_KEY = settings.KAKAO_API_KEY  # Kakao API Key를 settings에서 불러오기

# 도시별 위도, 경도 정보 (예시)
city_coordinates = {
    '서울': (37.5665, 126.9780),  # 서울의 위도, 경도
    '대구': (35.8717, 128.6014),  # 대구의 위도, 경도
    '부산': (35.1796, 129.0756),  # 부산의 위도, 경도
}

# 중간지점 계산 함수 (위도, 경도 기반)
def calculate_midpoint_coordinates(coordinates):
    latitudes = [coord[0] for coord in coordinates]
    longitudes = [coord[1] for coord in coordinates]
    return sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)

# 장소의 위도, 경도 정보를 가져오는 함수 (카카오 API 사용)
def get_coordinates(location_name):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": location_name}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        documents = response.json().get("documents", [])
        if documents:
            return float(documents[0]["y"]), float(documents[0]["x"])
    return None

# 기본 화면 (출발지 입력 페이지)
def index(request):
    return render(request, 'main.html')

# 결과 페이지 (위치 정보 기반 중간지점 계산)
def result(request):
    if request.method == "POST":
        # 사용자가 입력한 장소를 받아옴
        locations = request.POST.get("locations", "").split(",")
        locations = [location.strip() for location in locations]  # 공백 제거
        
        # 각 장소의 위도, 경도를 가져옴
        coordinates = [get_coordinates(location) for location in locations]
        
        # 만약 하나라도 위도, 경도를 가져올 수 없으면 오류 메시지 출력
        if None in coordinates:
            return render(request, "result.html", {"error": "위치 정보를 가져올 수 없습니다."})
        
        # 중간지점 계산
        midpoint = calculate_midpoint_coordinates(coordinates)
        
        # 결과를 dictionary 형태로 준비
        results = [{"name": location, "lat": lat, "lng": lng} for location, (lat, lng) in zip(locations, coordinates)]
        results.append({"name": "중간지점", "lat": midpoint[0], "lng": midpoint[1]})
        
        # 템플릿에 결과와 카카오 API 키를 전달
        return render(request, "result.html", {"results": results, "kakao_api_key": settings.KAKAO_API_KEY})
    
    # GET 요청일 경우 기본 화면
    return render(request, "result.html")

# 결과 상세 페이지 (특정 장소에 대한 정보 제공)
def result_detail(request, location):
    results = {
        '서울': {'lat': 37.5665, 'lng': 126.9780},
        '부산': {'lat': 35.1796, 'lng': 129.0756},
    }
    result = results.get(location)
    if result:
        return render(request, 'result_detail.html', {'result': result, 'location': location})
    else:
        return HttpResponse("해당 장소에 대한 결과가 없습니다.")

# 중간 장소 기록 페이지
def midpoint_list(request):
    midpoints = SearchedMidpoint.objects.all().order_by('-searched_at')  # 조회 날짜 기준 내림차순 정렬
    context = {
        'midpoints': midpoints
    }
    return render(request, 'profile.html', context)
