# app.py
print("Executing app.py")
from flask import Flask, render_template, request

from weatherMain import num_alerts, get_alerts_for_state, zip_to_geo, get_local_weather_forecast

app = Flask(__name__)

@app.route('/')
def index():
    print("Accessed index route")
    return render_template('index.html')


@app.route('/get_weather', methods=['POST'])
def get_weather():
    print("get_weather function called")
    zip_code = request.form['zipCode']
    print("Zip Code:", zip_code)
    
    # Call functions from weather.py
    latitude, longitude, state = zip_to_geo(zip_code)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("State:", state)

    alerts = get_alerts_for_state(state)
    print("Alerts:", alerts)

    forecast = get_local_weather_forecast(latitude, longitude)
    print("Forecast:", forecast)

    # Ensure forecast is a dictionary
    if not isinstance(forecast, dict):
        forecast = {}  # Set an empty dictionary if forecast is not a dictionary

    # Render the template with the data
    return render_template('result.html', num_alerts=num_alerts(), alerts=alerts, forecast=forecast)


if __name__ == "__main__":
    app.run(debug=True)
