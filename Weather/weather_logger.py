# Very simple weather logger that records the current temeprature
# by default for Waterloo, Canada and stores it in a CSV file.

import requests
import pandas as pd
from datetime import datetime

def getData(city):
    WEATHER_API_KEY = "1af3b3bd6ddd739572fadd7be38b331a"
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data["main"]
    else:
        print("ERROR: Could not fetch data!")
        return None

def getWeather(city = "Waterloo,ca"):
    data = getData(city)
    if data:
        with open("weather_log.csv", "a") as file:
            old_df = pd.read_csv("weather_log.csv", index_col=0)
            print("Got data!")
        with open("weather_log.csv", "w") as file:           
            temp = round(data["temp"] - 273.15, 2)
            date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            new_row = pd.DataFrame([pd.Series([date, temp])])
            new_row.columns = ["Date", "Temperature"]
            new_df = pd.concat([old_df, new_row], ignore_index=True)
            print(new_df)
            
            to_save = new_df.to_csv(index=True)
            file.write(to_save)
            print("Successfully written record!")
            file.close()

getWeather()
