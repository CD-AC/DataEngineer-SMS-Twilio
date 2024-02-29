"""
************************************************************************
* Author = @CD-AC                                                      *
* Date = '15/02/2024'                                                  *
* Description = Sending Twilio messages with Python                    *
************************************************************************
"""

# Import required libraries and modules
import os
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime
from utils import request_wapi, get_forecast, create_df, send_message, get_date

# Set the query location and API key for weather API
query = 'Bogotá'
api_key = API_KEY_WAPI

# Retrieve the current date
input_date = get_date()

# Request weather information from the API
response = request_wapi(api_key, query)

# Initialize an empty list to hold forecast data
datos = []

# Loop through the next 24 hours to get forecast data
for i in tqdm(range(24), colour='green'):
    datos.append(get_forecast(response, i))

# Create a DataFrame from the collected forecast data
df_rain = create_df(datos)

# Send a message using Twilio with the forecast information
message_id = send_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, input_date, df_rain, query)

# Print a success message with the message ID
print('Mensaje Enviado con exito ' + message_id)
