import requests
import random

# Sets up in application
WEATHER_API_KEY = ''

def generate_coordinates(city:str):
    """
    Takes a string of the needed city (covers edge case of multiple word cities), 
    requests coordinates from the API and returns them as output.
    """
    if len(city.split()) > 1:
        city = "+".join(city.split())

    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}') # limited to 1 city
    r_dict = response.json()
    if response.status_code == 200 and r_dict:
        lat, lon = r_dict[0]['lat'], r_dict[0]['lon'] 
        return lat, lon

def load_data(city:str):
    """
    Requests weather data from the API for a specific city. Returns a dictionary with the city 
    as key and it's stats as a value. Unit measurement for temperature is set to Celsius.
    """
    weather_info = {}
    lat, lon = generate_coordinates(city)

    response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&&units=metric&appid={WEATHER_API_KEY}')
    if response.status_code == 200:
        r_dict = response.json()
        weather_info[city] = (
            r_dict['current']['weather'][0]['description'],
            r_dict['current']['temp'], 
            r_dict['current']['humidity']
            )
    return weather_info

def check_coldest_city(weather_info:dict):
    """
    Takes a dict of cities and their stats, sorts them by their temperature value and returns the coldest one
    """
    sorted_by_temp = sorted(weather_info.items(), key=lambda weather_info: weather_info[1][1])
    return sorted_by_temp[0][0]

def check_avg_temp(weather_info:dict):
    """
    Takes a dict of cities and their stats and returns the average temperature between them
    """
    temps = [values[1] for values in weather_info.values()]
    return round(sum(temps) / len(temps), 2)

def gather_initial_output():
    CITIES = ['Sofia', 'London', 'Belgrade', 'Istanbul', 'Paris', 'Madrid', 'Oslo', 'New York', 'Los Angeles']
    random_cities = random.sample(CITIES, k=5)
    cities_data = {}

    for city in random_cities:
        weather_info = load_data(city)
        cities_data.update(weather_info)

    coldest_city = check_coldest_city(cities_data)
    avg_temp = check_avg_temp(cities_data)
    
    return random_cities, cities_data, coldest_city, avg_temp

def format_output(weather_info:dict):
    l_of_formatted_outputs = []
    for k, v in weather_info.items():
        l_of_formatted_outputs.append(f'{k.title()} - {v[0]}, Temperature: {v[1]} C, Humidity: {v[2]}')
    output = '\n'.join(l_of_formatted_outputs)
    return output
