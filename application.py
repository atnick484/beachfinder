import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import math

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///beaches.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # posted from the index.html form
        lat = float(request.form.get("lat"))
        lon = float(request.form.get("lon"))

        # finds beaches within a large square on map near the user's location
        query = db.execute("SELECT name, latitude, longitude FROM beaches2 WHERE latitude > ? AND latitude < ? AND longitude > ? AND longitude < ?;",
        lat - 1, lat + 1, lon - 1, lon + 1)

        # TIMEZONEDB API - finds the timezone in order to convert UTC +0 to local timezone
        urlTime = "http://api.timezonedb.com/v2.1/get-time-zone?key=YNVY50GZRJA2&format=json&by=position&lat=" + str(lat) + "&lng=" + str(lon)
        responseTimezone = (requests.request("GET", urlTime)).json()
        url2 = "http://api.timezonedb.com/v2.1/get-time-zone?key=YNVY50GZRJA2&format=json&by=position&lat=" + str(lat) + "&lng=" + str(lon)
        responseTimezone = (requests.request("GET", url2)).json()
        offSet = int(responseTimezone['gmtOffset'])/3600
        zone = responseTimezone['abbreviation']

        # find distance to each beach
        for beach in query:
            # havensine algorithm https://www.movable-type.co.uk/scripts/latlong.html
            R = 6371000 # meters
            phi1 = lat * (math.pi) / 180 # in radians
            phi2 = beach['latitude'] * (math.pi) / 180 # in radians
            deltaPhi = (beach['latitude'] - lat) * math.pi / 180
            deltaLambda = (beach['longitude'] - lon) * math.pi / 180
            a = math.sin(deltaPhi/2) * math.sin(deltaPhi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(deltaLambda/2) * math.sin(deltaLambda/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c
            beach['distanceToUser'] = round(distance * 0.000621371, 3)

        # sort by distance
        query = sorted(query, key = lambda i: i['distanceToUser'])

        # truncate query (limit to TRUNCATE_NUM) before running the weather API
        TRUNCATE_NUM = 10
        query = query[0 : TRUNCATE_NUM]


        # CLIMACELL API - to get the weather of each beach
        url = "https://api.climacell.co/v3/weather/realtime"

        # prepare data for each beach to display to user
        for beach in query:

            # cast
            beachLat = str(beach['latitude'])
            beachLon = str(beach['longitude'])

            # KEYS for ClimaCell: ecRDTsvBtn86e38GpjDQdhLyYk7902hC, o3BbD8KG7iu0d8JDJtPO9WUooq2ilNWI, BH74FE2n4b3oxS0ibKq1tD5Xva0lkMLD

            # run ClimaCell Weather API for current beach
            querystring = {"lat":beachLat,"lon":beachLon,"unit_system":"us","fields":"temp,humidity,precipitation,precipitation_type,surface_shortwave_radiation,sunrise,sunset,weather_code","apikey":"ecRDTsvBtn86e38GpjDQdhLyYk7902hC"}
            response = requests.request("GET", url, params=querystring)
            dictResponse = response.json()

            # try-except incase API limit is reached
            try:
                oldTimeSunrise = (dictResponse['sunrise']['value'].split('T')[1]).split('.')[0]
            except:
                return render_template("errorMade.html")

            # convert sunrise time to local timezone
            hoursRise = int(oldTimeSunrise.split(':')[0])
            hoursRise = int(hoursRise + offSet)
            if (hoursRise < 0):
                hoursRise += 24
            if (hoursRise > 12):
                hoursRise -= 12
                newTimeRise = str(hoursRise) + ':' + oldTimeSunrise.split(':')[1] + ':' + oldTimeSunrise.split(':')[2] + ' PM'
            else:
                newTimeRise = str(hoursRise) + ':' + oldTimeSunrise.split(':')[1] + ':' + oldTimeSunrise.split(':')[2] + ' AM'
            beach['sunrise'] = newTimeRise + ' ' + zone

            # convert sunset time to local timezone
            oldTimeSunset = (dictResponse['sunset']['value'].split('T')[1]).split('.')[0]
            hoursSet = int(oldTimeSunset.split(':')[0])
            hoursSet = int(hoursSet + offSet)
            if (hoursSet < 0):
                hoursSet += 24
            if (hoursSet > 12):
                hoursSet -= 12
                newTimeSet = str(hoursSet) + ':' + oldTimeSunset.split(':')[1] + ':' + oldTimeSunset.split(':')[2] + ' PM'
            else:
                newTimeSet = str(hoursSet) + ':' + oldTimeSunset.split(':')[1] + ':' + oldTimeSunset.split(':')[2] + ' AM'
            beach['sunset'] = newTimeSet + ' ' + zone

            # add data to the beach's dictionary
            beach['temp'] = dictResponse['temp']['value']
            beach['humidity'] = str(dictResponse['humidity']['value']) + ' %'
            beach['precipitation'] = dictResponse['precipitation']['value']
            beach['precipitation_type'] = dictResponse['precipitation_type']['value']
            beach['weather_code'] = dictResponse['weather_code']['value'].replace("_", " ")

            # WEATHERSTACK API to get image | KEYS for WeatherStack: 3efde1c66dc175fde6c0b6be6adaded0, ac205f71638722ea44b25ed29fc5d5fa
            queryParam = beachLat + ', ' + beachLon
            params = {
                'access_key': 'ac205f71638722ea44b25ed29fc5d5fa',
                'query': queryParam
                }

            img_result = requests.get('http://api.weatherstack.com/current', params)
            img_response = img_result.json()
            img_weather_code = img_response['current']['weather_icons'][0]
            beach['img'] = img_weather_code

        # sort list of beaches by what was requested by user
        sortBy = request.form.get("sortBy")
        query = sorted(query, key = lambda i: i[sortBy])

        return render_template("display.html", beaches=query, myLat = lat, myLon = lon)

    else:
        return render_template("index.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")