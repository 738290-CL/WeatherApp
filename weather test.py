import requests
import json
from flask import Flask

API = "b039a614fd5d49abb5e122542242709"
aqi = "yes"

city_name = input("Enter the city name: ")
url = f"http://api.weatherapi.com/v1/current.json?key={API}&q={city_name}&aqi={aqi}"
result = requests.get(url)

print(result)

wdata = json.loads(result.text)
print(wdata)

city_name = wdata["location"]["name"]
location_name = wdata["location"]["region"] + ", " + wdata["location"]["country"]
temp_c = wdata["current"]["temp_c"]
feelslike_c = wdata["current"]["feelslike_c"]
condition_text = wdata["current"]["condition"]["text"]
condition_icon = wdata["current"]["condition"]["icon"]
wind_kph = wdata["current"]["wind_mph"]
wind_dir = wdata["current"]["wind_dir"]
pressure_mb = wdata["current"]["pressure_mb"]
precip_mm = wdata["current"]["precip_mm"]
humidity = wdata["current"]["humidity"]
vis_km = wdata["current"]["vis_km"]


print(city_name, location_name, temp_c, feelslike_c, condition_icon, condition_text, wind_kph, wind_dir, pressure_mb, precip_mm, humidity, vis_km)
