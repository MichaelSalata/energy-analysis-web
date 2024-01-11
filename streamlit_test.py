
import streamlit as st

st.write("""
# Introduction
The [Energy_Use_Info](https://github.com/MichaelSalata/Energy_Use_Info) is meant to gather insights on electricity usage.
 
 This notebook looks for insights into electricity usage relative to weather data.
 
 ## Data
 * This notebook uses data cleaned with "green_button_data_cleaning.ipynb" aka:  clean_energy_use_*.csv
 * This notebook uses data cleaned with "weather_data_cleaning.ipynb.ipynb" aka: clean_weather_*.csv
 
 
 ## My Energy Data Source
 Currently, the data is from my energy company(ComEd) from the past year. 10_22_2022 to 10_22_2023
 Data from the [My Green Button](https://secure.comed.com/MyAccount/MyBillUsage/pages/secure/GreenButtonConnectDownloadMyData.aspx) webpage on the ComEd website.
 
## My Weather Data Source
My weather data was collected using [Meteostat](https://github.com/meteostat/meteostat-python). The Meteostat Python library provides a simple API for accessing open weather and climate data. The historical observations and statistics are collected by Meteostat from different public interfaces, most of which are governmental.
 
Among the data sources are national weather services like the National Oceanic and Atmospheric Administration (NOAA) and Germany's national meteorological service (DWD).
# Data Column Descriptions
 
 ## energy_df
 * **DATE**: Day recorded
 * **START_TIME**: start of recording (Date Hour:Minutes:Seconds)
 * **END_TIME**: end of recording (Date Hour:Minutes:Seconds)
 * **USAGE**: Electric usage (kWh)
 * **COST**: amount charged for energy usage (USD)
 
 ## weather_df
 src: [Meteostat Documentation](https://dev.meteostat.net/python/hourly.html#data-structure)
""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'GOOGL'
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)