# weatherMain.py

import requests
import pgeocode
from datetime import datetime
import itertools

def getForecast(latitude, longitude):
    # Get grid forecast endpoint for the specified location
    endpoint_url = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(endpoint_url)

    temp_data = {}

    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # print(data)

        # Get the forecast URL for 12h periods
        forecast_url = data['properties']['forecast']
        
        zone_id = data['properties']['forecastZone'].split('/')[-1]
        
        gridPoint, x, y = data['properties']['gridId'], data['properties']['gridX'],data['properties']['gridY']
        # print(data)
        # print(gridPoint,x,y)

        # Fetch the forecast data
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            
            # print(forecast_data)
            for period in forecast_data.get('properties', {}).get('periods', []):
                temp_data[period.get('name', '')] = {
                    'forecast': period.get('shortForecast', ''),
                    'temperature': period.get('temperature', '')
                }
    
    return temp_data,zone_id,gridPoint,x,y

def getHourlyForecast(grid, x, y ):
    endpoint_url = f'https://api.weather.gov/gridpoints/{grid}/{x},{y}/forecast/hourly'
    response = requests.get(endpoint_url)
    
    # print(response)
    temp_data = {}
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        
    
        for period in data.get('properties', {}).get('periods', []):
            startTime = period.get('startTime', '')
            
            try:
                startTime = datetime.fromisoformat(startTime[:-6])

                formattedTime = startTime.strftime("%I:%M %p")
            except:
                print('Cant get time')
                formattedTime= None
                
            temp_data[period.get('number', '')] = {
                'hour':formattedTime,
                'forecast': period.get('shortForecast', ''),
                'temperature': period.get('temperature', ''),
                'probRain': period.get('probabilityOfPrecipitation', {}).get('value'),
                'humidity':period.get('relativeHumidity', {}).get('value') # get values inside dictionaries\
        }
    temp_data=dict(itertools.islice(temp_data.items(),15)) # use itertools to slice the dictionary 
    # print("-------------------",temp_data)
    return temp_data
        

def num_alerts():
    endpoint_url = 'https://api.weather.gov/alerts/active/count'
    response = requests.get(endpoint_url)
    
    if response.status_code == 200:
        data = response.json()
        return data['total']
    else: 
        return "Failed to fetch the alerts count"



# def getAlerts(state):
#     endpoint_url = f'https://api.weather.gov/alerts/active?area={state}'
#     response = requests.get(endpoint_url)
    
#     alerts_data = []
    
#     if response.status_code == 200:
#         for alert in response.json().get('features', []):
#             alerts_data.append({
#                 'event': alert['properties']['event'],
#                 'headline': alert['properties']['headline'],
#                 'severity': alert['properties']['severity']
#             })
    
#     return alerts_data

import requests

def getAlerts(zoneId):
    endpoint_url = f'https://api.weather.gov/alerts/active/zone/{zoneId}'
    response = requests.get(endpoint_url)
    
    alerts_data = []
    
    if response.status_code == 200:
        for alert in response.json().get('features', []):
            alerts_data.append({
                'event': alert['properties']['event'],
                'headline': alert['properties']['headline'],
                'severity': alert['properties']['severity']
            })
    
    return alerts_data


def zipToGeo(zip):
    nomi = pgeocode.Nominatim('us')
    query = nomi.query_postal_code(zip)

    # print("Query result:", query)

    latitude = float(query.get("latitude", 0.0))  # Default to 0.0 if "latitude" is not present
    longitude = float(query.get("longitude", 0.0))  # Default to 0.0 if "longitude" is not present
    
    # Extract the actual state code from the query
    state = query.get("state_code", None)  # Default to None if "state_code" is not present

    return latitude, longitude, state

