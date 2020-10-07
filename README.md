# Manhattan Taxi Demand Predictor
![taxi image](/img/manhattan_taxis_image.jpg)

This project has been developed by [Ángel Ruiz-Peinado Sánchez](https://www.linkedin.com/in/angelruizpeinado/).  
Final Project - Master in Data Science - [KSchool](https://www.kschool.com/) Madrid.

***I am currently doing some modifications to this readme file and the info may not be shown in the appropriate order. Please, read the [wiki](https://github.com/angelrps/MasterDataScience_FinalProject/wiki) for an in-depth understanding of the porject. Apologies for the inconvenience.***

* [1_Introduction](#1_Introduction)
* [2_Methodology](#2_Methodology)
   * [2_1_Data Engineering](#2_1_Data-Engineering)
   * [2_2_Machine Learning Techniques](#2_2_Machine-Learning-Techniques)
   * [2_3_Statistical Methodologies](#2_3_Statistical-Methodologies)
* [3_What Data Have I used?](#3_What-Data-Have-I-used?)
* [4_Internal Structure](#4_Internal-Structure)
  * [4_1_Data Processing](#4_1_Data-Processing)
    * [4_1_1_Data Acquisition](#4_1_1_Data-Acquisition)
    * [4_1_2_Data Preparation](#4_1_2_Data-Preparation)
    * [4_1_3_Data Analysis](#4_1_3_Data-Analysis)
  * [4_2_Modeling](#)
  * [4_3_Front-End](#)
    * [4_3_1_Generate Model Inputs](#)
    * [4_3_2_Generate Predictions](#)
    * [4_3_3_Visualize Results](#)    
* [5_What do you need to run the project?](#)
  * [5_1_Dependencies and modules](#)
  * [5_2_Execution Guide](#)
  * [5_3_User Manual](#)  
* [6_Conclusions](#6_Conclusions)

# 1_Introduction
The purpose of this document is to give you a quick overview of the project. **If you want to read the whole Project´s documentation in much more detail, go straight to the [wiki page](https://github.com/angelrps/MasterDataScience_FinalProject/wiki).**<br>

**Manhattan Taxi Demand Predictor** is a machine learning app that predicts for the next three days how many passengers will request a taxi in Manhattan (New York). Predictions are shown grouped by city zone and in hourly periods.

## Why? And why is it relevant?
I wanted my project to be potentially **profitable in the real market**. If a taxi driver could know in advance (and with precision) which boroughs or areas are going to have the biggest demand, he could optimize his workday by driving only around those areas. He could choose whether to earn more money in the same time or save that time for his family/personal life. Either way, it will improve his life.

On the other side, I wanted to **solve an existing problem**. There has been a lot of debate in the past regarding [how Uber is literally eating the traditional street hail taxi market](https://www.cityandstateny.com/articles/policy/transportation/comparing-cabs-uber-new-york-city.html). Taxi drivers are afraid that they cannot compete with the kind of on-demand fare-adjusted service Uber provide, based in cutting-edge technology. I think that traditional taxi drivers should also make use of advance technology like my machine learning app in order to improve their service and profitability.

# 2_Methodology
## 2_1_Data Engineering
### Data pipelines
I have created a data pipeline with python to transform gigabytes of data into structures needed for the analysis.
### Web Scraping
I have used **Selenium Webdriver** to scrape weather precipitation forecast from www.wunderground.com.

## 2_2_Machine Learning Techniques
### Regression
I have used **linear regression** and non-linear regression models such as **Decision Trees** or **K-Nearest Neighbours**.
### Ensemble learning
I have applied ensemble learning methods such as **Bagging** (with KNN), **Random Forest** and **Gradient Boosting**.

I have also made used of ``GridSearchCV`` to find the best parameters.

## 2_3_Statistical Methodologies
### Predictive Analytics
Such as **data mining** and **data modeling**.
### Exploratory Data Analysis (EDA)
To spot anomalies, test hypothesis and check assumptions with the help of summary statistics and graphical representations. 
   
# 3_What Data have I used?
* **2019 Yellow Taxis data**: I have downloaded this data set from [NYC Open Data](https://opendata.cityofnewyork.us/), a free public data source of New York City. You can download the [dataset here](https://data.cityofnewyork.us/Transportation/2019-Yellow-Taxi-Trip-Data/2upf-qytp), although you don´t need it to run this app.<br>
The dataset includes 17 fields (you can have a look at the [data dictionary here](https://data.cityofnewyork.us/api/views/2upf-qytp/files/4a7a18af-bfc8-43d1-8a2e-faa503f75eb5?download=true&filename=data_dictionary_trip_records_yellow.pdf)). I was only interested in:

  * ``tpep_pickup_datetime``: The date and time when the meter was engaged.
  * ``PULocationID``: TLC Taxi Zone in which the taximeter was engaged. These id's correspond with the boundary zones of the polygone shapefile.
  
* **Weather precipitation history**: I wanted to include precipiation data to train the models, as it is sensible to think that rain would affect the taxi demand. The analysis would show me afterwards that this is not true. I downloaded it from the [NOAA](https://www.ncdc.noaa.gov/cdo-web/datasets#LCD) (National Centers for Environmental Information).

* [**Polygon shapefile**](https://archive.nyu.edu/handle/2451/36743): In order to visualize the results I needed geometric data. This ``.shape`` file represents the boundaries zones for taxi pickups as delimited by the New York City Taxi and Limousine Commission (TLC).
<img src="https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/taxi_zone_map_manhattan.jpg" width="400">

* **Weather Precipitation Forecast**: I scrape this data from [www.wunderground.com](https://www.wunderground.com/hourly/us/ny/new-york-city) in real time when executing the web app to get the predictions.

# 4_Internal Structure
I can internally divide the project in 3 parts: Data Processing, Modeling and Front-End.

## 4_1_Data Processing

### 4_1_1_Data Acquisition
This is just downloading the datasets from the sources explained above.

### 4_1_2_Data Preparation
This is the most laborious part. It includes exploring the *taxis* and *weather* datasets to find anomalies, patterns, insights, test hypothesis, etc.  
Once both datasets are cleaned and transformed, I joined them together in a single **.csv** file (``Data_Cleaned_2019_To_Model.csv``) which is ready to be analysed and/or served as input for the regression models.  
The *taxis* dataset was specially hard, as its size was to heavy (8GB and 83 million lines) to be read with my computer's memory. I had to compress it (800MB), and load it in chunks of 10.000 lines, perform all the analysis and transformations and put the chunks back together in a single file.

### 4_1_3_Data Analysis
Now is time to explore the data further by creating some self-explanatory graphs.  
#### 1. Map pickups by zone
I drew a choropleth map showing Manhattan tazi zones by number of pickups, highlighting the top ten in red. These zones should coincide with the predictions of the machine learning models.

![map](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Map.PNG)

#### 2. Linear chart pickups over time
I have analysed pickups' evolution over different periods of time looking for patterns.  

**Pickpus evolution over Months**  
- The number of pickups over the year is quite constant.  
- The only variation is a small decrease of pickups over the Summer months: July and August. This can mean that most taxis are taken by new yorkers (not tourists), and in this period new yorkers travel away from the city.

![evolution months](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_Months.PNG)


**Pickpus evolution over Weeks**  
This graph shows better how the taxi demand drops drastically on the USA Federal holidays:
- New Year's Day: 1st of January.
- Independence Day: 4th July.
- Labor Day: first Monday of September.
- Thanksgiving: 4th Thursday of November.

![evolution weeks](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_Weeks.PNG)

**Pickpus evolution over a Single Week**  
This graph shows the average number of pickups per weekday. Monday and Sunday are a bit quieter than the other days, but not much.

![evolution single week](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_SingleWeek.PNG)

**Pickpus evolution over a Day**  
This graph shows the average number of pickups over a day:
- 18:00 and 19:00 are the peak hours.
- 1:00 am to 6:00 am the quieter.

![evolution day](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_Day.PNG)

#### 3.Scatter Plot Relation between Precipitation and Pickups
I created this set of plots to find a correlation between precipitation and pickups. My hypothesis is that there are more pickups in rainy days, because people that usually walk are more likely to get a taxi.  
Most of the days it does not rain, so I will just plot rainy days and remove outliers above 0.5 precipitation.  
Surprisingly to me, the scatter plot was very clear: **there is no correlation between ``precipitation`` and ``pickups``.**

![pickups vs prec 3](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_PrepVSPickups_3.PNG)

#### 4. Pickups in Rainy Day vs Not Rainy Days
I wanted to confirm with a second method that my hypothesis about rainy days was wrong, comparing the average of pickups in rainy days vs not rainy days. The results are crystal clear, there is not relation at all between rain and pickups. The average shown below is nearly the same.

-|precipitation|pickups
-|-|-
0|0.0|127.548318
1|1.0|131.911881



  * [4_2_Modeling](#)
  * [4_3_Front-End](#)
    * [4_3_1_Generate Model Inputs](#)
    * [4_3_2_Generate Predictions](#)
    * [4_3_3_Visualize Results](#)    
* [5_What do you need to run the project?](#)
  * [5_1_Dependencies and modules](#)
  * [5_2_Execution Guide](#)
  * [5_3_User Manual](#)  
* [6_Conclusions](#6_Conclusions)


 
# 3_What do you need to run the project?
## 3_1_Dependencies and modules
You need the following dependencies and modules installed in your environment:
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
- ``Chrome Driver``: it needs to be installed from [here](https://sites.google.com/a/chromium.org/chromedriver/home) and saved in the same folder as the notebook (``./notebooks``). In the repository my version of ``Chromedriver.exe`` is copied but it could not work on your computer. The driver must be compatible with the installed [``Chrome`` version](https://sites.google.com/a/chromium.org/chromedriver/downloads/version-selection).


## 3_2_Execution Guide
If you want to replicate the project, execute the notebooks in the following order:
### Explore, Clean and Transform
**1. [Taxis Dataset](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Taxis_Clean_Transform.ipynb)**: explore, clean and transforms taxis data set into structures needed for the analysis.
**2. [Weather Dataset](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Weather_Clean_Transform.ipynb)**: explore, clean and transforms weather data set into structures needed for the analysis.



# 4_What do you need to run the project?


## 4_2_Steps
**Note**:  There are multiple environments on which you can execute the app and I am not capable to cover them all. So I will explain my personal one: Ubuntu running on WSL (Windows Subsystem for Linux).<br>
Follow these steps to run the app:  
1. Clone or download the repository.
2. Launch Ubuntu and navigate to ``\MasterDataScience_FinalProject\notebooks``.
3. Type ``streamlit run streamlit_app.py``.
4. Copy the returned Network URL ``http://192.168.1.106:8501 `` and paste in your internet browser.
5. That´s it! The app takes a couple of seconds to load. This is mainly due to the real time web-scraping. 

## 4_3_User Manual
* Use the controls on the side bar to select:
   * Graph type: map or line chart.
   * Day.
   * Time frame.
* The map will colour up according to the number of pickups (hover over the mouse to look at the exact numbers).
* The line chart will show pickups evolution over a whole day for each zone. Highlight a zone by selecting in the chart or in the legend.

#### Click in the image to see it in action!
[![see it in action](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Miniatura2.png)](https://youtu.be/xO07tr9dJ5o)

## Want to know more about this app? Check the [wiki](https://github.com/angelrps/MasterDataScience_FinalProject/wiki)
