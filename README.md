# Manhattan Taxi Demand Predictor
![taxi image](/img/manhattan_taxis_image.jpg)

This project has been developed by [Ángel Ruiz-Peinado Sánchez](https://www.linkedin.com/in/angelruizpeinado/).  
Final Project - Master in Data Science - [KSchool](https://www.kschool.com/) Madrid.

* [1_Introduction](#1_Introduction)
* [2_Methodology](#2_Methodology)
   * [2_1_Data Engineering](#2_1_Data-Engineering)
   * [2_2_Machine Learning Techniques](#2_2_Machine-Learning-Techniques)
   * [2_3_Statistical Methodologies](#2_3_Statistical-Methodologies)
* [3_What Data Have I used?](#3_What-Data-Have-I-used)
* [4_Internal Structure](#4_Internal-Structure)
  * [4_1_Data Processing](#4_1_Data-Processing)
  * [4_2_Modeling](#4_2_Modeling)
  * [4_3_Front-End](#4_3_Front-End)   
* [5_What do you need to run the project?](#5_What-do-you-need-to-run-the-project)
  * [5_1_Dependencies and modules](#5_1_Dependencies-and-modules)
  * [5_2_Execution Guide](#5_2_Execution-Guide)
  * [5_3_User Manual](#5_3_User-Manual)  
* [6_Conclusions](#6_Conclusions)

# 1_Introduction
The purpose of this document is to give you a quick overview of the project. **If you want to read the whole Project´s documentation in much more detail, go straight to the [wiki page](https://github.com/angelrps/MasterDataScience_FinalProject/wiki).**<br>

**Manhattan Taxi Demand Predictor** is a machine learning app that predicts for the next three days how many passengers will request a taxi in Manhattan (New York). Predictions are shown grouped by city zone and in hourly periods.

## Why? And why is it relevant?
On the one hand, I wanted my project to be potentially **profitable in the real market**. If a taxi driver could know in advance (and with precision) which boroughs or areas are going to have the biggest demand, he could optimize his workday by driving only around those areas. He could choose whether to earn more money in the same time or save that time for his family/personal life. Either way, it will improve his life.

On the other hand, I wanted to **solve an existing problem**. There has been a lot of debate in the past regarding [how Uber is literally eating the traditional street hail taxi market](https://www.cityandstateny.com/articles/policy/transportation/comparing-cabs-uber-new-york-city.html). Taxi drivers are afraid that they cannot compete with the kind of on-demand fare-adjusted service Uber provide, based in cutting-edge technology. I think that traditional taxi drivers could also make use of advance technology like my machine learning app in order to improve their service and profitability.

# 2_Methodology
## 2_1_Data Engineering
* **Data pipelines**: I created a data pipeline with python to transform gigabytes of data into structures needed for the analysis.
* **Web Scraping**: I used **Selenium Webdriver** to scrape weather precipitation forecast from www.wunderground.com.

## 2_2_Machine Learning Techniques
* **Regression**: I used **linear regression** and non-linear regression models such as **Decision Trees** or **K-Nearest Neighbours**.
* **Ensemble learning**: I have applied ensemble learning methods such as **Bagging** (with KNN), **Random Forest** and **Gradient Boosting**.

I also used ``GridSearchCV`` to find the best parameters.

## 2_3_Statistical Methodologies
* **Predictive Analytics**: Such as **data mining** and **data modeling**.
* **Exploratory Data Analysis (EDA)**: To spot anomalies, test hypothesis and check assumptions with the help of summary statistics and graphical representations. 
   
# 3_What Data Have I used?
* **2019 Yellow Taxis data**: I downloaded this dataset from [NYC Open Data](https://opendata.cityofnewyork.us/), a free public data source of New York City. You can download the [dataset here](https://data.cityofnewyork.us/Transportation/2019-Yellow-Taxi-Trip-Data/2upf-qytp), although you don´t need it to run this app (only if you want to replicate the project).<br>
The dataset includes 17 fields (you can have a look at the [data dictionary here](https://data.cityofnewyork.us/api/views/2upf-qytp/files/4a7a18af-bfc8-43d1-8a2e-faa503f75eb5?download=true&filename=data_dictionary_trip_records_yellow.pdf)). I was only interested in:

  * ``tpep_pickup_datetime``: The date and time when the meter was engaged.
  * ``PULocationID``: TLC Taxi Zone in which the taximeter was engaged. These id's correspond with the boundary zones of the polygone shapefile.
  
* **Weather precipitation history**: I wanted to include precipitation data to train the models, as it is sensible to think that rain would affect the taxi demand. The analysis would show me afterwards that this is not true. I downloaded it from the [NOAA](https://www.ncdc.noaa.gov/cdo-web/datasets#LCD) (National Centers for Environmental Information) but it takes a couple of days for them to respond your query so you can also download it from my repo [here](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/data/NOAA_CentralPark_Weather.csv).

* **Polygon shape file**: In order to visualize the results I needed geometric data. This ``.shp`` file represents the boundaries zones for taxi pickups as delimited by the New York City Taxi and Limousine Commission (TLC). You can download the file from several [websites](https://archive.nyu.edu/handle/2451/36743) or from my [repo](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/data/taxi_zones/taxi_zones.shp).
<img src="https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/taxi_zone_map_manhattan.jpg" width="400">

* **Weather Precipitation Forecast**: When executing the app, it scrapes precipitation forecast from [www.wunderground.com](https://www.wunderground.com/hourly/us/ny/new-york-city) in real time to get the predictions.

# 4_Internal Structure
I can divide the project in 3 parts: **Data Processing**, **Modeling** and **Front-End**.

![Internal Structure](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Internal%20Structure2.PNG)

## 4_1_Data Processing
Includes **Data Acquisition** (this is just downloading the datasets from the sources explained above), **Data Preparation** and **Data Analysis**.

### Data Preparation
This is the most laborious part. It includes exploring the *[taxis](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Taxis_Clean_Transform.ipynb)* and *[weather](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Weather_Clean_Transform.ipynb)* datasets to find anomalies, patterns, insights, test hypothesis, etc.  
Once both datasets are cleaned and transformed, I *[joined](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Prepare_For_Models.ipynb)* them together in a single **.csv** file (``Data_Cleaned_2019_To_Model.csv``) which is ready to be analysed and/or served as input for the regression models.  
This is how the data looks like after being processed:  

![taxis merged](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Data_Prepare_For_Models_Merged.PNG)

The *taxis* dataset was specially hard, as the file size was too heavy (8GB and 83 million lines) to be read with my computer's memory. I had to compress it (800MB), and load it in chunks of 10.000 lines, perform all the analysis and transformations and put the chunks back together in a single file.

### Data Analysis
Now is time to explore the data further by creating some self-explanatory graphs (check out the notebook [here](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Analysis_01.ipynb)).  
#### 1. Map pickups by zone
I plotted a choropleth map showing Manhattan taxi zones by number of pickups, highlighting the top ten in red. These zones should coincide with the predictions of the machine learning models.

![map](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Map.PNG)

#### 2. Linear chart pickups over time
I analysed pickups' evolution over different periods of time looking for patterns.  

**Pickups evolution over Months**  
- The number of pickups over the year is quite constant.  
- The only variation is a small decrease of pickups over the Summer months: July and August. This can mean that most taxis are taken by new yorkers (not tourists), and in this period new yorkers travel away from the city.

![evolution months](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_Months.PNG)


**Pickups evolution over Weeks**  
This graph shows better how the taxi demand drops drastically on the USA Federal holidays (2019):
- New Year's Day: 1st of January.
- Independence Day: 4th July.
- Labor Day: first Monday of September.
- Thanksgiving: 4th Thursday of November.

![evolution weeks](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_Weeks.PNG)

**Pickups evolution over a Single Week**  
This graph shows the average number of pickups per weekday. Monday and Sunday are a bit quieter than the other days, but not much.

![evolution single week](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_SingleWeek.PNG)

**Pickups evolution over a Day**  
This graph shows the average number of pickups over a day:
- 18:00 and 19:00 are the peak hours.
- 1:00 am to 6:00 am the quieter.

![evolution day](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_Evolution_Day.PNG)

#### 3. Scatter Plot Relation between Precipitation and Pickups
I created this set of plots to find a correlation between precipitation and pickups. My hypothesis was that there were more pickups in rainy days, because people that usually walk are more likely to get a taxi.  
Most of the days it does not rain, so I plotted only rainy days and removed outliers above 0.5 precipitation.  
Surprisingly to me, the scatter plot was very clear: **there is no correlation between ``precipitation`` and ``pickups``.**

![pickups vs prec 3](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_PrepVSPickups_3.PNG)

#### 4. Pickups in Rainy Day vs Not Rainy Days
I wanted to confirm that my hypothesis about rainy days was wrong, by comparing the average of pickups in rainy days vs not rainy days. The results were crystal clear, there is not relation at all between rain and pickups. The average shown below is nearly the same.

-|precipitation|pickups
-|-|-
0|0.0|127.548318
1|1.0|131.911881

#### 5. Pairwise Relationships
As the number of pickups is very stable over time, I analysed only one month (so that my computer can handle it).<br>
These are the relations found between the variables:

- **Pickups - iswweekend**. There are more pickups during the weekend.
- **Pickups - dayofweek**. There are more pickups on Saturday, Friday, Thursday, in this order. This variable is related to ``isweekend`` but it contains more granularity about pickups distribution so I will keep this variable and remove ``is weekend`` when training the models.
- **Pickups - hour**. There are more pickups between 23:00 and 3:00. This could be because there is not public transport.
- **Pickups - day**. There is a clear weekly pattern so this information is already given by ``dayofweek``. So I will not use ``day``.

![pairwise relations](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Analysis_pairwise_relations_marked.PNG)

## 4_2_Modeling
These are the steps I followed:
(check out the notebook [here](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Modelling_01.ipynb))
### 4_2_1_Create some helper functions that will help me out in the process
* [``split_data()``](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#split_data): splits the data into train, validation and test.
* [``plot_real_vs_pred()``](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#plot_real_vs_pred): it creates a bar plot to visually compare real vs predicted values.
* [``get_metrics()``](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#get_metrics): it calculates relevant metrics all at once.
* [``compare_model_metrics()``](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#compare_model_metrics): bar plot to compare metrics from different models and choose the best one.

### 4_2_2_Import the data and select the following features:
Import the file ``Data_Cleaned_2019_To_Model.csv`` generated in the previous part and select the following features:
*Input* variables:
- ``month``
- ``hour``
- ``week``
- ``dayofweek``
- ``isholiday``
- ``LocationID``
- ``precipitation``

*Output* variable:
- ``pickups``

### 4_2_3_Split the data into Train, Validation and Test
Using my custom function ``split_data()`` which implements ``sklearn.model_selection.train_test_split``.

### 4_2_4_Create a [baseline model](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#Baseline-model)
By calculating the average of pickups per zone and per hour. I will use this model to compare with the regression models.

### 4_2_5_Train several regression models
using ``scikit-learn``.
  * [Linear Regression](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#Linear-Regression)
  * [K Nearest Neighbour Regressor](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#K-Nearest-Neighbour-Regressor)
  * [Decision Tree Regresor](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#Decision-Tree-Regressor)
  * [K Nearest Neighbour Regressor (using ``GridSearchCV``)](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#K-Nearest-Neighbour-Regressor_GridSearchCV)
  * [Decision Tree Regressor (using ``GridSearchCV``)](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#Decision-Tree-Regressor_GridSearchCV)
  * [Bagging Regressor (with ``KNeighboursRegressor``)](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#K-Nearest-Neighbour-Regressor_Bagging)
  * [Random Forest Regressor](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#Random-Forest-Regressor)
  * [Random Forest Regressor (using ``GridSearchCV``)](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#Random-Forest-Regressor_GridSearchCV)
  * [Gradient Boosting Regressor](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_3_Modelling#Gradient-Boosting-Regressor)

### 4_2_6_Compare metrics
I plotted a couple of graphs along the process to help me tune the models.  
A scatter plot of **'Actual vs Predicted'** values gives me a quick overview of how predictions are performing:
![DT Grid1](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Modelling_DT_Grid1.PNG)

A bar plot it is very useful to compare metrics between models:
![GradientBoosting](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Modelling_GradientBoosting.png)

Finally, I chose **Gradient Boosting** as it had the best metrics:
- ``RMSE``: 10%
- ``R2`` = 0.8%
- ``R`` = 0.4% <br>

And ``MAE`` is only 1% worse than *Random Forest_RandomizedSearchCV*.  
So in average **I think Gradient Boosting was the best model**  

### 4_2_7_Check if there is overfitting
To check if there is overfitting I do the following:
#### Compare *Test Predictions* with *Validation Predictions*
If I plot *Actual vs Predicted* values, *Test* Predictions should be similiar or a bit worse than *Validation* Predictions.  
In this case Test Predictions are actually a bit better but not enough to be worried.
![overfitting 1](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Modelling_Overfitting1.PNG)

#### Compare metrics: should be similiar
In coherence with the point above, the metrics are also very similar.
![overfitting 2](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Modelling_Overfitting2.PNG)


#### Plot Fitted Values vs Residuals: Mean should be zero.
Finally, I am plotting Fitted Values vs Residuals for both validation and test datasets.  
Residuals should be randomly scattered around zero. That means that the model´s predictions are correct and the independent variables are explaining everything they can.

In my model everything looks good:
- The mean is almost zero.
- The points are randomly scattered around zero.

Conclusion: **There is no overfitting**.

![overfitting 3](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Modelling_Overfitting3.PNG)

### 4_2_8_Pack model with Pickle
Finally I pack de model with ``pickle`` so I can use it in the front end.

## 4_3_Front-End
*(check out the full front-end [code](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Streamlit.ipynb) and the [wiki](https://github.com/angelrps/MasterDataScience_FinalProject/wiki/3_4_4_Streamlit-app))*  

The front-end is a web application that a taxi driver could potentially run every day to plan his journey. It performs the following three actions:

### Generate Model Inputs
It the one hand, it generates datetime info based on the current date and shapes the data appropriately including ``LocationID`` of Manhattan's zones. On the ohter hand, it scrapes in real time the precipitation weather forecast from www.wunderground.com and attach the data to the previous one.

### Generate Predictions
It unpacks the pickle model and make predictions using the input data generated above.

### Visualize Results
It takes the predictions and shapes the data so that it can be shown interactively in a **choropleth map** and a **multiple line chart**. Charts are made with **Bokeh** and **Altair**, and the web application is made with **Streamlit**.  

# 5_What do you need to run the project?
## 5_1_Dependencies and modules
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


## 5_2_Execution Guide
### If you want to run the app
Follow these steps:  
*Note:  There are multiple environments on which you can execute the app and I am not capable to cover them all. So these steps refer to my personal environment: Ubuntu running on WSL (Windows Subsystem for Linux).*<br>

1. Clone or download the [repository](https://github.com/angelrps/MasterDataScience_FinalProject).
2. Launch Ubuntu and navigate to ``\MasterDataScience_FinalProject\notebooks``.
3. Type ``streamlit run streamlit_app.py`` in the command line.
4. Copy the returned Network URL ``http://192.168.1.106:8501 `` and paste in your internet browser.
5. That´s it! The app takes a couple of seconds to load. This is mainly due to the real time web-scraping. 

### If you want to replicate the project
Execute the notebooks in the following order:  

**1. [Taxis Dataset](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Taxis_Clean_Transform.ipynb)**:
Explore, clean and transforms taxis data set into structures needed for the analysis.  

**2. [Weather Dataset](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Weather_Clean_Transform.ipynb)**:
Explore, clean and transforms weather data set into structures needed for the analysis.  

**3. [Merge Taxis and Weather Data](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Prepare_For_Models.ipynb)**:
It merges taxis and precipitation data into a single dataset, cleaned and ready for analysis and modeling.

**4. [Data Analysis](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Data_Analysis_01.ipynb)**:
It does not produce any output needed to execute the app but it contains the analysis in case that you want to execute it yourself.

**5. [Modeling](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Modelling_01.ipynb)**:
Explores different regression models and produces a pickle file with the selected model. You can also take the [pickle file from here](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/model_regGB.pickle)

**6. [Front-End](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/Streamlit.ipynb)**:
This notebook outputs the python (``.py``) script that will create the web application.

**7. [Run the app](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/notebooks/streamlit_app.py)**:
Finally, you can use this notebook to run the app.

For more clarity, this diagram illustrates how the different datasets, notebooks and their outputs are related.
![methodology_diagram](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Methodology_Diagram.png)


## 5_3_User Manual
* Use the controls on the side bar to select:
   * Graph type: map or line chart.
   * Day.
   * Time frame.
* The map will colour up according to the number of pickups (hover over the mouse to look at the exact numbers).
* The line chart will show pickups evolution over a whole day for each zone. Highlight a zone by selecting in the chart or in the legend.

**Click in the image to see it in action!**  
[![see it in action](https://github.com/angelrps/MasterDataScience_FinalProject/blob/master/img/Miniatura2.png)](https://youtu.be/xO07tr9dJ5o)



# 6_Conclusions
- The project addresses a problem that is relevant nowadays, and the final result (a machine learning app) **serves the purpose** it was developed for.

- It is **easy to use**. A taxi driver could easily install the dependencies on his computer and run it in a couple of seconds to look at the most demanding areas and plan his journey for the next 3 days.

- It gives **reliable predictions**.

- The data used in this project is easy to find, comes from a reliable source and it is kept up-to-date. Meaning that **this project could indeed be put in production and be maintained over the years**.

- **Searching for the right dataset** can be very time consuming. Sometimes the data is not available or it does not exist. When I defined my project idea I thought: "it is quite simple, there must be some free taxis dataset of Madrid". I was wrong, after weeks of unsuccessfull search I decided to move on and work with the New York dataset, which is of great quality, but it is not what I wanted.

- Study, clean and transform the data takes most of your time and efforts. And when you think you are done with it, some strange results in the analysis or model predictions warns you that something is wrong with the data, and you have to step back to find out.

- **Study, clean and transform the data is indeed one of the pilars of any machine learning project**. If your data is of a good quality, cleaned and shaped correctly, the models will return good predictions.

- It seems like there is a big gap between the product creation and the product use. There are lots of tools for data scientist to analyse data, clean, transform, train models, visualize data, etc. But once all that work is done, we need to put into production, create a product that someone unskilled in the field can use, for example, a web application. Streamlit seems to be the best option, and yet it is in very early stages. For this reason I encountered a significant number of bugs in streamlit while trying to integrate an altair choropleth map. This made me realise of how young is still the Data Science field and some of its tools.


## Want to know more about this app? Check out the [wiki](https://github.com/angelrps/MasterDataScience_FinalProject/wiki)
