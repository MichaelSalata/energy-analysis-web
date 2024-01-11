#!/usr/bin/env python
# coding: utf-8

# # Electricity & Weather Data Analysis

#zz # Introduction
# The [Energy_Use_Info](https://github.com/MichaelSalata/Energy_Use_Info) is meant to gather insights on electricity usage.
# 
# This notebook looks for insights into electricity usage relative to weather data.
# 
# ## Data
# * This notebook uses data cleaned with "green_button_data_cleaning.ipynb" aka:  clean_energy_use_*.csv
# * This notebook uses data cleaned with "weather_data_cleaning.ipynb.ipynb" aka: clean_weather_*.csv
# 
# 
# ## My Energy Data Source
# Currently, the data is from my energy company(ComEd) from the past year. 10_22_2022 to 10_22_2023
# Data from the [My Green Button](https://secure.comed.com/MyAccount/MyBillUsage/pages/secure/GreenButtonConnectDownloadMyData.aspx) webpage on the ComEd website.
# 
# ## My Weather Data Source
# My weather data was collected using [Meteostat](https://github.com/meteostat/meteostat-python). The Meteostat Python library provides a simple API for accessing open weather and climate data. The historical observations and statistics are collected by Meteostat from different public interfaces, most of which are governmental.
# 
# Among the data sources are national weather services like the National Oceanic and Atmospheric Administration (NOAA) and Germany's national meteorological service (DWD).

# # Data Column Descriptions
# 
# ## energy_df
# * **DATE**: Day recorded
# * **START_TIME**: start of recording (Date Hour:Minutes:Seconds)
# * **END_TIME**: end of recording (Date Hour:Minutes:Seconds)
# * **USAGE**: Electric usage (kWh)
# * **COST**: amount charged for energy usage (USD)
# 
# ## weather_df
# src: [Meteostat Documentation](https://dev.meteostat.net/python/hourly.html#data-structure)
# 
# | | | |
# |-|-|-|
# |**Column**|**Description**|**Type**|
# |**time**|datetime of the observation|Datetime64|
# |**temp**|air temperature in *°C*|Float64|
# |**dwpt**|dew point in *°C*|Float64|
# |**rhum**|relative humidity in percent (*%*)|Float64|
# |**prcp**|one hour precipitation total in *mm*|Float64|
# |**wdir**|average wind direction in degrees (*°*)|Float64|
# |**wspd**|average wind speed in *km/h*|Float64|
# |**pres**|average sea-level air pressure in *hPa*|Float64|

# In[46]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[47]:


# Import clean_energy_use spreadsheet from 'data' directory

# Define the directory path and the regular expression pattern
import glob
directory_path = "./data"
file_pattern = "energy_weather_*.csv"

# Use glob.glob to match filenames based on the pattern
file_path = glob.glob(f"{directory_path}/{file_pattern}")[0]
energy_weather_df = pd.read_csv(filepath_or_buffer=file_path)
energy_weather_df.info()
energy_weather_df.head()


# In[48]:


# convert the time cols into Datetime objs
energy_weather_df['time'] = pd.to_datetime(energy_weather_df['time'], format='%Y-%m-%d %H:%M:%S')
print(energy_weather_df['time'].dtypes)
energy_weather_df.head(4)


# In[50]:


# convert the START_TIME col into Datetime objs
energy_weather_df['HOUR'] = pd.to_datetime(energy_weather_df['HOUR'], format='%Y-%m-%d %H:%M:%S')
print(energy_weather_df['HOUR'].dtypes)
energy_weather_df.head(4)


# In[51]:


# Visualize the Cumulative Cost  &  rolling Temperature avg
# Calculate cumulative sum for 'COST'
# Calculate 14-day rolling sum for 'temp'
# since data is recorded 
hours=24
days=7
window_size0 = hours*days
window_name = "temp_"+str(days)+"_mean"

COST_Cumulative = energy_weather_df['COST'].cumsum()
rolling_avg_temp = energy_weather_df['temp'].rolling(window=window_size0).mean()

# Plotting
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
plt.show()


# # Analysis - Cumulative Cost  &  Temperature (7 Day avg)
# I was hoping to visualize the temperature/electricity_usage correlation. **NOTE:** USAGE & COST directly correlate.
# 
# * COST rises more steeply when the temperature is lower.
# * The visualization misses the positive temp/usage correlation at higher temperatures.
# 

# In[52]:


# graph the USAGE level for different temperature levels
# Convert 'temp' to Fahrenheit
energy_weather_df['temp_fahrenheit'] = (energy_weather_df['temp'] * 9/5) + 32

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
plt.show()


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
