import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(
    page_title="Sky Oracle",
    page_icon="weather.png",
    menu_items={
        "About":"""Introducing Sky Oracle, your ultimate weather companion! Experience real-time weather conditions with precision and clarity. Uncover detailed Air Quality Analysis for a deeper understanding of your environment. Plan ahead with our expertly crafted forecasts, spanning the next six days. Dive into our intuitive forecast visualization tools, offering clear insights into upcoming weather patterns."""
    }
)

st.write("<h2 style='color:#00C853';>Your Gateway to Weather Wisdom</h2>",unsafe_allow_html=True)

city=st.text_input("Search City")

btn=st.button("Search")
lat=long=None

if btn:
    try:
        api_key="4d40a0735c2b47b69146db86045844d5"
        # API 1
        weather = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api_key)
        data=weather.text
        conv_weather=json.loads(data)

        # Storing all Basic Weather Information 
        city=conv_weather["name"]
        long=conv_weather["coord"]["lon"]
        lat=conv_weather["coord"]["lat"]
        description=conv_weather["weather"][0]["description"].title()
        temp = "{:.2f}°C".format(int(conv_weather["main"]["temp"]) - 273.15)
        feels_like = "{:.2f}°C".format(int(conv_weather["main"]["feels_like"]) - 273.15)
        pressure = "{} hPa".format(conv_weather["main"]["pressure"])
        humidity = "{}%".format(conv_weather["main"]["humidity"])
        speed = "{} m/s".format(conv_weather["wind"]["speed"])
        degree = "{}°".format(conv_weather["wind"]["deg"])


        # Displaying the Basic Weather Information
        df = pd.DataFrame([["City",city],["Weather Overview",description],["Temperature",temp],["Feels Like",feels_like],["Pressure",pressure],["Humidity",humidity],["Wind Speed",speed],["Wind Degree",degree],["Latitude",lat],["Longitude",long]])
        data_html = df.to_html(index=False, header=False, escape=False)

        st.write("<h2 style='color:#FFC400;'>Current Condition in {}</h2>".format(city.title()), unsafe_allow_html=True)

        st.write(data_html, unsafe_allow_html=True)
        
        st.write("<h2 style='color:#FFC400';>Air Quality Analysis</h2>",unsafe_allow_html=True)
        # API 2
        road = requests.get("http://api.openweathermap.org/data/2.5/air_pollution?lat=" + str(lat) + "&lon=" + str(long) + "&appid=" + api_key)
        data3=road.text
        conv_road=json.loads(data3)
        # Storing Air Quality Data
        carbon_monoxide=conv_road["list"][0]["components"]["co"]
        nitric_oxide=conv_road["list"][0]["components"]["no"]
        nitrogen_dioxide=conv_road["list"][0]["components"]["no2"]
        ozone=conv_road["list"][0]["components"]["o3"]
        sulphur_dioxide=conv_road["list"][0]["components"]["so2"]
        fine_particulate_matter=conv_road["list"][0]["components"]["pm2_5"]
        coarse_particulate_matter=conv_road["list"][0]["components"]["pm10"]
        ammonia=conv_road["list"][0]["components"]["nh3"]

        # Displaying Air Quality Data
        df3 = pd.DataFrame([["Carbon Monoxide (CO)",carbon_monoxide],["Nitric Oxide (NO)",nitric_oxide],["Nitrogen Dioxide (NO2)",nitrogen_dioxide],["Ozone (O3)",ozone],["Sulfur Dioxide (SO2)",sulphur_dioxide],["Fine Particulate Matter (PM2.5)",fine_particulate_matter],["Coarse Particulate Matter (PM10)",coarse_particulate_matter],["Ammonia (NH3)",ammonia]])

        data_html3 = df3.to_html(index=False, header=False, escape=False)

        st.write(data_html3, unsafe_allow_html=True)

        st.write("<h2 style='color:#FFC400';>Forecast for the Next Six Days</h2>",unsafe_allow_html=True)

        # API 3
        forecast = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat=" + str(lat) + "&lon=" + str(long) + "&appid=" + api_key)
        data2=forecast.text
        conv_forecast=json.loads(data2)

        # Getting the Length Of 6 Day Forcast
        i=len(conv_forecast["list"])

        # Storing the 6 Day Forcast
        six_day=[["Date","Time","Sky Status","Temperature","Feels Like","Min Temp","Max Temp","Humidity","Ground Level","Wind Speed"]]
        six_day_temperature=[]
        six_day_date=[]
        for k in range(0,i):
                day=conv_forecast["list"][k]
                splitted_date=day["dt_txt"].split(" ")
                date=splitted_date[0]
                time=splitted_date[1][0:5]
                description=day["weather"][0]["description"]
                temp = "{:.2f}°C".format(int(day["main"]["temp"]) - 273.15)
                feels_like = "{:.2f}°C".format(int(day["main"]["feels_like"]) - 273.15)
                min_temp = "{:.2f}°C".format(int(day["main"]["temp_min"]) - 273.15)
                max_temp = "{:.2f}°C".format(int(day["main"]["temp_max"]) - 273.15)
                ground_level = "{} hPa".format(day["main"]["grnd_level"])
                humidity = "{}%".format(day["main"]["humidity"])
                speed = "{} m/s".format(day["wind"]["speed"])
                six_day_data=[date,time,description,temp,feels_like,min_temp,max_temp,humidity,ground_level,speed]
                six_day.append(six_day_data)
                six_day_temperature.append("{:.0f}".format(int(day["main"]["temp"]) - 273.15))
                six_day_date.append(splitted_date[0])

        # Displaying the 6 Day Forcast
        df2 = pd.DataFrame(
                six_day
        )
        
        data_html2 = df2.to_html(index=False, header=False, escape=False)
        st.write(data_html2, unsafe_allow_html=True)

        # Weather Graph
        st.write("<h2 style='color:#FFC400';>Forecast Visualization</h2>",unsafe_allow_html=True)
        st.write("<br>",unsafe_allow_html=True)
        six_day_temperature_float=[float(temp) for temp in six_day_temperature]
        chart_data = pd.DataFrame(
                {"Temperature":six_day_temperature_float},
                index=six_day_date
        )
        st.scatter_chart(chart_data)

    except:
        st.error ("Invalid City :(")
