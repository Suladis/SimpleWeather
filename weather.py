import requests
import pgeocode
import us
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons # to be used for future functions
import seaborn as sns
sns.set_style("darkgrid")
import requests
import tkinter as tk
from tkinter import simpledialog
import streamlit as st

def get_local_weather_forecast(latitude, longitude):
    print(latitude, longitude)
    # Get grid forecast endpoint for the specified location
    endpoint_url = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(endpoint_url)
    
    tempData = {}
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Get the forecast URL for 12h periods
        forecast_url = data['properties']['forecast']
        
        # Fetch the forecast data
        forecast_response = requests.get(forecast_url)
        
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            
            
            # Process and display the forecast data
            print("Local Weather Forecast:")
            for period in forecast_data['properties']['periods']:
                tempData[period['name']]=period['temperature']
                print(f"{period['name']}: {period['shortForecast']} - {period['temperature']}°F")
        else:
            print(f"Failed to fetch forecast data. Status Code: {forecast_response.status_code}")
    else:
        print(f"Failed to fetch grid forecast endpoint. Status Code: {response.status_code}")

 
    # plotTemp(tempData)
    
    
def numAlerts():
    endpoint_url = f'https://api.weather.gov/alerts/active/count'
    response = requests.get(endpoint_url)
    
    if response.status_code == 200:
        data = response.json()
        
        count = data['total']
        print(f"The number of Active Alerts: {count}")
    else: 
        print("Failed to fetch the alerts count")


# def plotTemp(tempData, labelColor='black'):
#     print(tempData)
#     lists = sorted(tempData.items())
#     x,y = zip(*lists)
#     print(x)
#     print(y)
#     fig, ax = plt.subplots()
    
#     ax.plot(x,y, ls=':', lw = 3)

#     ax.set_xlabel('Day Forcast')
#     ax.xaxis.label.set_color(labelColor)

#     ax.set_ylabel('Temperatures [F]')
#     ax.yaxis.label.set_color(labelColor)

#     plt.show()
    
def stateAbbr(state):
    
    abbr = us.states.lookup(state).abbr
    return abbr  
    
def get_alerts_for_state(state):
    # Get all active alerts for the specified state
    endpoint_url = f'https://api.weather.gov/alerts/active?area={state}'
    response = requests.get(endpoint_url)
    
    if response.status_code == 200:
        # Parse the response JSON
        alerts_data = response.json()
        
        
        if alerts_data['features']:
            
            # Display alerts
            print("\nActive Alerts:")
            for alert in alerts_data['features']:
                print(f"{alert['properties']['event']} - {alert['properties']['headline']}-{alert['properties']['severity']}")
        else:
            print("No active alerts.")
    else:
        print(f"Failed to fetch alerts data. Status Code: {response.status_code}")

#Zipcode to Geolocation     
def ZipToGeo(zip):
    print(f"ZIP code entered: {zip}")
    nomi = pgeocode.Nominatim('us')
    query = nomi.query_postal_code(zip)

    latitude = float(query["latitude"])
    longitude = float(query["longitude"])
    
    state = stateAbbr(query["state_name"])
   
    get_alerts_for_state(state)
    
    
    get_local_weather_forecast(latitude, longitude)
    

def main():
    numAlerts()
    ROOT = tk.Tk()
    ROOT.withdraw()
    
    
    
    # Zip Code will be converted to Geolocation
    zip = simpledialog.askstring(title="Zip", prompt="Please enter a zipcode:")
    ZipToGeo(zip)
    
   

if __name__ == "__main__":
    main()
