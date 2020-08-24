
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
pd.options.display.max_columns = None
pd.options.display.max_rows = None

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt

from bokeh.io import output_notebook, output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool, Select, ColumnDataSource, WheelZoomTool, LogColorMapper, LinearColorMapper, ColorBar, BasicTicker
from bokeh.palettes import Viridis256 as palette
from bokeh.layouts import row


#############################   DEFINE FUNCTIONS START   #############################

# GET LOCATION ID DATA FRAME
# when deploying to external server, consider create LocationIDs manually instead of reading csv
@st.cache
def get_LocationIDs():
    # 1. Import Location and Borough columns form NY TAXI ZONES dataset
    dfzones = pd.read_csv('../data/NY_taxi_zones.csv', sep=',',
                          usecols=['LocationID', 'borough'])

    # 2. Filter Manhattan zones
    dfzones = dfzones[dfzones['borough']=='Manhattan']\
                    .drop(['borough'], axis=1)\
                    .sort_values(by='LocationID')\
                    .drop_duplicates('LocationID').reset_index(drop=True)    
    return dfzones

# CREATE DATETIME INFO AND APPEND LOCATION IDs
@st.cache
def datetimeInfo_and_LocID(df_LocIds, start_date, NoOfDays):   

    from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
    
    # repeat LocationIDs. All of them... for each hour
    location_id_col = pd.concat([df_LocIds]*24*NoOfDays).reset_index(drop=True)

    # create data frame with range of days with hourly period
    df_pred = pd.DataFrame()
    dates = pd.date_range(start = start_date, end = start_date + timedelta(days=NoOfDays), freq = "H")
    df_pred['datetime'] = dates
    df_pred.drop([df_pred.shape[0]-1], inplace=True)

    # Create new columns from datetime
    df_pred['month'] = df_pred['datetime'].dt.month
    df_pred['hour'] = df_pred['datetime'].dt.hour
    # 'dayhour' will serve as index to perform the join
    df_pred['dayhour'] = df_pred['datetime'].dt.strftime('%d%H')
    df_pred['week'] = df_pred['datetime'].dt.week
    df_pred['dayofweek'] = df_pred['datetime'].dt.dayofweek


    # Create date time index calendar
    drange = pd.date_range(start=str(start_date.year)+'-01-01', end=str(start_date.year)+'-12-31')
    cal = calendar()
    holidays = cal.holidays(start=drange.min(), end=drange.max())
    
    # 8.3 create new columns 'date' and 'isholiday'
    df_pred['date'] = pd.to_datetime(df_pred['datetime'].dt.date)
    df_pred['isholiday'] = df_pred['datetime'].isin(holidays).astype(int)
    
    # drop 'date' and 'datetime' column
    df_pred.drop(['datetime'], axis=1, inplace=True)
    df_pred.drop(['date'], axis=1, inplace=True)

    # repeat rows. 67 rows per hour
    df_pred = df_pred.iloc[np.arange(len(df_pred)).repeat(len(df_LocIds))].reset_index(drop=True)
    #df_index = df_index.iloc[np.arange(len(df_index)).repeat(67)].reset_index(drop=True)

    df_pred = df_pred.join(location_id_col)
    
    return df_pred

# SCRAPE PRECIPITATION FORECAST FROM wunderground.com
@st.cache
def scrape_data(today, days_in):
    # Use .format(YYYY, M, D)
    lookup_URL = 'https://www.wunderground.com/hourly/us/ny/new-york-city/date/{}-{}-{}.html'

    options = webdriver.ChromeOptions();
    options.add_argument('headless'); # to run chrome in the backbroung

    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)

    start_date = today + pd.Timedelta(days=1)
    end_date = today + pd.Timedelta(days=days_in + 1)

    df_prep = pd.DataFrame()

    while start_date != end_date:
        timestamp = pd.Timestamp(str(start_date)+' 00:00:00')
        
        print('gathering data from: ', start_date)
        
        formatted_lookup_URL = lookup_URL.format(start_date.year,
                                                 start_date.month,
                                                 start_date.day)

        driver.get(formatted_lookup_URL)
        rows = WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="mat-cell cdk-cell cdk-column-liquidPrecipitation mat-column-liquidPrecipitation ng-star-inserted"]')))
        for row in rows:
            hour = timestamp.strftime('%H')
            day = timestamp.strftime('%d')
            prep = row.find_element_by_xpath('.//span[@class="wu-value wu-value-to"]').text
            # append new row to table
            # 'dayhour' column will serve as column index to perform the Join
            df_prep = df_prep.append(pd.DataFrame({"dayhour":[day+hour], 'precipitation':[prep]}),
                                     ignore_index = True)
            
            timestamp += pd.Timedelta('1 hour')

        start_date += timedelta(days=1)
    return df_prep

# GET INPUT DATA USING THE FUNCTIONS ABOVE: LocationIDs and Datetime info
@st.cache
def get_input_data(start_date, NoOfDays):
    # get LocationIDs data frame
    df_LocIds = get_LocationIDs()

    # create datetime info and append LocationsIDs
    dtInfo_and_LocID = datetimeInfo_and_LocID(df_LocIds,start_date,NoOfDays)

    # get precipitation forecast
    prep_forecast = scrape_data(date.today(), NoOfDays)

    # merge both data frames
    df_merged = dtInfo_and_LocID.merge(prep_forecast, on="dayhour", how="left")

    # drop dayhour column
    df_merged = df_merged.drop(['dayhour'], axis=1)
    
    return df_merged

# GET OUPPUT DATA: get predictions, append to input_data and format it to be processed
@st.cache
def get_output_data(pickle_file, input_data):
    import pickle

    model = pickle.load(open(pickle_file,'rb'))

    # get prediction, convert to integer and convert Array into DataFrame
    model_predict = (model.predict(input_data)).astype(int)
    df_predict = pd.DataFrame({'pickups':model_predict})

    # join input_data with DataFrame
    joined = input_data.join(df_predict)
    
    output_data = joined[['hour','dayofweek','LocationID','pickups']]
    
    return output_data

# GET DATA FRAME WITH SHAPE GEOMETRY INFO
@st.cache
def load_shape_data():
    shape_data = gpd.read_file('../data/taxi_zones/taxi_zones.shp')

    # filter Manhattan zones
    shape_data = shape_data[shape_data['borough'] == 'Manhattan'].reset_index(drop=True)

    shape_data = shape_data.drop(['borough'], axis=1)

    #EPSG-Code of Web Mercador
    shape_data.to_crs(epsg=3785, inplace=True)

    # Simplify Shape of Zones (otherwise slow peformance of plot)
    shape_data["geometry"] = shape_data["geometry"].simplify(100)

    data = []
    for zonename, LocationID, shape in shape_data[["zone", "LocationID", "geometry"]].values:
        #If shape is polygon, extract X and Y coordinates of boundary line:
        if isinstance(shape, Polygon):
            X, Y = shape.boundary.xy
            X = [int(x) for x in X]
            Y = [int(y) for y in Y]
            data.append([LocationID, zonename, X, Y])

        #If shape is Multipolygon, extract X and Y coordinates of each sub-Polygon:
        if isinstance(shape, MultiPolygon):
            for poly in shape:
                X, Y = poly.boundary.xy
                X = [int(x) for x in X]
                Y = [int(y) for y in Y]
                data.append([LocationID, zonename, X, Y])

    #Create new DataFrame with X an Y coordinates separated:
    shape_data = pd.DataFrame(data, columns=["LocationID", "ZoneName", "X", "Y"])
    return shape_data

@st.cache(allow_output_mutation=True)
def load_taxis_data(output_data, shape_data):
    df_to_visualize = shape_data.copy()
    pickups = output_data.groupby(['hour','dayofweek','LocationID']).sum()
    start_day = pd.unique(output_data['dayofweek']).min()
    end_day = pd.unique(output_data['dayofweek']).max()

    for hour in range(24):
        for dayofweek in range(start_day,end_day+1,1):
            # get pickups for this hour and weekday
            p = pd.DataFrame(pickups.loc[(hour, dayofweek)]).reset_index()
        
            # add pickups to the Taxi Zones DataFrame       
            df_to_visualize = pd.merge(df_to_visualize, p, on="LocationID", how="left").fillna(0)
            # rename column as per day and hour
            df_to_visualize.rename(columns={"pickups" : "Passenger_%d_%d"%(dayofweek, hour)}, inplace=True)

    return df_to_visualize


#############################   DEFINE FUNCTIONS END   #############################

# DECLARE VARIABLES: start date, NoOfDays, pickle_file
start_date = date.today() + timedelta(days=1) # start day is tomorrow
NoOfDays = 3 # number of days for prediction
pickle_file = './model_regGB.pickle'

# RUN FUNCTIONS
input_data = get_input_data(start_date, NoOfDays)

output_data = get_output_data(pickle_file, input_data)

shape_data = load_shape_data()

df_to_visualize = load_taxis_data(output_data,shape_data)

# INITIAL SET PAGE CONFIG
page_title = 'Taxi Demand Predictor'
layout='wide'
initial_sidebar_state = 'expanded'

# SHOW TITLE AND DESCRIPTION
st.title("Manhattan Taxi Demand Predictor")
"""
Hi! With this Machine Learning app you can get your taxi demand prediction in Manhattan for the next 3 days!

Just choose day and hour from the side bar and hover the mouse over the map.

It will tell you how many passenger are expected in that time frame.
"""

# SIDE BAR
st.sidebar.text('Choose DAY and TIME')
# add slider widget: Hours
hour = st.sidebar.slider("Hour",min_value=0, max_value=23, value=7, step=1)


# add buttons widget: Dayofweek
button1_day = date.today() + pd.Timedelta(days=1)
button2_day = date.today() + pd.Timedelta(days=2)
button3_day = date.today() + pd.Timedelta(days=3)
    
button1 = st.sidebar.button(str(button1_day) + " ("+button1_day.strftime("%A") + ")")
button2 = st.sidebar.button(str(button2_day) + " ("+button2_day.strftime("%A") + ")")
button3 = st.sidebar.button(str(button3_day) + " ("+button3_day.strftime("%A") + ")")
weekday = button1_day.weekday()
if button1:
    weekday = button1_day.weekday()
if button2:
    weekday = button2_day.weekday()
if button3:
    weekday = button3_day.weekday()
    

# ColumnDataSource transforms the data into something that Bokeh and Java understand
df_to_visualize["Passengers"] = df_to_visualize["Passenger_" + str(weekday) + "_" + str(hour)]

source = ColumnDataSource(df_to_visualize)

max_passengers_per_hour = df_to_visualize[filter(lambda x: "Passenger_" in x, df_to_visualize.columns)].max().max()

color_mapper = LinearColorMapper(palette=palette[::-1], high=max_passengers_per_hour, low=0)


##### Color Bar
color_bar = ColorBar(color_mapper = color_mapper,
                     ticker = BasicTicker(),
                    label_standoff=8,
                     location=(0,0),
                     orientation='vertical')

p = figure(title="New York Taxi Pickups",
           plot_width=450, plot_height=750,
           toolbar_location=None,
           tools='pan,wheel_zoom,box_zoom,reset,save')
p.xaxis.visible = False
p.yaxis.visible = False

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Get rid of zoom on axes:
for t in p.tools:
    if type(t) == WheelZoomTool:
        t.zoom_on_axis = False

patches = p.patches(xs="X", ys="Y", source=source,fill_alpha=1,
                  fill_color={'field': 'Passengers',
                              'transform': color_mapper},
                  line_color="black", alpha=0.5)

hovertool = HoverTool(tooltips=[('Zone:', "@ZoneName"),
                                ("Passengers:", "@Passengers")])
p.add_tools(hovertool)

p.add_layout(color_bar, 'right')

st.bokeh_chart(p)

'''
**Ideas to improve**:

- Show day, hour and zone for máximum and minimum value.
- Show line chart with pickup evolution throughout the day, and make it interactive, highlighting the zone selected in the map

'''
