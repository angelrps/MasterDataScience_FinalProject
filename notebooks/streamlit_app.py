
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt
import random

st.title("Taxi Demand Predict")
"""
Write some description here
"""

@st.cache
def load_shape_data():
    df_taxizones = gpd.read_file('../data/taxi_zones/taxi_zones.shp')

    # filter Manhattan zones
    df_taxizones = df_taxizones[df_taxizones['borough'] == 'Manhattan'].reset_index(drop=True)

    df_taxizones = df_taxizones.drop(['borough'], axis=1)

    df_taxizones.to_crs(epsg=3785, inplace=True)

    #EPSG-Code of Web Mercador

    # Simplify Shape of Zones (otherwise slow peformance of plot)
    df_taxizones["geometry"] = df_taxizones["geometry"].simplify(100)

    data = []
    for zonename, LocationID, shape in df_taxizones[["zone", "LocationID", "geometry"]].values:
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
    df_taxizones = pd.DataFrame(data, columns=["LocationID", "ZoneName", "X", "Y"])
    return df_taxizones

df_taxizones1 = load_shape_data()

@st.cache(allow_output_mutation=True)
def load_taxis_data(df_taxizones1):
    # 'df_taxis' should be a data frame returned by the ML model
    df_taxis = pd.read_csv('../data/Data_Taxis_2017_Cleaned.csv', sep=',',
                          usecols=['hour','dayofweek','LocationID','NoOfPickups'])

    pickups = df_taxis.groupby(['hour','dayofweek','LocationID']).sum()

    for hour in range(24):    
        for dayofweek in range(7):

            #Get pickups and dropoff for this hour and weekday:
            p = pd.DataFrame(pickups.loc[(hour, dayofweek)]).reset_index().rename(columns={"LocationID" : "LocationID"})

            #Add information of pickups and dropoff to the New York Taxi Zone DataFrame:
            df_taxizones1 = pd.merge(df_taxizones1, p, on="LocationID", how="left").fillna(0)
            df_taxizones1.rename(columns={"NoOfPickups" : "Passenger_%d_%d"%(dayofweek, hour)}, inplace=True) 
    return df_taxizones1

df_taxizones2 = load_taxis_data(df_taxizones1)

from bokeh.io import output_notebook, output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool, Select, ColumnDataSource, WheelZoomTool, LogColorMapper, LinearColorMapper, ColorBar, BasicTicker
from bokeh.palettes import Viridis256 as palette
from bokeh.layouts import row

# add slider widget: Hours
hour = st.slider("Hour",min_value=0, max_value=23, value=7, step=1)

# add slider widget: Dayofweek
weekday = st.slider("Day of week",min_value=0, max_value=6, value=1, step=1)

# ColumnDataSource transforms the data into something that Bokeh and Java understand
df_taxizones2["Passengers"] = df_taxizones2["Passenger_" + str(weekday) + "_" + str(hour)]

source = ColumnDataSource(df_taxizones2)

max_passengers_per_hour = df_taxizones2[filter(lambda x: "Passenger_" in x, df_taxizones2.columns)].max().max()

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

patches = p.patches(xs="X", ys="Y", source=source,
                  fill_color={'field': 'Passengers',
                              'transform': color_mapper},
                  line_color="black", alpha=0.5)

hovertool = HoverTool(tooltips=[('Zone:', "@ZoneName"),
                                ("Passengers:", "@Passengers")])
p.add_tools(hovertool)

p.add_layout(color_bar, 'right')

st.bokeh_chart(p)
max_value = df_taxizones2.drop(['LocationID','ZoneName','X', 'Y'], axis=1).max().sort_values()

st.write(max_value)
"""
End of script
"""
