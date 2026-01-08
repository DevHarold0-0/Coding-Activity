import os
import sys
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"


def get_weather_by_city(city_name: str):
    """Fetch current weather data for any city from OpenWeather API."""
    if not API_KEY:
        print("ERROR: OPENWEATHER_API_KEY environment variable not set.")
        return None
    
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": UNITS,
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None

    if response.status_code != 200:
        try:
            error_data = response.json()
            message = error_data.get("message", "Unknown API error")
        except:
            message = response.text
        print(f"API error ({response.status_code}): {message}")
        return None

    data = response.json()
    weather = {
        "city": data.get("name", "Unknown"),
        "country": data.get("sys", {}).get("country", ""),
        "temp": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "description": data.get("weather", [{}])[0].get("description", ""),
    }
    return weather


def print_weather(weather):
    """Display weather information."""
    if not weather:
        return
    
    city_line = f"{weather['city']}, {weather['country']}" if weather['country'] else weather['city']
    print("\n" + "="*50)
    print(f"WEATHER FOR: {city_line}")
    print("="*50)
    print(f"Temperature:  {weather['temp']}°C")
    print(f"Feels like:   {weather['feels_like']}°C")
    print(f"Humidity:     {weather['humidity']}%")
    print(f"Condition:    {weather['description'].title()}")
    print("="*50 + "\n")


def search_weather():
    """Search and display weather for any city."""
    city = input("\nEnter city name: ").strip()
    if not city:
        print("City name cannot be empty.")
        return
    
    print(f"Searching weather for '{city}'...")
    weather = get_weather_by_city(city)
    print_weather(weather)


def add_favourite(favourites):
    """Add a city to favourites (max 3)."""
    if len(favourites) >= 3:
        print("Favourites full (max 3). Use option 4 to update.")
        return
    
    city = input("\nEnter city to add to favourites: ").strip()
    if not city:
        print("City name cannot be empty.")
        return
    
    if city.lower() in [c.lower() for c in favourites]:
        print("City already in favourites.")
        return
    
    weather = get_weather_by_city(city)
    if weather:
        favourites.append(weather["city"])
        print(f"Added '{weather['city']}' to favourites ({len(favourites)}/3)")
    else:
        print("Cannot add city - weather lookup failed.")


def list_favourites(favourites):
    """List all favourite cities with current weather."""
    if not favourites:
        print("\nNo favourite cities yet. Add some with option 2!")
        return
    
    print(f"\nFAVOURITES ({len(favourites)}/3):")
    print("-" * 40)
    for i, city in enumerate(favourites, 1):
        print(f"\n{i}. {city}")
        weather = get_weather_by_city(city)
        print_weather(weather)


def update_favourites(favourites):
    """Remove a favourite and optionally add a new one."""
    if not favourites:
        print("\nNo favourites to update.")
        return
    
    print(f"\nCurrent favourites ({len(favourites)}/3):")
    for i, city in enumerate(favourites, 1):
        print(f"{i}. {city}")
    
    try:
        choice = input("\nEnter number to REMOVE (1-3, Enter to cancel): ").strip()
        if not choice:
            return
        
        index = int(choice) - 1
        if 0 <= index < len(favourites):
            removed = favourites.pop(index)
            print(f"Removed '{removed}'")
            
            if len(favourites) < 3:
                add_more = input("Add new favourite? (y/N): ").strip().lower()
                if add_more == 'y':
                    add_favourite(favourites)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    if not API_KEY:
        print("ERROR: Set OPENWEATHER_API_KEY environment variable first!")
        print("  export OPENWEATHER_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    favourites = []  
    
    while True:
        print("\n" + "WEATHER CLI".center(50, "="))
        print("1. Search weather for any city")
        print("2. Add city to favourites (max 3)")
        print("3. List favourites with weather")
        print("4. Update favourites (remove/add)")
        print("5. Exit")
        print("="*50)
        
        choice = input("Choose (1-5): ").strip()
        
        if choice == "1":
            search_weather()
        elif choice == "2":
            add_favourite(favourites)
        elif choice == "3":
            list_favourites(favourites)
        elif choice == "4":
            update_favourites(favourites)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Pick 1-5.")


if __name__ == "__main__":
    main()
