"""Weather Service for SmartFarmingAI"""

import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
import random

from backend.config import settings
from backend.services.cache_service import cache_result

logger = logging.getLogger(__name__)


@cache_result(ttl=1800, key_prefix="weather:current")  # Cache for 30 mins
async def get_weather_data(city: str = None, location: str = None) -> Dict[str, Any]:
    """Fetch current weather data from OpenWeatherMap or provide realistic mock data."""
    city = city or settings.DEFAULT_CITY
    
    if not settings.ENABLE_REAL_TIME_WEATHER or not settings.WEATHER_API_KEY:
        logger.warning("Weather API disabled or key missing. Using mock data.")
        return get_mock_weather_data(city, location)
    
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "description": data["weather"][0]["description"].capitalize(),
                        "wind_speed": data["wind"]["speed"],
                        "pressure": data["main"]["pressure"],
                        "city": data["name"],
                        "location": location or settings.DEFAULT_LOCATION,
                        "real_time": True,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    logger.error(f"Weather API error: {response.status}")
                    return get_mock_weather_data(city, location)
                    
    except Exception as e:
        logger.error(f"Weather API exception: {str(e)}")
        return get_mock_weather_data(city, location)


@cache_result(ttl=7200, key_prefix="weather:forecast")  # Cache for 2 hours
async def get_weather_forecast(city: str = None, days: int = 7) -> List[Dict[str, Any]]:
    """Fetch weather forecast for next N days from OpenWeatherMap."""
    city = city or settings.DEFAULT_CITY
    
    if not settings.ENABLE_REAL_TIME_WEATHER or not settings.WEATHER_API_KEY:
        return get_mock_forecast(city, days)
        
    try:
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    # OpenWeatherMap 5-day forecast returns data every 3 hours
                    # We'll group them by day and take a representative point (noon)
                    daily_forecasts = []
                    today = datetime.now().strftime("%Y-%m-%d")
                    
                    seen_days = set()
                    for item in data["list"]:
                        date_str = item["dt_txt"].split(" ")[0]
                        hour = item["dt_txt"].split(" ")[1]
                        
                        if date_str != today and date_str not in seen_days and "12:00:00" in hour:
                            daily_forecasts.append({
                                "date": date_str,
                                "temperature": item["main"]["temp"],
                                "humidity": item["main"]["humidity"],
                                "description": item["weather"][0]["description"].capitalize(),
                                "rain_probability": int(item.get("pop", 0) * 100),
                                "wind_speed": item["wind"]["speed"]
                            })
                            seen_days.add(date_str)
                    
                    return daily_forecasts if daily_forecasts else get_mock_forecast(city, days)
                else:
                    return get_mock_forecast(city, days)
    except Exception:
        return get_mock_forecast(city, days)


def get_mock_weather_data(city: str, location: str = None) -> Dict[str, Any]:
    """Provides realistic mock weather data with time-based variation."""
    now = datetime.now()
    hour = now.hour
    month = now.month
    
    if month in [12, 1, 2]:
        base_temp = 15.0
    elif month in [3, 4, 5]:
        base_temp = 22.0
    elif month in [6, 7, 8]:
        base_temp = 32.0
    else:
        base_temp = 20.0
    
    if 6 <= hour <= 10:
        temp_adj = -3
    elif 11 <= hour <= 15:
        temp_adj = 5
    elif 16 <= hour <= 19:
        temp_adj = 2
    else:
        temp_adj = -5
    
    random_drift = random.uniform(-2, 2)
    temperature = base_temp + temp_adj + random_drift
    
    base_humidity = 65
    humidity = max(30, min(90, base_humidity - (temperature - 25) * 2 + random.uniform(-10, 10)))
    
    descriptions = ["Clear sky", "Few clouds", "Scattered clouds", "Partly cloudy", "Overcast", "Light rain"]
    description = random.choice(descriptions)
    
    return {
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1),
        "description": description,
        "wind_speed": round(random.uniform(2, 15), 1),
        "pressure": round(random.uniform(1010, 1020), 1),
        "city": city,
        "location": location or settings.DEFAULT_LOCATION,
        "real_time": False,
        "timestamp": now.isoformat()
    }


def get_mock_forecast(city: str, days: int = 7) -> List[Dict[str, Any]]:
    """Generate realistic mock forecast with daily variation."""
    forecasts = []
    base_temp = 28.0
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        
        temp_trend = random.uniform(-1, 1) * i
        daily_temp = base_temp + temp_trend + random.uniform(-3, 3)
        
        rain_prob = random.randint(10, 60)
        
        descriptions = ["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Scattered showers"]
        description = descriptions[min(rain_prob // 15, 4)]
        
        forecasts.append({
            "date": date.strftime("%Y-%m-%d"),
            "temperature": round(daily_temp, 1),
            "humidity": round(random.uniform(50, 80), 1),
            "description": description,
            "rain_probability": rain_prob,
            "wind_speed": round(random.uniform(5, 20), 1)
        })
    
    return forecasts
