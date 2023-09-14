from django.shortcuts import render, HttpResponse
from .api_config import DATA_TOKEN, WEATHER_TOKEN
import requests, json

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    # Getting client's IP adress
    ip = get_client_ip(request)

    # Requesting client's city by IP from API
    params = {"token": DATA_TOKEN}
    try:
        city = requests.get(f'https://ipinfo.io/{ip}', params=params).json()['city']
    except:
        city = 'Moscow'
    # Requesting weather forecast for specific city for 3 days
    querystring = {"q":city,"days":"3"}
    headers = {
        "X-RapidAPI-Key": WEATHER_TOKEN,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.get("https://weatherapi-com.p.rapidapi.com/forecast.json", headers=headers, params=querystring).json()
    forecast = response['forecast']['forecastday']
    context = {'days': forecast, 'city': city}
    return render(request, 'index.html', context)
