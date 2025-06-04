#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objs as go

from plotly.subplots import make_subplots

import matplotlib.pyplot as plt
import streamlit as st


st.write("""
## [Energy_Use_Info](https://github.com/MichaelSalata/Energy_Use_Info)
This project visualizes insights from **weather data** from Meteostat & my ComEd **electricity meter data**. This helps with to quantifing the weather’s impact and preparing for an HVAC upgrade
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


# Sidebar setup
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










st.write(f""" **NOTE**: Data ranges from {cold_start_date} to {cold_end_date}""")


# filter for the warm days
warm_start_date = pd.to_datetime(warm_start_date)
warm_end_date = pd.to_datetime(warm_end_date)
warm_day_mask = (energy_weather_df['time'] >= warm_start_date) & (energy_weather_df['time'] <= warm_end_date)
filtered_df = energy_weather_df.loc[warm_day_mask]


# 7-day rolling average for COST & Temp
hours = 24
days = 7
window_size = hours * days
rolling_avg_cost = energy_weather_df['COST'].rolling(window=window_size).mean()
rolling_avg_temp = energy_weather_df['temp_fahrenheit'].rolling(window=window_size).mean()

# Create subplots with secondary_y axis for the two y-axes
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=energy_weather_df['time'], y=rolling_avg_cost, name='$BILL', mode='lines', line=dict(color='green')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=energy_weather_df['time'], y=rolling_avg_temp, name='All Temps', mode='lines', line=dict(color='royalblue')),
    secondary_y=True,
)

fig.add_vline(x=warm_start_date, line=dict(color='red'))
fig.add_vline(x=warm_end_date, line=dict(color='red'))
fig.add_trace(
    go.Scatter(x=energy_weather_df['time'].loc[warm_day_mask], y=rolling_avg_temp.loc[warm_day_mask], name='Warm Temps', mode='lines', line=dict(color='orange')),
    secondary_y=True,
)

fig.update_xaxes(title_text='<b>Date</b>')
fig.update_yaxes(title_text='<b>$BILL</b>', secondary_y=False, tickprefix='$')
fig.update_yaxes(title_text='<b>Temperature (°F)</b>', secondary_y=True)

fig.update_layout(
    title_text='Temperature & Energy Bill throughout the Year'
)

st.plotly_chart(fig)















st.write("""
### Lower Temperatures = Higher Energy Bill?
We see that the Energy Bill is significantly higher during the colder temperatures. Given how far the temperature is from a comfortable ~68degrees, it makes sense as the heating system is likely working very hard.""")

st.write("""The also graph demonstrates a clear inverse relationship between temperature and energy bill, with lower temperatures.""")

st.write("""
### Warm Days Tell the Opposite Story""")



rolling_avg_cost_filtered = rolling_avg_cost.loc[warm_day_mask]
rolling_avg_temp_filtered = rolling_avg_temp.loc[warm_day_mask]

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
During the warm months (June to September), the energy bill is higher when the temperature is higher, indicating that the cooling system is working harder to maintain a comfortable temperature.
""")











st.write("""## $Bill Correlations""")
# mapping for clearer column names
column_descriptions = {
    "temp_fahrenheit": "Air Temperature (°F)",
    "dwpt": "Dew Point (°C)",
    "wspd": "Wind Speed (km/h)",
    "wdir": "Wind Direction (°)",
    "pres": "Air Pressure (hPa)",
    "rhum": "Relative Humidity (%)",
    "prcp": "Precipitation (mm)"
}

# correlate BILL with all days
usage_corr = energy_weather_df.select_dtypes(include=[np.number]).corr()['COST'].sort_values(key=abs, ascending=False)

potential_corr_cols = ["temp_fahrenheit", "dwpt", "wspd", "wdir", "pres", "rhum", "prcp"]
correlation_display = usage_corr[potential_corr_cols].rename(index=column_descriptions)
correlation_display.name = "$BILL Correlation All Year"
st.write(correlation_display)


# correlate BILL with warm days
warm_day_data = energy_weather_df.loc[warm_day_mask]
warm_usage_corr = warm_day_data.select_dtypes(include=[np.number]).corr()['COST'].sort_values(key=abs, ascending=False)
warm_correlation_display = warm_usage_corr[potential_corr_cols].rename(index=column_descriptions)
warm_correlation_display.name = "$BILL Correlation (Jun-Sept)"
st.write(warm_correlation_display)
st.write("""
The correlation function confirms our observerations. The Air Temperature correlates negatively with the $BILL most of the year but positively during the summer months.
""")











st.write("""## Electricity NOT for Heating/Cooling""")

avg_usage_65_70 = energy_weather_df.loc[
    (energy_weather_df['temp_fahrenheit'] > 65) & (energy_weather_df['temp_fahrenheit'] < 70), 'USAGE'
].mean()

plt.figure(figsize=(10, 6))
plt.scatter(energy_weather_df['temp_fahrenheit'], energy_weather_df['USAGE'], alpha=0.5)

# plot the average among the points
plt.plot(temp_usage_avg['temp_fahrenheit'], temp_usage_avg['USAGE'], color='red')
plt.axhline(y=avg_usage_65_70, color='red', linestyle='--', label=f'Avg Usage (65°F-70°F): {avg_usage_65_70:.2f} kWh')

plt.title('Temperature vs. Energy Usage')
plt.xlabel('Temperature (°F)')
plt.ylabel('Energy Usage (kwh)')

st.pyplot(plt)
st.write(f"""
To help quantify how much of an impact the HVAC system has, we can to identify a baseline household electricity usage by learning the electricity usage for temperatures 65°F to 70°F. This range is typically comfortable for most households and when the HVAC system won't be running.
""")
st.write(f"""
The graph visualises this at a lateral line at: \n **{avg_usage_65_70:.2f} kWh**.
""")


# First, create the scatter plot
fig = px.scatter(energy_weather_df, x='temp_fahrenheit', y='USAGE', title='Temperature vs. Energy Usage (interactive)',
                 labels={'temp_fahrenheit': 'Temperature (°F)', 'USAGE': 'Energy Usage (kwh)'}, opacity=0.20)

fig.update_traces(marker=dict(symbol='x'), name='Scatter Points')

fig.add_trace(go.Scatter(x=temp_usage_avg['temp_fahrenheit'], y=temp_usage_avg['USAGE'], mode='lines', name='Average Usage', line=dict(color='red')))


fig.add_shape(
    type="line",
    x0=energy_weather_df['temp_fahrenheit'].min(),
    x1=energy_weather_df['temp_fahrenheit'].max(),
    y0=avg_usage_65_70,
    y1=avg_usage_65_70,
    line=dict(color="red", width=2, dash="dash"),
    name=f"Avg Usage (65°F-70°F): {avg_usage_65_70:.2f} kWh"
)

st.plotly_chart(fig)









# Sidebar: Temperature Bins Adjustment
st.sidebar.header("Temperature Bins")
temp_bin_size = st.sidebar.number_input("Temp Bin Size", value=10, step=1)
temp_bin_start = st.sidebar.number_input("Start Temperature", value=-10, step=temp_bin_size)
temp_bin_end = st.sidebar.number_input("End Temperature", value=110, step=temp_bin_size)
temp_bins = list(range(temp_bin_start, temp_bin_end, temp_bin_size))






st.write("""## Quantified Impact of Weather on Energy Usage""")

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
        name='Baseline USAGE'
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


fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')

st.plotly_chart(fig)

st.write("""The quantity of hours at the higher kWh usage helps indicate which system system is the biggest energy drain. In this case, it's the heating system.""")








# electricity usage for different temperature ranges
labels = ['Below 65°F', '65°F-70°F', 'Above 70°F']
below_65_usage = energy_weather_df.loc[energy_weather_df['temp_fahrenheit'] < 65, 'USAGE'].sum()
between_65_70_usage = energy_weather_df.loc[(energy_weather_df['temp_fahrenheit'] >= 65) & (energy_weather_df['temp_fahrenheit'] <= 70), 'USAGE'].sum()
above_70_usage = energy_weather_df.loc[energy_weather_df['temp_fahrenheit'] > 70, 'USAGE'].sum()

# electricity cost for different temperature ranges
below_65_cost = energy_weather_df.loc[energy_weather_df['temp_fahrenheit'] < 65, 'COST'].sum()
between_65_70_cost = energy_weather_df.loc[(energy_weather_df['temp_fahrenheit'] >= 65) & (energy_weather_df['temp_fahrenheit'] <= 70), 'COST'].sum()
above_70_cost = energy_weather_df.loc[energy_weather_df['temp_fahrenheit'] > 70, 'COST'].sum()

# pie chart setup
piechart_colors = ['blue',      'white',                'orange']
usage_values = [below_65_usage, between_65_70_usage,    above_70_usage]
cost_values = [below_65_cost,   between_65_70_cost,     above_70_cost]

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]],
                    subplot_titles=["Electricity Usage Distribution", "Electricity Cost Distribution"])

fig.add_trace(go.Pie(labels=labels, values=usage_values, hole=0.3, name="Usage", marker=dict(colors=piechart_colors)), row=1, col=1)
fig.add_trace(go.Pie(labels=labels, values=cost_values, hole=0.3, name="Cost", marker=dict(colors=piechart_colors)), row=1, col=2)

fig.update_layout(title_text='Electricity Usage and Cost Distribution by Temperature Range')
st.plotly_chart(fig)

st.write(f"""
- **Below 65°F**: 
    - Total Usage: {below_65_usage:.0f} kWh
    - Total Cost: ${below_65_cost:.2f}
- **65°F-70°F**: 
    - Total Usage: {between_65_70_usage:.0f} kWh
    - Total Cost: ${between_65_70_cost:.2f}
- **Above 70°F**: 
    - Total Usage: {above_70_usage:.0f} kWh
    - Total Cost: ${above_70_cost:.2f}
""")
st.write("""
The heating system is the clear point of potential improvement, as the data shows significantly higher energy usage and cost below 65°F. Optimizing or upgrading the heating system could lead to substantial cost savings.
""")

st.write("""## Project Use Cases""")
st.write("""
1. **HVAC System Optimization**: Use the data to identify the most energy-intensive temperature ranges and optimize heating/cooling systems accordingly.
2. **Renewable Energy Integration**: Evaluate the feasibility of renewable energy sources (e.g., solar panels) to offset high energy usage during peak seasons.
3. **Cost Savings Calculation**: Analyze the potential cost savings of upgrading the heating system by comparing current energy usage and costs with projected values for more efficient systems.
""")


