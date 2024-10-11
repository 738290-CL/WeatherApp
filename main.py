import requests
import json
from flask import Flask, render_template, request, url_for, redirect, flash, abort
from datetime import datetime
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'guhdjhfkjafvbkahv'


# Database initialisation
def init_db():
    with sqlite3.connect(r"C:\Users\738290\Downloads\SQLiteDatabaseBrowserPortable\WeatherAppDB.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
            )""")
        conn.commit()


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        user_city = request.form.get("user_city")
        if user_city == "":
            return render_template("home.html", placeholder="Enter a name of a city.", logged_in=logged_in,
                                   user_name=user_name)

        return redirect(f"/city/{user_city}")
    return render_template("home.html", placeholder="London...", logged_in=logged_in, user_name=user_name)


@app.route("/city/<user_city>")
def city_page(user_city):
    try:
        api = "92888070b5d8422ea64103903241110"
        aqi = "yes"

        forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api}&q={user_city}&aqi={aqi}&days=7"
        requests.get(forecast_url)

    except:
        print("test 4")
        return redirect("/")

    else:
        api = "92888070b5d8422ea64103903241110"
        aqi = "yes"

        forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api}&q={user_city}&aqi={aqi}&days=7"
        forecast = requests.get(forecast_url)

        fdata = json.loads(forecast.text)

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
        uk_defra_index = fdata["current"]["air_quality"]["gb-defra-index"]

        forecast = fdata["forecast"]["forecastday"]

        day0 = (datetime.strptime(forecast[0]["date"], "%Y-%m-%d").date()).strftime("%a %d %b")
        day1 = (datetime.strptime(forecast[1]["date"], "%Y-%m-%d").date()).strftime("%a %d %b")
        day2 = (datetime.strptime(forecast[2]["date"], "%Y-%m-%d").date()).strftime("%a %d %b")
        day3 = (datetime.strptime(forecast[3]["date"], "%Y-%m-%d").date()).strftime("%a %d %b")
        day4 = (datetime.strptime(forecast[4]["date"], "%Y-%m-%d").date()).strftime("%a %d %b")
        day5 = (datetime.strptime(forecast[5]["date"], "%Y-%m-%d").date()).strftime("%a %d %b")
        day6 = (datetime.strptime(forecast[6]["date"], "%Y-%m-%d").date()).strftime("%a %d %b")

        return render_template("city.html", user_city=user_city.capitalize(), city_name=city_name,
                               location_name=location_name, temp_c=temp_c, feelslike_c=feelslike_c,
                               condition_text=condition_text, condition_icon=condition_icon, wind_kph=wind_kph,
                               wind_dir=wind_dir, pressure_mb=pressure_mb, precip_mm=precip_mm, humidity=humidity,
                               vis_km=vis_km, day0=day0, day1=day1, day2=day2, day3=day3, day4=day4, day5=day5,
                               day6=day6, uk_defra_index=uk_defra_index, forecast=forecast, logged_in=logged_in,
                               user_name=user_name)


@app.route("/test")
def test_page():
    return render_template("test.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        entered_email = request.form.get("user_email")
        entered_password = request.form.get("user_password1")

        with sqlite3.connect(r"C:\Users\738290\Downloads\SQLiteDatabaseBrowserPortable\WeatherAppDB.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            global logged_in, user_name

            for user in users:
                db_name = user[0]
                db_email = user[1]
                db_password = user[2]

                entered_password_encode = entered_password.encode("UTF-8")
                equal_passwords = bcrypt.checkpw(entered_password_encode, db_password)

                if db_email == entered_email and equal_passwords:
                    logged_in = True
                    user_name = db_name
                    return redirect("/")

            logged_in = False
            return abort(403)
    return render_template("login.html", logged_in=logged_in, user_name=user_name)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_email = request.form.get("user_email")
        user_password = request.form.get("user_password1")

        # hashing password
        user_password_bytes = user_password.encode("UTF-8")
        salt = bcrypt.gensalt()
        user_password_hash = bcrypt.hashpw(user_password_bytes, salt)

        with sqlite3.connect(r"C:\Users\738290\Downloads\SQLiteDatabaseBrowserPortable\WeatherAppDB.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?,?,?)""", (user_name, user_email, user_password_hash))
            conn.commit()
        return redirect("/login")
    return render_template("register.html", logged_in=logged_in)


@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    return redirect("/")


@app.route("/403")
@app.errorhandler(403)
def error_403_page(error):
    return render_template("403.html")


@app.errorhandler(404)
def error_404_redirect(error):
    return redirect("/")


global logged_in, user_name
logged_in = False
user_name = "Guest"
if __name__ == "__main__":
    init_db()
    app.run(debug=True)