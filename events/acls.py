from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json


def get_photo(city):
    header = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": f"{city}"
    }
    url = "https://api.pexels.com/v1/search?"
    response = requests.get(url, params=params, headers=header)
    content = json.loads(response.content)
    return {"images_url": content["photos"][0]["src"]["original"]}


def get_weather_data(city, state):
    params = {
        "q": f"{city},{state},US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    url = "http://api.openweathermap.org/geo/1.0/direct"
    response = requests.get(url, params=params)
    content = response.json()

    try:
        latitude = content[0]["lat"]
        longitude = content[0]["lon"]

    except (KeyError, IndexError):
        return None

    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }

    response = requests.get(weather_url, params=weather_params)
    content = response.json()

    try:
        description = content["weather"][0]["description"]
        temp = content["main"]["temp"]
    except (KeyError, IndexError):
        return None
    return {"description": description, "temp": temp}
