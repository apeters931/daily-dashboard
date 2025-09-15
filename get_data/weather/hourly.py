import requests
import json
import os
from datetime import date # Import the date class from the datetime module

def get_hourly_weather_json(api_key: str, location: str, target_date: str):
    """
    Fetches hourly weather data for a specific date from WeatherAPI.com
    and returns it as a Python dictionary.

    :param api_key: Your WeatherAPI key
    :param location: City or lat/lon (e.g., "Madison,WI")
    :param target_date: The specific date to get the hourly forecast for (YYYY-MM-DD)
    :return: A Python dictionary of the hourly weather data, or None if an error occurs.
    """
    url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": location,
        "days": 1,
        "aqi": "no",
        "alerts": "no"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        forecast_day = None
        for day in data["forecast"]["forecastday"]:
            if day["date"] == target_date:
                forecast_day = day
                break

        if forecast_day is None:
            print(f"Error: No forecast found for {target_date}. Please check the date and try again.")
            return None

        hourly_list = []
        for hour in forecast_day["hour"]:
            hourly_entry = {
                "time": hour["time"],
                "temperature_fahrenheit": hour["temp_f"],
                "condition": hour["condition"]["text"],
                "chance_of_rain_percent": hour["chance_of_rain"]
            }
            hourly_list.append(hourly_entry)

        final_json = {
            "location": data["location"]["name"],
            "date": target_date,
            "hourly_weather": hourly_list
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

    :param data: The dictionary to save.
    :param directory: The directory to save the file in.
    :param filename: The name of the file (e.g., "forecast.json").
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    filepath = os.path.join(directory, filename)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully saved hourly weather data to {filepath}")


# Example usage
if __name__ == "__main__":
    API_KEY = "5b3bf3eb95b6472781c00225251009"
    
    # Use the datetime module to get the current date automatically
    current_date = date.today().isoformat()
    
    # Get the weather data as a dictionary
    weather_data = get_hourly_weather_json(
        api_key=API_KEY,
        location="Madison,WI",
        target_date=current_date
    )

    # If data was successfully fetched, save it to a file
    if weather_data:
        save_directory = "JSON"
        file_name = f"hourly_weather.json"
        save_json_file(weather_data, save_directory, file_name)