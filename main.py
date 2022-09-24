from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from twilio.rest import Client
from datetime import datetime

# API key
api_file = open("api-key.txt", "r")
api_key = api_file.read()
api_file.close()

# Current time
current_time = datetime.now().time()
print(current_time)
# Sets origin and destination based on time of day
if current_time.hour < 12:
    # Origin
    start_name = "Lakeview Green"
    start_location = "2901+4th+Ave+S+Birmingham+AL+35233"

    # Destination
    end_name = "Grandview"
    end_location = "3690+Grandview+Pkwy+Birmingham+AL+35243"
else:
    start_name = "Grandview"
    start_location = "3690+Grandview+Pkwy+Birmingham+AL+35243"

    # Destination
    end_name = "Lakeview Green"
    end_location = "2901+4th+Ave+S+Birmingham+AL+35233"

# base URL
url = "https://maps.googleapis.com/maps/api/distancematrix/json"

# get response
r = requests.get(url + "?destinations=" + end_location + "&origins=" + start_location + "&departure_time=now" +
                 "&key=" + api_key)

# return time as text
time = r.json()["rows"][0]["elements"][0]["duration_in_traffic"]["text"]

# print the total travel time
travel_time = f"The total travel time from {start_name} to {end_name} is {time}."
print(travel_time)
