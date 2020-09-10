# Manhattan Taxi Demand Predictor
![taxi image](/img/manhattan_taxis_image.jpg)

This project has been developed by [Ángel Ruiz-Peinado Sánchez](https://www.linkedin.com/in/angelruizpeinado/).  
Final Project - Master in Data Science - [KSchool](https://www.kschool.com/) Madrid.

* [1_Introduction](#1_Introduction)
* [2_What Data have I used?](#2_What-Data-have-I-used)
* [3_Methodology and Tools](#3_Methodology-and-Tools)
* [4_What do you need to run the project?](#4_What-do-you-need-to-run-the-project)
    * [4_1_Dependencies and modules](#4_1_Dependencies-and-modules)
    * [4_2_Steps](#4_2_Steps)
    * [4_3_User Manual](#4_3_User-Manual)

# 1_Introduction
The purpose of this README file is to give you a quick overview of the project and go through the necessary steps to run the app in your computer.<br>
**If you are a KSchool teacher or want to read the whole Project´s documentation in much more detail, go straight to the [wiki page](https://github.com/angelrps/MasterDataScience_FinalProject/wiki).**

## 1_1_What is this?
It is a machine learning app that predicts for the next three days how many passengers will request a taxi in Manhattan (New York). Predictions are made by city zone and in hourly periods.

## 1_2_Why?
If a taxi driver could know in advance (and with precision) which boroughs or areas are going to have the biggest demand, he could optimize his workday by driving only around those areas. He could choose whether to earn more money in the same time or save that time for his family/personal life. Either way, it will improve his life.

## 1_3_Why is relevant?
There has been a lot of debate in the past regarding [how Uber is literally eating the traditional street hail taxi market](https://www.cityandstateny.com/articles/policy/transportation/comparing-cabs-uber-new-york-city.html). Taxi drivers are afraid that they cannot compete with the kind of on-demand fare-adjusted service Uber provide, based in cutting-edge technology.

I think that traditional taxi drivers should also make use of advance technology like this machine learning app in order to improve their service and profitability.

# 2_What Data have I used?
* **2019 Yellow Taxis data**: I have downloaded the data from [NYC Open Data](https://opendata.cityofnewyork.us/), a free public data source of New York City. You can download the [dataset here](https://data.cityofnewyork.us/Transportation/2019-Yellow-Taxi-Trip-Data/2upf-qytp), although you don´t need it to run this app.<br>
The dataset includes 17 fields (you can have a look at the [data dictionary here](https://data.cityofnewyork.us/api/views/2upf-qytp/files/4a7a18af-bfc8-43d1-8a2e-faa503f75eb5?download=true&filename=data_dictionary_trip_records_yellow.pdf)). I was only interested in:

  * ``tpep_pickup_datetime``: The date and time when the meter was engaged.
  * ``PULocationID``: TLC Taxi Zone in which the taximeter was engaged. These id's correspond with the boundary zones of the polygone shapefile.
  
* **Weather precipitation history**: downloaded from the [NOAA](https://www.ncdc.noaa.gov/cdo-web/datasets#LCD) (National Centers for Environmental Information).

* **Weather Precipitation Forecast**: scraped from [www.wunderground.com](https://www.wunderground.com/hourly/us/ny/new-york-city).

* [**Polygon shapefile**](https://archive.nyu.edu/handle/2451/36743): Represents the boundaries zones for taxi pickups as delimited by the New York City Taxi and Limousine Commission (TLC).
<img src="https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/taxi_zone_map_manhattan.jpg" width="400">

# 3_Methodology and Tools
* Jupyter Notebook as a workframe.
* Python 3 (pandas, numpy, sklearn) for data cleaning, engineering and modelling (regression models).
* Matplotlib, Seaborn, Bokeh and Altair for data analysis and graphic representation.
* Selenium Webdriver for web scraping.
* Streamlit for webapp front-end.

# 4_What do you need to run the project?
## 4_1_Dependencies and modules
- ``pandas``
- ``numpy``
- ``matplotlib``
- ``seaborn``
- ``altair``
- ``geopandas``
- ``descartes``
- ``bokeh 2.`` or superior
- ``shapely``
- ``scikit-learn``
- ``pickle``
- ``streamlit`` 0.57 or superior
- ``selenium``
- Google Chrome.

## 4_2_Steps
**Note**:  There are multiple environments on which you can execute the app and I am not capable to cover them all. So I will explain my personal one: Ubuntu running on WSL (Windows Subsystem for Linux).
1. Clone or download the repository.
2. Launch Ubuntu and navigate to ``\MasterDataScience_FinalProject\notebooks``.
3. Type ``streamlit run streamlit_app.py``.
4. Copy the returned Network URL ``http://192.168.1.106:8501 `` and paste in your internet browser.
5. That´s it! The app takes a couple of seconds to load. This is mainly due to the real time web-scraping. 

## 4_3_User Manual
* Use the controls on the side bar to select:
   * Graph type: map or line chart.
   * Time frame.
   * Day.
* The map will colour up according to the number of pickups (hover over the mouse to look at the exact numbers).
* The line chart will show pickups evolution over a whole day for each zone. Highlight a zone by selecting in the chart or in the legend.

#### Click in the image to see it in action!
[![see it in action](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Miniatura2.png)](https://youtu.be/xO07tr9dJ5o)

## Want to know more about this app? Check the [wiki](https://github.com/angelrps/MasterDataScience_FinalProject/wiki)
