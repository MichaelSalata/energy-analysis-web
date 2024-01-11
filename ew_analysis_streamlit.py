#!/usr/bin/env python
# coding: utf-8

# # Electricity & Weather Data Analysis



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# creating a interactable website display
# import mpld3
# import streamlit.components.v1 as components


st.write("""
# Introduction
* This project creates insights into energy usage patterns in relation to time & weather.
    * It requires (downloadable) [ComEd](https://secure.comed.com/MyAccount/MyBillUsage/pages/secure/GreenButtonConnectDownloadMyData.aspx) & [Meteostat](https://github.com/meteostat/meteostat-python) data spreadsheets.
    * Cleans dirty data
    * Creates intuitive graphs & conclusions
 """)
 


import glob
directory_path = "./data"
file_pattern = "energy_weather_*.csv"

file_path = glob.glob(f"{directory_path}/{file_pattern}")[0]
energy_weather_df = pd.read_csv(filepath_or_buffer=file_path)
energy_weather_df.info()
energy_weather_df.head()


# convert the time cols into Datetime objs
energy_weather_df['time'] = pd.to_datetime(energy_weather_df['time'], format='%Y-%m-%d %H:%M:%S')
# print(energy_weather_df['time'].dtypes)
# energy_weather_df.head(4)


# convert the START_TIME col into Datetime objs
energy_weather_df['HOUR'] = pd.to_datetime(energy_weather_df['HOUR'], format='%Y-%m-%d %H:%M:%S')
# print(energy_weather_df['HOUR'].dtypes)
# energy_weather_df.head(4)


# Visualize the Cumulative Cost  &  rolling Temperature avg
# Calculate cumulative sum for 'COST'
# Calculate 14-day rolling sum for 'temp'
# since data is recorded 
hours=24
days=7
window_size0 = hours*days
window_name = "temp_"+str(days)+"_mean"


# Convert 'temp' to Fahrenheit
energy_weather_df['temp_fahrenheit'] = (energy_weather_df['temp'] * 9/5) + 32
# print(energy_weather_df.columns)


COST_Cumulative = energy_weather_df['COST'].cumsum()
rolling_avg_temp = energy_weather_df['temp'].rolling(window=window_size0).mean()




# streamlit plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plotting the cumulative sum for 'COST' on the primary y-axis
ax1.set_xlabel('Date')
ax1.set_ylabel('Cumulative Cost ($USD)', color='green')
line1, = ax1.plot(energy_weather_df['time'], COST_Cumulative, label='Cumulative Cost', color='green')
ax1.tick_params(axis='y', labelcolor='green')


# Creating a secondary y-axis for the rolling avg of 'temp'
ax2 = ax1.twinx()
ax2.set_ylabel('Temperature', color='blue')

# plotting rolling means of 'temp'
line2, = ax2.plot(energy_weather_df['time'], rolling_avg_temp, label='Temp ('+str(days)+'Day avg)', color='royalblue')
ax2.tick_params(axis='y', labelcolor='royalblue')



# Adding vertical lines for each month
for date in energy_weather_df['time'][energy_weather_df['time'].dt.is_month_end]:  # Adjust the frequency as needed
    ax1.axvline(x=date, color='gray', linestyle=':')
    
# Formatting x-axis tick labels with abbreviated month names
# label frequency should every ~30days
start = (30-20)*24   # the number of hours left in Oct
freq = 24*30 + 8    # average num of hours in a month
ax1.set_xticks(energy_weather_df['time'][start::freq])  # Adjust the frequency as needed
ax1.set_xticklabels(energy_weather_df['time'].dt.strftime('%b')[start::freq], rotation=45, ha='right')

fig.tight_layout()

# Include both lines in the legend
lines = [line1, line2]
# labels = [line.label for line in lines]
labels = [line1.get_label(), line2.get_label()]
ax1.legend(lines, labels, loc='upper left')

plt.title('Cumulative Cost  &  Temperature ('+str(days)+'Day avg)')

# have mpld3 convert graph to something streamlit can render
# fig_html = mpld3.fig_to_html(fig)
# components.html(fig_html, height=600)


# plt.show()
# streamlit version
st.pyplot(fig)


# creating a interactable website display
# mpld3 version
# fig_html = mpld3.fig_to_html(fig)
# components.html(fig_html, height=600)
# mpld3.show()



# # Analysis - Cumulative Cost  &  Temperature (7 Day avg)
# I was hoping to visualize the temperature/electricity_usage correlation. **NOTE:** USAGE & COST directly correlate.
# 
# * COST rises more steeply when the temperature is lower.
# * The visualization misses the positive temp/usage correlation at higher temperatures.
# 









# graph the USAGE level for different temperature levels

# Create temperature bins
temp_bins = list(range(-20, 110, 10))

# Categorize rows based on temperature bins
energy_weather_df['temp_bins'] = pd.cut(energy_weather_df['temp_fahrenheit'], bins=temp_bins, right=False)

# Group by temperature bins and calculate average 'USAGE' and count
average_data = energy_weather_df.groupby('temp_bins').agg({'USAGE': ['mean', 'count']}).reset_index()
average_data.columns = ['temp_bins', 'avg_USAGE', 'count']

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 5))

# Bar chart
bars = ax1.bar(average_data['temp_bins'].astype(str), average_data['avg_USAGE'], color='royalblue', label='Average USAGE')
ax1.set_xlabel('Temperature Ranges (10°F)')
ax1.set_ylabel('USAGE per Hour (avg kwh)')

# Display the count on top of each bar
for bar, count in zip(bars, average_data['count']):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, height/2, f'{count}\nhrs', ha='center', va='bottom')

ax1.legend(loc='upper right')
ax1.grid(axis='y')

plt.title('Average USAGE  every  10°F (Temperature)')
plt.xticks(rotation=45, ha='right')

# plt.show()
st.pyplot(fig)


# # Analysis - Usage / 10F
# * Indicates minimal energy usage when temperature is 60-70F.
# * The farther the temperature gets from 60-70F range, the greater energy usage it takes for climate control.
# 
# ## Heating takes more Energy than Cooling
# * 50-60 and 70-80 ranges are ~10 degrees away from 60-70 but more energy is used at 50-60
# * 40-50 and 80-90 ranges are ~20 degrees away from 60-70 but more energy is used at 40-50
# 
# ## Future Analysis using 'hrs'
# Number of hours spent at each temperature range could be used to get a how much energy is being spent to climate control at different temperatures. Those metrics could be used to do cost/benefit analysis of actions.
# 
# * e.g. How much total energy would be used using with different heaters could be calculated


st.write("""
# Data Used
* **Energy data** is downloaded from [Comed's Green Button Download webpage](https://secure.comed.com/MyAccount/MyBillUsage/pages/secure/GreenButtonConnectDownloadMyData.aspx).
* **Weather data** is downloaded using [Meteostat](https://github.com/meteostat/meteostat-python).
* **Energy data** is cleaned using [green_button_data_cleaning.ipynb](https://github.com/MichaelSalata/Energy_Use_Info/blob/main/green_button_data_cleaning.ipynb)
* **Weather data** is cleaned using [green_button_data_cleaning.ipynb](https://github.com/MichaelSalata/Energy_Use_Info/blob/main/weather_data_cleaning.ipynb)
* *Energy data** **Weather data** is combined & formmated with [electricity_and_weather_analysis.ipynb](https://github.com/MichaelSalata/Energy_Use_Info/blob/main/electricity_and_weather_analysis.ipynb)
* **Energy/Weather combined data** is displayed here.
""")
