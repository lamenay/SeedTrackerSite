import requests
from datetime import date, timedelta


def get_weather_forecast(city="Уфа"):
    """Получает прогноз погоды на 7 дней через Open-Meteo"""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru"
        geo_response = requests.get(geo_url, timeout=5)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return None

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum"
            f"&timezone=Europe%2FMoscow&forecast_days=7"
        )

        weather_response = requests.get(weather_url, timeout=5)
        weather_data = weather_response.json()

        daily = weather_data.get("daily")
        if not daily:
            return None

        # Convert to list of day dicts for templates
        days = []
        for i in range(len(daily.get("time", []))):
            days.append({
                "date": daily["time"][i],
                "temp_max": round(daily["temperature_2m_max"][i]),
                "temp_min": round(daily["temperature_2m_min"][i]),
                "precipitation": daily.get("precipitation_sum", [0]*7)[i],
                "precipitation_probability": daily.get("precipitation_probability_max", [0]*7)[i],
            })
        return days

    except Exception as e:
        print(f"Ошибка получения погоды: {e}")
        return None


def check_rain_forecast(city, days_ahead=7):
    """
    Проверяет прогноз дождя на ближайшие N дней.
    Возвращает список дат, когда ожидается значительный дождь (>2мм).
    """
    weather = get_weather_forecast(city)
    if not weather:
        return []

    rain_days = []
    for day in weather[:days_ahead]:
        precip = day.get("precipitation", 0)
        prob = day.get("precipitation_probability", 0)
        if precip > 2 or prob > 60:
            rain_days.append({
                "date": day["date"],
                "precipitation_mm": precip,
                "probability": prob,
            })

    return rain_days


def get_watering_advice(planting, city):
    """
    Умный совет по поливу: учитывает прогноз дождя.
    Возвращает словарь с информацией и рекомендацией.
    """
    if not planting.watering_interval:
        return {"advice": "no_interval", "message": "Интервал полива не задан"}

    next_water = planting.next_watering_date
    days_until = planting.days_until_watering

    result = {
        "next_watering_date": next_water,
        "days_until": days_until,
        "rain_days": [],
        "advice": "normal",
        "message": "",
        "skip_possible": False,
    }

    # Проверяем прогноз дождя
    try:
        rain_days = check_rain_forecast(city, days_ahead=max(7, (planting.watering_interval or 7) + 2))
    except Exception:
        rain_days = []

    result["rain_days"] = rain_days

    if days_until is not None and days_until <= 0:
        result["advice"] = "water_now"
        result["message"] = "Пора поливать! 💧"
    elif days_until == 1:
        result["advice"] = "water_tomorrow"
        result["message"] = "Завтра нужно полить 💧"
    else:
        result["message"] = f"Следующий полив через {days_until} дн."

    # Проверяем: если дождь ожидается до или в день полива — можно пропустить
    if rain_days and next_water:
        for rd in rain_days:
            rain_date = date.fromisoformat(rd["date"])
            # Если дождь будет раньше или в день следующего полива
            if rain_date <= next_water and rd["precipitation_mm"] > 2:
                result["skip_possible"] = True
                result["advice"] = "rain_expected"
                result["message"] = (
                    f"🌧 Дождь ожидается {rain_date.strftime('%d.%m')} "
                    f"(~{rd['precipitation_mm']:.0f}мм, вероятность {rd['probability']}%). "
                    f"Полив можно пропустить!"
                )
                break

    return result
