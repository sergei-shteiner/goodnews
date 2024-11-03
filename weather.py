import requests
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
api_key = os.getenv("OPENWEATHERMAP_API_KEY")

def get_coordinates(city_name, api_key):
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': city_name,
        'limit': 1,
        'appid': api_key
    }
    
    response = requests.get(geocoding_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            print("Stadt nicht gefunden. Bitte überprüfen Sie die Eingabe.")
            return None, None
    else:
        print(response.json())
        print("Fehler beim Abrufen der Koordinaten.")
        return None, None

def get_weather_by_location(lat, lon, api_key):
    weather_url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly,daily,alerts',  # nur das aktuelle Wetter abrufen
        'appid': api_key,
        'units': 'metric',  # Temperatur in Grad Celsius
        'lang': 'de'  # Sprache der Beschreibung
    }
    
    response = requests.get(weather_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        current = data['current']
        weather_description = current['weather'][0]['description']
        temperature = current['temp']
        return f"{weather_description.capitalize()}, {int(temperature)}°C"
    else:
        raise ValueError("Weird weather!")

def get_weather(location_name):
    city_name = f"{location_name},Deutschland"
    lat, lon = get_coordinates(city_name, api_key)
    return get_weather_by_location(lat, lon, api_key)
