"""
************************************************************************
* Author = @CD-AC                                                      *
* Date = '15/02/2024'                                                  *
* Description = Sending Twilio messages with Python                    *
************************************************************************
"""

# Import necessary libraries
import pandas as pd
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI
from datetime import datetime
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Function to get the current date in YYYY-MM-DD format
def get_date():
    input_date = datetime.now()  # Get the current date and time
    input_date = input_date.strftime("%Y-%m-%d")  # Format the date
    return input_date  # Return the formatted date

# Function to request weather data from the WeatherAPI
def request_wapi(api_key, query):
    # Construct the request URL with the provided API key and query parameters
    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key=' + api_key + '&q=' + query + '&days=1&aqi=no&alerts=no'
    try:
        response = requests.get(url_clima).json()  # Make the request and parse the JSON response
    except Exception as e:
        print(e)  # Print any errors that occur during the request
    return response  # Return the response

# Function to extract and return forecast information for a specific hour
def get_forecast(response, i):
    # Extract data for the specified hour
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    # Return the extracted data
    return fecha, hora, condicion, tempe, rain, prob_rain

# Function to create and return a DataFrame filtered for rain predictions
def create_df(data):
    # Define DataFrame columns
    col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'prob_lluvia']
    df = pd.DataFrame(data, columns=col)  # Create DataFrame from data
    df = df.sort_values(by='Hora', ascending=True)  # Sort DataFrame by hour

    # Filter DataFrame for rain predictions between 6 AM and 10 PM
    df_rain = df[(df['Lluvia'] == 1) & (df['Hora'] > 6) & (df['Hora'] < 22)]
    df_rain = df_rain[['Hora', 'Condicion']]  # Keep only relevant columns
    df_rain.set_index('Hora', inplace=True)  # Set the 'Hora' column as the DataFrame index
    return df_rain  # Return the filtered DataFrame

# Function to send a message via Twilio with the rain forecast
def send_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, input_date, df, query):
    # Setup Twilio client with provided SID and Auth Token
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    # Create and send a message with the forecast information
    message = client.messages \
        .create(
            body='\nHola! \n\n El pronostico de lluvia hoy ' + input_date + ' en ' + query + ' es : \n\n ' + str(df),
            from_=PHONE_NUMBER,
            to='+573194127902'  # Example recipient number
        )
    return message.sid  # Return the message SID
