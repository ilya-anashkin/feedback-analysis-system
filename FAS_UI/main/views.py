import requests
from django.http import JsonResponse
from django.shortcuts import render

# Базовый URL для внешнего API
API_BASE_URL = "http://194.87.190.126:8000/api/feedback"

# Главная страница
def index(request):
    return render(request, 'main/home.html')

# Кнопка Start
def start(request):
    try:
        response = requests.post(f"{API_BASE_URL}/start")
        response.raise_for_status()  # Проверяем, есть ли ошибки HTTP
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({"error": f"Failed to start: {str(e)}"}, status=500)

# Кнопка Stop
def stop(request):
    try:
        response = requests.post(f"{API_BASE_URL}/stop")
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({"error": f"Failed to stop: {str(e)}"}, status=500)

# Метод Info
def info(request):
    try:
        response = requests.get(f"{API_BASE_URL}/info")
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({"error": f"Failed to get info: {str(e)}"}, status=500)
