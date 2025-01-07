#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objs as go
import matplotlib as plt
import streamlit as st



st.write("""
## [Energy_Use_Info](https://github.com/MichaelSalata/Energy_Use_Info)
This project visualizes insights using my **weather & electricity** meter data.

Visit [Energy_Use_Info project page](https://github.com/MichaelSalata/Energy_Use_Info/blob/main/README.md) for how the data was **downloaded, cleaned & visualized**  
""")




import glob
directory_path = "./data"
file_pattern = "energy_weather_*.csv"

file_path = glob.glob(f"{directory_path}/{file_pattern}")[0]
energy_weather_df = pd.read_csv(filepath_or_buffer=file_path)



# process data for visualization

# convert the time cols into Datetime objs
energy_weather_df['time'] = pd.to_datetime(energy_weather_df['time'], format='%Y-%m-%d %H:%M:%S')

# convert the START_TIME col into Datetime objs
energy_weather_df['HOUR'] = pd.to_datetime(energy_weather_df['HOUR'], format='%Y-%m-%d %H:%M:%S')

# Create a column for the temperature in fahrenheit
energy_weather_df['temp_fahrenheit'] = (energy_weather_df['temp'] * 9/5) + 32



# Sidebar: Date Range Picker for Warm Days
st.sidebar.header("Blue Date Range")
cold_start_date = st.sidebar.date_input("Start Date", energy_weather_df['time'].min())
cold_end_date = st.sidebar.date_input("End Date", energy_weather_df['time'].max())

# Sidebar: Date Range Picker for Warm Days
st.sidebar.header("Orange Date Range")
warm_start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2023-06-20'))
warm_end_date = st.sidebar.date_input("End Date", pd.to_datetime('2023-09-19'))


# Calculating the average energy usage for each temperature and plotting a line
# Group by temperature and calculate mean USAGE
temp_usage_avg = energy_weather_df.groupby('temp_fahrenheit')['USAGE'].mean().reset_index()

# Sort the values for a smooth line
temp_usage_avg = temp_usage_avg.sort_values(by='temp_fahrenheit')



# Filter the DataFrame for the warm days
# Convert start and end dates to datetime64[ns] type
warm_start_date = pd.to_datetime(warm_start_date)
warm_end_date = pd.to_datetime(warm_end_date)

# Convert start and end dates to datetime64[ns] type
warm_start_date = pd.to_datetime(warm_start_date)
warm_end_date = pd.to_datetime(warm_end_date)

# Filter the DataFrame for the warm days
warm_day_mask = (energy_weather_df['time'] >= warm_start_date) & (energy_weather_df['time'] <= warm_end_date)
filtered_df = energy_weather_df.loc[warm_day_mask]


# Calculate 7-day rolling average for COST & Temp
hours = 24
days = 7
window_size = hours * days
rolling_avg_cost = energy_weather_df['COST'].rolling(window=window_size).mean()
rolling_avg_temp = energy_weather_df['temp_fahrenheit'].rolling(window=window_size).mean()


from plotly.subplots import make_subplots

# Create subplots with secondary_y axis for the two y-axes
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=energy_weather_df['time'], y=rolling_avg_cost, name='$COST', mode='lines', line=dict(color='green')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=energy_weather_df['time'], y=rolling_avg_temp, name='All Temps', mode='lines', line=dict(color='royalblue')),
    secondary_y=True,
)


fig.add_vline(x=warm_start_date)
fig.add_vline(x=warm_end_date)
fig.add_trace(
    go.Scatter(x=energy_weather_df['time'].loc[warm_day_mask], y=rolling_avg_temp.loc[warm_day_mask], name='Warm Temps', mode='lines', line=dict(color='orange')),
    secondary_y=True,
)

fig.update_xaxes(title_text='<b>Date</b>')
fig.update_yaxes(title_text='<b>$COST: 7-day Rolling Avg</b>', secondary_y=False, tickprefix='$')
fig.update_yaxes(title_text='<b>Temperature (°F)</b>', secondary_y=True)

fig.update_layout(
    title_text='Temperature & Energy Bill throughout the Year'
)

st.plotly_chart(fig)




st.write("""## $Bill Correlates with Temperature""")
usage_corr = energy_weather_df.select_dtypes(include=[np.number]).corr()['COST'].sort_values(key=abs, ascending=False)
potential_corr_cols = ["temp_fahrenheit", "dwpt", "wspd", "wdir", "pres", "rhum", "prcp"]
st.write(usage_corr[potential_corr_cols])


st.write("""
## Lower Temperatures = Higher Energy Bill?
The Bill inversely correlates with Temperature between 65F to -10F. We can infer that the heating system is the biggest Energy drain.
""")

st.write("""
## Warm Days Tell the Opposite Story
""")


# filtered_df = energy_weather_df[(energy_weather_df['time'] >= start_date) & (energy_weather_df['time'] <= end_date)]

# Calculate 7-day rolling averages for the filtered data
# rolling_avg_cost_filtered = filtered_df['COST'].rolling(window=7*24, min_periods=1).mean()
# rolling_avg_temp_filtered = filtered_df['temp'].rolling(window=7*24, min_periods=1).mean()

# rolling_avg_cost_filtered = rolling_avg_cost[(rolling_avg_cost['time'] >= start_date) & (rolling_avg_cost['time'] <= end_date)]
# rolling_avg_temp_filtered = rolling_avg_temp[(rolling_avg_temp['time'] >= start_date) & (rolling_avg_temp['time'] <= end_date)]

rolling_avg_cost_filtered = rolling_avg_cost.loc[warm_day_mask]
rolling_avg_temp_filtered = rolling_avg_temp.loc[warm_day_mask]

# Create subplots with secondary_y axis for the two y-axes
fig_filtered = make_subplots(specs=[[{"secondary_y": True}]])

fig_filtered.add_trace(
    go.Scatter(x=filtered_df['time'], y=rolling_avg_cost_filtered, name='$COST', mode='lines', line=dict(color='green')),
    secondary_y=False,
)

fig_filtered.add_trace(
    go.Scatter(x=filtered_df['time'], y=rolling_avg_temp_filtered, name='Warm Temps', mode='lines', line=dict(color='orange')),
    secondary_y=True,
)

fig_filtered.update_xaxes(title_text='<b>Date</b>')
fig_filtered.update_yaxes(title_text='<b>$COST: 7-day Rolling Avg</b>', secondary_y=False, tickprefix='$')
fig_filtered.update_yaxes(title_text='<b>Temperature (°F)</b>', secondary_y=True)

fig_filtered.update_layout(
    title_text='Temperature & Energy Bill (Jun-Sept)'
)

# Display the filtered graph in Streamlit
st.plotly_chart(fig_filtered)


st.write("""
## Electricity NOT for Heating/Cooling
Using the trends we see for Heating or Cooling, we infer electricity usage for rest of the household from the minimum on the chart.
""")




import matplotlib.pyplot as plt

# Scatter plot of Temperature vs. Energy Usage
plt.figure(figsize=(10, 6))
plt.scatter(energy_weather_df['temp_fahrenheit'], energy_weather_df['USAGE'], alpha=0.5)

# Plotting the line
plt.plot(temp_usage_avg['temp_fahrenheit'], temp_usage_avg['USAGE'], color='red')

# Adding titles and labels
plt.title('Temperature vs. Energy Usage')
plt.xlabel('Temperature (°F)')
plt.ylabel('Energy Usage (kwh)')
# plt.show()
st.pyplot(plt)



# First, create the scatter plot
fig = px.scatter(energy_weather_df, x='temp_fahrenheit', y='USAGE', title='Temperature vs. Energy Usage (interactive)',
                 labels={'temp_fahrenheit': 'Temperature (°F)', 'USAGE': 'Energy Usage (kwh)'}, opacity=0.5)

fig.update_traces(marker=dict(symbol='x'))

# add the average energy usage line on top
fig.add_trace(go.Scatter(x=temp_usage_avg['temp_fahrenheit'], y=temp_usage_avg['USAGE'], mode='lines', name='Average Usage', line=dict(color='red')))

st.plotly_chart(fig)




# Sidebar: Temperature Bins Adjustment
st.sidebar.header("Temperature Bins")
temp_bin_size = st.sidebar.number_input("Temp Bin Size", value=10, step=1)
temp_bin_start = st.sidebar.number_input("Start Temperature", value=-10, step=temp_bin_size)
temp_bin_end = st.sidebar.number_input("End Temperature", value=110, step=temp_bin_size)
temp_bins = list(range(temp_bin_start, temp_bin_end, temp_bin_size))

# Categorize rows based on temperature bins
energy_weather_df['temp_bins'] = pd.cut(energy_weather_df['temp_fahrenheit'], bins=temp_bins, right=False)

# Group by temperature bins and calculate average 'USAGE' and count
average_data = energy_weather_df.groupby('temp_bins').agg({'USAGE': ['mean', 'count']}).reset_index()
average_data.columns = ['temp_bins', 'avg_USAGE', 'count']

# electricity USAGE per 10°F Range bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(
        x=average_data['temp_bins'].astype(str),
        y=average_data['avg_USAGE'],
        text=average_data['count'].apply(lambda x: f'{x}<br>hrs'),
        textposition='auto',
        marker_color='royalblue',
        name='Average USAGE'
    )
])

fig.update_layout(
    title='electricity USAGE per 10°F Range',
    xaxis_title='Temp Ranges (10°F)',
    yaxis_title='Avg USAGE per Hour (kWh)',
    xaxis_tickangle=-45
)

fig.update_layout(
    title_text='Energy Usage per 10°F Range',
    barmode='group',
    xaxis_tickangle=-45,
    legend=dict(x=0.1, y=1.1, orientation="h")
)

# Add gridlines
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')

st.plotly_chart(fig)

