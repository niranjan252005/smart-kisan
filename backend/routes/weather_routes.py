from flask import Blueprint, request
import requests
import os

weather_bp = Blueprint("weather", __name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Use OpenWeather API

@weather_bp.route("/current", methods=["POST"])
def weather():
    data = request.json
    city = data["city"]

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    return {
        "temperature": response["main"]["temp"],
        "humidity": response["main"]["humidity"],
        "weather": response["weather"][0]["description"]
    }
