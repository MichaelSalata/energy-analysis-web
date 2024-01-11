st.write("""
# Introduction
The [Energy_Use_Info](https://github.com/MichaelSalata/Energy_Use_Info) project is meant to gather insights on electricity usage relative to weather data.

 ## Data Pipeline
 ### Energy Data
1) Energy data is first downloaded from my electricity company, [ComEd](https://secure.comed.com/MyAccount/MyBillUsage/pages/secure/GreenButtonConnectDownloadMyData.aspx).
2) 
 ### Weather Data
 
1) Historical weather data is gotten from [Meteostat](https://github.com/meteostat/meteostat-python), which sources it's USA data from the NOAA.
2) Weather data is cleaned using "green_button_data_cleaning.ipynb" and outputted to clean_energy_use_*.csv
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