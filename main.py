from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from twilio.rest import Client
from datetime import datetime

# API key
api_file = open("api-key.txt", "r")
api_key = api_file.read()
api_file.close()
