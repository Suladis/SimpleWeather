# app.py
print("Executing app.py")
from flask import Flask, render_template, request
from weatherMain import num_alerts, getAlerts, zipToGeo, getForecast , getHourlyForecast

app = Flask(__name__)

@app.route('/')
def index():
    # print("Accessed index route")
    return render_template('index.html')


@app.route('/get_weather', methods=['POST'])
def get_weather():
    # print("get_weather function called")
    try:
        zip_code = request.form['zipCode']
        # print("Zip Code:", zip_code)
        print(1)
    except:
        print(1)
   
    try:
        # Call functions from weatherMain.py
        latitude, longitude, state = zipToGeo(zip_code)
        # print("Latitude:", latitude)
        # print("Longitude:", longitude)
        # print("State:", state)
        print(2)
    except:
        print(2, 'failed')
    
    try:
        forecast,zoneid,gridPoint,x,y = getForecast(latitude, longitude)
        # print("Forecast:", forecast)
        print(3)
    except:
        print(4,"Fail")
    
    # forecastHourly = getHourlyForecast(gridPoint,x,y)
    hourlyForecast = getHourlyForecast(gridPoint,x,y)
    # print(hourlyForecast)
    
    alerts = getAlerts(zoneid)

    # print("Alerts Type:", type(alerts))
    # print("Alerts Content:", alerts)

    # Ensure forecast is a dictionary
    if not isinstance(forecast, dict):
        forecast = {}  # Set an empty dictionary if forecast is not a dictionary

    # Render the template with the data
    return render_template('result.html', num_alerts=num_alerts(), alerts=alerts, forecast=forecast , zip_code=zip_code, hourly=hourlyForecast)


if __name__ == "__main__":
    app.run(debug=True)
