
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

file_name, cell_number = sys.argv
cell_number = int(cell_number)


#LOADING DATA
dataset = pd.read_csv(r"canada_eq.csv")
#filters
#dataset = dataset[dataset.Year >= 1900]
#dataset = dataset[dataset.Mag > 1]
#dataset = dataset[dataset.Lon <= 64]
#dataset = dataset[dataset.Lon >= 43.5]
#dataset = dataset[dataset.Lat <= 41]

def density_map(dataset, number_of_increments_in_a_row):
    #this function needs a DataFrame file (preferebaly imported as csv or excel)
    #which has columns by the exact names of "Lat"and "Lon". The result of the function 
    #is a new DataFrame with the exact form but a column named "Density" is added. 
    #
    #        number_of_increments_in_a_row sets the resolution.
    #
    dataset["Density"] = ''
    dataset_new = []
    dataset_new = pd.DataFrame(dataset_new)

    data_length = len(dataset['Lon'])

    min_lat = np.min(dataset['Lat'])*0.999
    max_lat = np.max(dataset['Lat'])*1.001
    min_lon = np.min(dataset['Lon'])*0.999
    max_lon = np.max(dataset['Lon'])*1.001

    lat_increments = np.linspace(min_lat, max_lat, number_of_increments_in_a_row+1)
    lon_increments = np.linspace(min_lon, max_lon, number_of_increments_in_a_row+1)
    length = np.diff(lon_increments).mean()*np.diff(lat_increments).mean()
    print("Proposed Radius:", length)
    for i in range(len(lat_increments)-1):
        for j in range(len(lon_increments)-1):
            cell = dataset[dataset.Lat < lat_increments[i+1]]
            cell = cell[cell.Lat >= lat_increments[i]]
            cell = cell[cell.Lon < lon_increments[j+1]]
            cell = cell[cell.Lon >= lon_increments[j]]
            
            Density = 1*len(cell)
            if Density <= 10:
                Density = 10
            cell["Density"] = Density
            
            dataset_new = pd.concat([dataset_new,cell])
    #dataset_new.Density *= 0.5
    
    return dataset_new

cell_number = 30
density_applied_dataset = density_map(dataset,cell_number)

fig = px.scatter_geo(density_applied_dataset, lon='Lon',lat='Lat',  color="Density", scope="asia" )
fig.show()
density_applied_dataset.to_csv(r"den_cat.csv")