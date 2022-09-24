"""

A program the uses the Google Maps Distance Matrix API to automatically obtain the travel time from one location to
another. Using Twilio, it sends a text to a list of phones.

"""

from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from twilio.rest import Client
from datetime import datetime

# API key
with open("api_key.txt", "r") as api_file:
    api_key = api_file.read()

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
    # Origin
    start_name = "Grandview"
    start_location = "3690+Grandview+Pkwy+Birmingham+AL+35243"

    # Destination
    end_name = "Lakeview Green"
    end_location = "2901+4th+Ave+S+Birmingham+AL+35233"

# Base URL
url = "https://maps.googleapis.com/maps/api/distancematrix/json"

# GET request
r = requests.get(url + "?destinations=" + end_location + "&origins=" + start_location + "&departure_time=now" +
                 "&key=" + api_key)

# Return time as text
time = r.json()["rows"][0]["elements"][0]["duration_in_traffic"]["text"]

# Print the total travel time
travel_time = f"The total travel time from {start_name} to {end_name} is {time}."
print(travel_time)

# Twilio account sid and authorization token
with open("account_sid.txt", "r") as account_file:
    account_sid = account_file.read()
with open("auth_token.txt", "r") as auth_file:
    auth_token = auth_file.read()

# Creates a Client object from Twilio
client = Client(account_sid, auth_token)

# List of numbers to text
numbers_to_message = ['+12055639451', '+2053965212']
# Looping through the numbers and send the text to each number
for number in numbers_to_message:
    message = client.messages.create(
        messaging_service_sid='MG624d8354f0ca7aa37be60d1a39ed47de',
        body=travel_time,
        to=number
    )



