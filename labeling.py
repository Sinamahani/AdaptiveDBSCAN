#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:57:59 2022

@author: sina

this code is created to label the catalogue based on the locatio of earthquakes.
it should be noted that shape files must be as seperate files!
"""
import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, box

seismotectonic_provinces = ['zagros','alborz','makran','kope-dagh','central']

def number_of_points_in_each_sp(cluster,seismotectonic_provinces): 
    #sp stands for seismotectonic province
    return 5
# zag = gpd.read_file('/Users/sina/Documents/Course/AD Seismology 2/DBSCAN/shape-files/kopeh-dagh.shp')

# dataset = pd.read_excel(r"data_isc.xlsx")
# geomet = gpd.points_from_xy(dataset.Lon, dataset.Lat)
# gdf = gpd.GeoDataFrame(dataset,geometry=geomet)
# sa_capitals = gpd.clip(gdf, zag)

# zag.plot()
# plt.scatter(sa_capitals["Lon"], sa_capitals["Lat"],c='red',marker=".")
# plt.show()

def dbscan_error(dataset):
    max_percentage =[]  
    """the error analysis algorithm is based on calculating the percentage of locating a cluster in a 
    seismotectonic province and use the maximum percentage. Finally, the average of all clusters can be
    considered as the accuracy of the model"""
    
    for cluster_counter in range(np.max(dataset["Label"])):
        cluster_counter += 1; #because it starts from zero but here zero shows our noise!
        cluster = dataset[dataset.Label == cluster_counter]
        all_events_in_cluster = len(cluster)
        
        print(all_events_in_cluster)
        
dbscan_error(dataset)