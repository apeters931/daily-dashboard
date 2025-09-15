import requests
import json
import os

def get_full_forecast_json(api_key: str, location: str):
    """
    Fetches the maximum number of forecast days (14 days) from WeatherAPI.com
    and returns it as a Python dictionary.

    :param api_key: Your WeatherAPI key
    :param location: City or lat/lon (e.g., "Madison,WI")
    :return: A Python dictionary of the full forecast data, or None if an error occurs.
    """
    url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": location,
        "days": 14, # Updated to 14 for the maximum forecast
        "aqi": "no",
        "alerts": "no"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        full_forecast = []
        for day in data["forecast"]["forecastday"]:
            # Extract daily summary data
            daily_summary = {
                "date": day["date"],
                "max_temp_f": day["day"]["maxtemp_f"],
                "min_temp_f": day["day"]["mintemp_f"],
                "avg_temp_f": day["day"]["avgtemp_f"],
                "condition": day["day"]["condition"]["text"],
                "chance_of_rain_percent": day["day"]["daily_chance_of_rain"]
            }
            full_forecast.append(daily_summary)

        final_json = {
            "location": data["location"]["name"],
            "full_forecast": full_forecast
        }
        
        return final_json

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def save_json_file(data: dict, directory: str, filename: str):
    """
    Saves a Python dictionary to a JSON file.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    filepath = os.path.join(directory, filename)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully saved full forecast data to {filepath}")

# Example usage
if __name__ == "__main__":
    API_KEY = "5b3bf3eb95b6472781c00225251009"
    
    weather_data = get_full_forecast_json(
        api_key=API_KEY,
        location="Madison,WI"
    )

    if weather_data:
        save_directory = "JSON"
        file_name = "weekly_forecast.json"
        save_json_file(weather_data, save_directory, file_name)
