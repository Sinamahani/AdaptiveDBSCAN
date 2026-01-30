
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


# _ , file_name, cell_number = sys.argv #this line is for running the code in the terminal
# cell_number = int(cell_number)

class EQ_Density:
    def __init__(self, cell_number, min_year=1900, max_year=2050, min_mag=1, max_mag=9, map_extension_value = 0.01, data_file=r"decl_cat.csv", filters={}):
        try:
            os.mkdir("Results")
        except:
            print("Results folder already exists.")
               
        self.data_file = data_file
        self.cell_number = cell_number
        self.dataset = pd.read_csv(f"{self.data_file}")
        
        #filtering with custom filters
        if not isinstance(filters, dict):
            raise TypeError("The filters should be in dictionary format")
        if filters != {}:
            if not all(k in filters.keys() for k in ("col", "op", "val")):
                raise KeyError("The filters dictionary must contain 'col', 'op', and 'val' keys.")
            if not (isinstance(filters["col"], list) and isinstance(filters["op"], list) and isinstance(filters["val"], list)):
                raise TypeError("The values for 'col', 'op', and 'val' in filters must be lists.")
            if not (len(filters["col"]) == len(filters["op"]) == len(filters["val"])):
                raise ValueError("The lists for 'col', 'op', and 'val' must have the same length.")
            
            op = filters["op"]
            col = filters["col"]
            val = filters["val"]
            for c, o, v in zip(col, op, val):
                if o == ">":
                    self.dataset = self.dataset[self.dataset[c] > v]
                elif o == ">=":
                    self.dataset = self.dataset[self.dataset[c] >= v]
                elif o == "<":
                    self.dataset = self.dataset[self.dataset[c] < v]
                elif o == "<=":
                    self.dataset = self.dataset[self.dataset[c] <= v]
                elif o == "==":
                    self.dataset = self.dataset[self.dataset[c] == v]
                elif o == "!=":
                    self.dataset = self.dataset[self.dataset[c] != v]
                else:
                    raise ValueError(f"Unsupported condition: {o}. Use one of the following: >, >=, <, <=, ==, !=")
        
        #filtering dataset
        if "Year" in self.dataset.columns:
            self.dataset = self.dataset[self.dataset.Year >= min_year]
            self.dataset = self.dataset[self.dataset.Year <= max_year]
        
        if "Mw" in self.dataset.columns:
            self.dataset = self.dataset[self.dataset.Mw <= max_mag]
            self.dataset = self.dataset[self.dataset.Mw >= min_mag]
        min_lat = np.min(self.dataset['Lat'])- map_extension_value 
        max_lat = np.max(self.dataset['Lat'])+ map_extension_value 
        min_lon = np.min(self.dataset['Lon'])- map_extension_value 
        max_lon = np.max(self.dataset['Lon'])+ map_extension_value 
        print(f"Dataset filtered between years {min_year} and {max_year}, Magnitudes {min_mag} and {max_mag}, Latitudes {min_lat} and {max_lat}, Longitudes {min_lon} and {max_lon}.")
        self.dataset = self.dataset[self.dataset.Lat >= min_lat]
        self.dataset = self.dataset[self.dataset.Lat <= max_lat]
        self.dataset = self.dataset[self.dataset.Lon <= max_lon]
        self.dataset = self.dataset[self.dataset.Lon >= min_lon]

        #adding density column
        self.dataset["Density"] = ''
        self.dataset["Cell#"] = ''
        

    def calc_density(self, minimum_density=10):
        """
        This function needs a DataFrame file (preferebaly imported as csv or excel) to calculate the density of earthquakes in each cell.
        """
        #creating new dataset
        self.dataset_new = []
        self.dataset_new = pd.DataFrame(self.dataset_new)
        self.data_length = self.dataset.shape[0]
        self.min_lat = np.min(self.dataset['Lat'])*0.999
        self.max_lat = np.max(self.dataset['Lat'])*1.001
        self.min_lon = np.min(self.dataset['Lon'])*0.999
        self.max_lon = np.max(self.dataset['Lon'])*1.001
        self.lat_increments = np.linspace(self.min_lat, self.max_lat, self.cell_number+1)
        self.lon_increments = np.linspace(self.min_lon, self.max_lon, self.cell_number+1)
        self.radius = round(np.diff(self.lon_increments).mean()*np.diff(self.lat_increments).mean(),3)
        print("Proposed Radius:", self.radius)
        self.heat_matrix = np.zeros((len(self.lat_increments)-1, len(self.lat_increments)-1))

        # start working on the dataset - Calculating density
        n = 0  #cell counter
        for i in range(len(self.lat_increments)-1):
            for j in range(len(self.lon_increments)-1):
                cell = self.dataset[self.dataset.Lat < self.lat_increments[i+1]]
                cell = cell[cell.Lat >= self.lat_increments[i]]
                cell = cell[cell.Lon < self.lon_increments[j+1]]
                cell = cell[cell.Lon >= self.lon_increments[j]]

                Density = 1*len(cell)
                if Density <= minimum_density:
                    Density = minimum_density
                cell["Density"] = int(Density)
                cell["Cell#"] = n
                n += 1
                self.heat_matrix[i, j] = int(Density)
                
                self.dataset_new = pd.concat([self.dataset_new,cell])
        if not os.path.exists("Results"):
            os.mkdir("Results")
        if "/" in self.data_file or "\\" in self.data_file:
            self.data_file = self.data_file.split("/")[-1].split("\\")[-1]
        self.dataset_new.to_csv(f"Results/den_{self.data_file.split('.')[0]}__{self.cell_number}.csv")
        print("Done!\nFile saved as:", f"Results/den_{self.data_file.split('.')[0]}__{self.cell_number}.csv")
        print("Density Matrix Shape:\n", self.heat_matrix.shape)
        return self.heat_matrix
    
    def plot_density(self):
        """
        This function plots the density map of earthquakes using the csv file provided.
        Information needed for plotting are "Lat", "Lon" and "Density" columns.
        """
        extent = self.min_lon, self.max_lon, self.min_lat, self.max_lat
        lat = np.round(np.linspace(self.max_lat, self.min_lat, 10),1)
        lon = np.round(np.linspace(self.min_lon, self.max_lon, 5), 1)
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(self.heat_matrix, cmap='viridis', interpolation='nearest', extent=extent, origin='lower')
        plt.colorbar(shrink=0.5)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.xticks(lon)
        plt.yticks(lat)
        plt.title(f"Earthquake Density Map\nCells: {self.cell_number} x {self.cell_number} | Radius: {self.radius}")
        plt.gca().set_aspect('equal', adjustable='box')  # Equal aspect ratio
        plt.tight_layout()
        try:
            fig.savefig(f"Results/IMG_{self.data_file.split('.')[0]}__{self.cell_number}.png")
        except:
            raise FileNotFoundError(f"Make sure you have a folder named '{self.data_folder}' in your directory. If not, create one.")
        plt.show()

    def cell_smoother(self, apply_smooth=True, plot_on = True):
        """
        This function applies a smoothing filter to the density matrix.
        """
        smooth_matrix = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        extent = self.min_lon, self.max_lon, self.min_lat, self.max_lat
        #convolution
        self.smooth_heat_matrix = convolve2d(self.heat_matrix, smooth_matrix, mode='same')/np.sum(smooth_matrix)
        print("Smooth Density Matrix Shape:\n", self.heat_matrix.shape)
        if plot_on:
            fig = plt.figure(figsize=(10, 10))
            plt.imshow(self.smooth_heat_matrix, cmap='viridis', interpolation='nearest', extent=extent, origin='lower')
            plt.colorbar(shrink=0.5)
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            lat = np.round(np.linspace(self.max_lat, self.min_lat, 10),1)
            lon = np.round(np.linspace(self.min_lon, self.max_lon, 5), 1)
            plt.xticks(lon)
            plt.yticks(lat)
            plt.title(f"Smoothed Earthquake Density Map\nCells: {self.cell_number} x {self.cell_number} | Radius: {self.radius}")
            plt.gca().set_aspect('equal', adjustable='box')  # Equal aspect ratio
            plt.tight_layout()
            fig.savefig(f"Results/IMG_{self.data_file.split('.')[0]}__{self.cell_number}_smooth.png")
            plt.show()
        if apply_smooth:
            self.apply_smooth_den()
        return self.smooth_heat_matrix
    
    def apply_smooth_den(self):
        n = 0
        self.dataset_smooth = pd.DataFrame()
        for i in range(self.smooth_heat_matrix.shape[0]):
            for j in range(self.smooth_heat_matrix.shape[1]):
                cell = self.dataset_new[self.dataset_new["Cell#"] == n]
                smooth_val = self.smooth_heat_matrix[i, j]
                cell.loc[:, "Density"] = int(smooth_val)
                n += 1
                self.dataset_smooth = pd.concat([self.dataset_smooth, cell])
        self.dataset_smooth.to_csv(f"Results/den_{self.data_file.split('.')[0]}__{self.cell_number}_smooth.csv")
        print(f"Done!\nFile saved as: den_{self.data_file.split('.')[0]}__{self.cell_number}_smooth.csv")
        return self.dataset_smooth

                
