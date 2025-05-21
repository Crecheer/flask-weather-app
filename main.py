from flask import *
import requests
import urllib
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Go to ./forecast?city=(city)</h1>"

@app.route("/forecast", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    units = request.args.get("units")
    raw = request.args.get("raw")
    day = request.args.get("day")
    if city == None:
        abort(400, "No city was parsed")
    if units == None:
        units = "metric"
    if day != None:
        single_day = True
    else:
        single_day = False
    
    data = {}
    data["q"] = city
    data["appid"] = "0b5b164098bdcf11dd4cfd38f04bfd6a"
    data["units"] = units
    
    url_args = urllib.parse.urlencode(data)
    url = "https://api.openweathermap.org/data/2.5/forecast"
    full_url = url + "?" + url_args
    resp = Response(data)
    resp.status_code = 200
    print(full_url)
    data = urllib.request.urlopen(full_url)
    data_json = json.loads(data.read())
    
    filtered = []
    if day != None:
        for i in data_json["list"]:
            if day in i["dt_txt"]:
                filtered.append(i)
    else:
        filtered = data_json
            
    
    if raw == "true":
        return filtered
    else:
        return render_template("index.html", title="Weather App", data=filtered, single_day = single_day)