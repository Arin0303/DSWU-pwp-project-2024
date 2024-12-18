from django.shortcuts import render

import requests
from django.shortcuts import render
from django.http import JsonResponse

KAKAO_API_KEY = "60163a9f4b787569bf83789a6a5263be"  # Kakao API Key

# 출발지 입력 페이지
def index(request):
    return render(request, 'main.html')

# 좌표를 받아와서 결과 페이지로 넘김
def result(request):
    if request.method == "POST":
        addresses = request.POST.getlist('addresses[]')  # 입력된 주소들
        results = []

        for address in addresses:
            url = f"https://dapi.kakao.com/v2/local/search/address.json?query={address}"
            headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data['documents']:
                    coords = data['documents'][0]
                    lat = coords['y']  # 위도
                    lng = coords['x']  # 경도
                    results.append({'address': address, 'lat': lat, 'lng': lng})
                else:
                    results.append({'address': address, 'error': '변환 실패'})
            else:
                results.append({'address': address, 'error': 'API 호출 실패'})

        # 결과 페이지 렌더링
        return render(request, 'result.html', {'results': results})

    return JsonResponse({'error': '잘못된 요청입니다.'})