
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


# _ , file_name, cell_number = sys.argv #this line is for running the code in the terminal
# cell_number = int(cell_number)

class EQ_Density:
    def __init__(self, file_name, cell_number, min_year=1900, max_year=2050, min_mag=1, max_mag=9,  min_lat=20, max_lat=41, min_lon=43.5, max_lon=64):
        self.file_name = file_name
        self.cell_number = cell_number
        self.dataset = pd.read_csv(file_name)
        #filtering dataset
        self.dataset = self.dataset[self.dataset.Year >= min_year]
        self.dataset = self.dataset[self.dataset.Year <= max_year]
        self.dataset = self.dataset[self.dataset.Mw <= max_mag]
        self.dataset = self.dataset[self.dataset.Mw >= min_mag]
        self.dataset = self.dataset[self.dataset.Lat >= min_lat]
        self.dataset = self.dataset[self.dataset.Lat <= max_lat]
        self.dataset = self.dataset[self.dataset.Lon <= max_lon]
        self.dataset = self.dataset[self.dataset.Lon >= min_lon]

        #adding density column
        self.dataset["Density"] = ''
        self.dataset["Cell#"] = ''
        

    def calc_density(self, minimum_density=10, save_file_name = r"den_catal.csv"):
        """
        This function needs a DataFrame file (preferebaly imported as csv or excel) to calculate the density of earthquakes in each cell.
        """
        #creating new dataset
        self.dataset_new = []
        self.save_file_name = save_file_name
        self.dataset_new = pd.DataFrame(self.dataset_new)
        self.data_length = len(self.dataset['Lon'])
        self.min_lat = np.min(self.dataset['Lat'])*0.999
        self.max_lat = np.max(self.dataset['Lat'])*1.001
        self.min_lon = np.min(self.dataset['Lon'])*0.999
        self.max_lon = np.max(self.dataset['Lon'])*1.001
        self.lat_increments = np.linspace(self.min_lat, self.max_lat, self.cell_number+1)
        self.lon_increments = np.linspace(self.min_lon, self.max_lon, self.cell_number+1)
        self.radius = round(np.diff(self.lon_increments).mean()*np.diff(self.lat_increments).mean(),3)
        print("Proposed Radius:", self.radius)

        self.heat_matrix = np.zeros((len(self.lat_increments)-1, len(self.lat_increments)-1))
        # print("Calculating density...")

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
        self.dataset_new.to_csv(self.save_file_name)
        print("Done!\nFile saved as:", self.save_file_name)
        print("Density Matrix Shape:\n", self.heat_matrix.shape)
        return self.heat_matrix
    
    def plot_den(self):
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
        try:
            fig.savefig(f"results/den_cat_{self.cell_number}.png")
        except:
            raise FileNotFoundError("Make sure you have a folder named 'results' in your directory. If not, create one.")
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
            fig.savefig(f"results/den_cat_{self.cell_number}_smooth.png")
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
                cell["Density"] = int(smooth_val)
                n += 1
                self.dataset_smooth = pd.concat([self.dataset_smooth, cell])
        self.dataset_smooth.to_csv(f"den_cat_{self.cell_number}_smooth.csv")
        print(f"Done!\nFile saved as: den_cat_{self.cell_number}_smooth.csv")
        return self.dataset_smooth

                
