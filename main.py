"""

A program that uses the Google Maps Distance Matrix API to automatically obtain the travel time from one location to
another. Using Twilio, it sends a text to a list of phones.

"""
import pandas
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
# from twilio.rest import Client
from datetime import datetime

# Current time and date
current_date = datetime.now().date()
print(current_date)
# Writes a date heading and appends it to data.csv file
with open("data.csv", mode="a") as data:
    data.write(f"{current_date}")
# Creates an empty dictionary
empty_dict = {"Time": [],
              "Origin": [],
              "Destination": [],
              "Duration": []
              }

# Creates a Dataframe from the empty dictionary and appends the headers to data.csv
initial_data = pandas.DataFrame(empty_dict)
initial_data.to_csv("data.csv", mode="a")


def check_travel_time():
    # API key
    with open("api_key.txt", "r") as api_file:
        api_key = api_file.read()

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
    duration = r.json()["rows"][0]["elements"][0]["duration_in_traffic"]["text"]

    # Print the total travel time
    travel_time = f"The total travel time from {start_name} to {end_name} is {duration}."
    print(travel_time)

    # Creates a dictionary with the info from Google Maps API
    data_dict = {"Time": [current_time],
                 "Origin": [start_name],
                 "Destination": [end_name],
                 "Duration": [duration]
                 }

    # Sorts the data from above into a Dataframe and appends it to data.csv file
    df_data = pandas.DataFrame(data_dict)
    df_data.to_csv("data.csv", mode="a", header=False)

    # # Twilio account sid and authorization token
    # with open("account_sid.txt", "r") as account_file:
    #     account_sid = account_file.read()
    # with open("auth_token.txt", "r") as auth_file:
    #     auth_token = auth_file.read()

    # # Creates a Client object from Twilio
    # client = Client(account_sid, auth_token)
    #
    # # List of numbers to text
    # numbers_to_message = ['+12055639451', '+12053965212']
    # # Looping through the numbers and send the text to each number
    # for number in numbers_to_message:
    #     message = client.messages.create(
    #         messaging_service_sid='MG624d8354f0ca7aa37be60d1a39ed47de',
    #         body=travel_time,
    #         to=number
    #     )


check_travel_time()
scheduler = BlockingScheduler()
scheduler.add_job(check_travel_time, 'interval', minutes=30)
scheduler.start()
