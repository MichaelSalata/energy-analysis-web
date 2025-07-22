
## [Fully Interactable Webhosted Analysis](https://energy-analysis-web.streamlit.app/)
**NOTE**: Web Hosting may take a minute to load

Energy Use Info
-----------------------
To aid in preparing for an HVAC upgrade, the [Energy-Use Info](https://github.com/MichaelSalata/Energy_Use_Info) project gathers and cleans **Meteostat weather data** & **ComEd energy meter data**.
This project then further analyzes the data and visualizes the insights in a webdashboard.

![bill_vs_weather](https://github.com/MichaelSalata/energy-analysis-web/blob/main/imgs/bill_vs_weather.png)
Sample Image from the [Webhosted Analysis](https://energy-analysis-web.streamlit.app/)

How to Launch it Yourself
-----------------------
1. download the project
```bash
git clone https://github.com/MichaelSalata/energy-analysis-web.git
```
2. Create a Virtual Environment in the project
```bash
cd energy-analysis-web/
python3 -m venv venv
```
3. Install the requirements
```bash
pip install -r requirements.txt
```
4. Run streamlit
```bash
streamlit run ew_plotly_streamlit.py
```
