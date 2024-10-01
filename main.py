import requests
import json
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = 'guhdjhfkjafvbkahv'


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        user_city = request.form.get("user_city")
        if user_city == "":
            return render_template("home.html", placeholder="Enter a name of a city.")

        return redirect(f"/city/{user_city}")
    return render_template("home.html", placeholder="London...")


@app.route("/city/<user_city>")
def city_page(user_city):
    try:
        api = "b039a614fd5d49abb5e122542242709"
        aqi = "yes"

        #url = f"http://api.weatherapi.com/v1/current.json?key={api}&q={user_city}&aqi={aqi}"
        #current = requests.get(url)

        #wdata = json.loads(current.text)

        forecastUrl = f"http://api.weatherapi.com/v1/forecast.json?key={api}&q={user_city}&aqi={aqi}&days=7"
        forecast = requests.get(forecastUrl)

        fdata = json.loads(forecast.text)
        print(fdata["forecast"]["forecastday"][0])
        #print(fdata["forecast"]["forecastday"][1])
        #print(fdata["forecast"]["forecastday"][2])

        city_name = fdata["location"]["name"]
        location_name = fdata["location"]["region"] + ", " + fdata["location"]["country"]
        temp_c = fdata["current"]["temp_c"]
        feelslike_c = fdata["current"]["feelslike_c"]
        condition_text = fdata["current"]["condition"]["text"]
        condition_icon = fdata["current"]["condition"]["icon"]
        wind_kph = fdata["current"]["wind_mph"]
        wind_dir = fdata["current"]["wind_dir"]
        pressure_mb = fdata["current"]["pressure_mb"]
        precip_mm = fdata["current"]["precip_mm"]
        humidity = fdata["current"]["humidity"]
        vis_km = fdata["current"]["vis_km"]

        forecast = fdata["forecast"]["forecastday"]

        return render_template("city.html", user_city=user_city.capitalize(), city_name=city_name,
                               location_name=location_name, temp_c=temp_c, feelslike_c=feelslike_c,
                               condition_text=condition_text, condition_icon=condition_icon, wind_kph=wind_kph,
                               wind_dir=wind_dir, pressure_mb=pressure_mb, precip_mm=precip_mm, humidity=humidity,
                               vis_km=vis_km, forecast=forecast)
    except:
        return render_template("home.html", placeholder="Please enter a valid City name!") and redirect("/")

@app.route("/test")
def test_page():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
