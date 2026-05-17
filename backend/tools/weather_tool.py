"""
Weather Tool — Real HTTP call to Open-Meteo API
Gets venue weather conditions including temperature, humidity, cloud cover, wind speed,
and dew point to inform the dew factor analysis.
"""

import httpx
from typing import Any

# Venue coordinates lookup
VENUE_COORDINATES = {
    "Wankhede Stadium, Mumbai": {"lat": 18.9388, "lon": 72.8258},
    "MA Chidambaram Stadium, Chennai": {"lat": 13.0627, "lon": 80.2792},
    "Eden Gardens, Kolkata": {"lat": 22.5645, "lon": 88.3433},
    "Arun Jaitley Stadium, Delhi": {"lat": 28.6366, "lon": 77.2200},
    "M. Chinnaswamy Stadium, Bengaluru": {"lat": 12.9791, "lon": 77.5995},
    "Rajiv Gandhi Intl Cricket Stadium, Hyderabad": {"lat": 17.4062, "lon": 78.5519},
    "Sawai Mansingh Stadium, Jaipur": {"lat": 26.8946, "lon": 75.8028},
    "BRSABV Ekana Cricket Stadium, Lucknow": {"lat": 26.8900, "lon": 80.9500},
    "Punjab Cricket Association Stadium, Mohali": {"lat": 30.6942, "lon": 76.7170},
    "Narendra Modi Stadium, Ahmedabad": {"lat": 23.0900, "lon": 72.5940},
}

async def get_venue_weather(venue: str) -> dict[str, Any]:
    """
    Fetches current weather conditions for a cricket venue using Open-Meteo API.
    
    Args:
        venue: The name of the cricket venue/stadium
    
    Returns:
        Dictionary with temperature, humidity, dew_point, wind_speed, cloud_cover,
        dew_risk (high/medium/low), and a weather summary string.
    """
    coords = VENUE_COORDINATES.get(venue)
    if not coords:
        # Default to Mumbai if venue not found
        coords = {"lat": 18.9388, "lon": 72.8258}
    
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={coords['lat']}&longitude={coords['lon']}"
        "&current=temperature_2m,relative_humidity_2m,dew_point_2m,"
        "cloud_cover,wind_speed_10m,precipitation"
        "&timezone=Asia%2FKolkata"
        "&forecast_days=1"
    )
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        
        current = data["current"]
        temp = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        dew_point = current["dew_point_2m"]
        cloud_cover = current["cloud_cover"]
        wind_speed = current["wind_speed_10m"]
        precipitation = current.get("precipitation", 0)
        
        # Dew risk: if temp-dew_point < 4°C AND humidity > 80%, high dew risk
        dew_spread = temp - dew_point
        if dew_spread < 3 and humidity > 85:
            dew_risk = "HIGH"
        elif dew_spread < 6 and humidity > 70:
            dew_risk = "MEDIUM"
        else:
            dew_risk = "LOW"
        
        summary = (
            f"{temp}°C, {humidity}% humidity, {cloud_cover}% cloud cover, "
            f"wind {wind_speed} km/h. Dew spread: {dew_spread:.1f}°C → Dew risk: {dew_risk}."
        )
        
        return {
            "venue": venue,
            "temperature_c": temp,
            "humidity_percent": humidity,
            "dew_point_c": dew_point,
            "cloud_cover_percent": cloud_cover,
            "wind_speed_kmh": wind_speed,
            "precipitation_mm": precipitation,
            "dew_risk": dew_risk,
            "summary": summary,
            "source": "Open-Meteo API (live)"
        }
    
    except Exception as e:
        # Fallback with estimated data if API fails
        return {
            "venue": venue,
            "temperature_c": 28,
            "humidity_percent": 75,
            "dew_point_c": 23,
            "cloud_cover_percent": 40,
            "wind_speed_kmh": 12,
            "precipitation_mm": 0,
            "dew_risk": "MEDIUM",
            "summary": f"Weather API unavailable ({str(e)[:50]}). Using estimated: 28°C, 75% humidity, MEDIUM dew risk.",
            "source": "estimated (fallback)"
        }
