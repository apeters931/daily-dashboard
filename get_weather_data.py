import requests
import json

def save_forecast(api_key: str, location: str, days: int, target_date: str, filename: str):
    """
    Fetch forecast data from WeatherAPI.com and save JSON for a specific date.

    :param api_key: Your WeatherAPI key
    :param location: City or lat/lon (e.g., "Madison,WI" or "43.0731,-89.4012")
    :param days: Number of forecast days to request (max 14)
    :param target_date: Date to extract (YYYY-MM-DD)
    :param filename: File to save the JSON
    """
    url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": location,
        "days": days,
        "aqi": "no",
        "alerts": "no"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Find forecast for target_date
    forecast_day = None
    for day in data["forecast"]["forecastday"]:
        if day["date"] == target_date:
            forecast_day = day
            break

    if forecast_day is None:
        raise ValueError(f"No forecast found for {target_date}. Check the 'days' parameter.")

    # Save to file
    with open(filename, "w") as f:
        json.dump(forecast_day, f, indent=2)

    print(f"Saved forecast for {target_date} to {filename}")

API_KEY = "5b3bf3eb95b6472781c00225251009"
save_forecast(
    api_key=API_KEY,
    location="Madison,WI",
    days=5,
    target_date="2025-09-11",
    filename="madison_forecast_2025-09-11.json"
)
