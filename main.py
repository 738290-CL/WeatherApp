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

        url = f"http://api.weatherapi.com/v1/current.json?key={api}&q={user_city}&aqi={aqi}"
        result = requests.get(url)

        wdata = json.loads(result.text)

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

        return render_template("city.html", user_city=user_city.capitalize(), city_name=city_name,
                               location_name=location_name, temp_c=temp_c, feelslike_c=feelslike_c,
                               condition_text=condition_text, condition_icon=condition_icon, wind_kph=wind_kph,
                               wind_dir=wind_dir, pressure_mb=pressure_mb, precip_mm=precip_mm, humidity=humidity,
                               vis_km=vis_km)
    except:
        return render_template("home.html", placeholder="Please enter a valid City name!") and redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
