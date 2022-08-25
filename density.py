import numpy as np
import pandas as pd

##LOADING DATA
dataset = pd.read_csv(r"M_cat1.csv")
dataset = dataset[dataset["Mw"] >= 4.5]
dataset = dataset[dataset["Lon"] <= 64]

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
    Area = (max_lat-min_lat)/50*111 #it just shows a cell size
    print(f"Area: {Area}")
    
    for i in range(len(lat_increments)-1):
        for j in range(len(lon_increments)-1):
            cell = dataset[dataset.Lat < lat_increments[i+1]]
            cell = cell[cell.Lat >= lat_increments[i]]
            cell = cell[cell.Lon < lon_increments[j+1]]
            cell = cell[cell.Lon >= lon_increments[j]]
            
            Density = 0.25*len(cell)
            if Density <= 10:
                Density += 10
            cell["Density"] = Density
            
            dataset_new = pd.concat([dataset_new,cell])
    
    return dataset_new

new_dataset = density_map(dataset,30)


new_dataset.to_csv(r"M_cat2.csv")