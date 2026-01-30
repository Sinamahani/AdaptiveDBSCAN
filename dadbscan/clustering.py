import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
# from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
import geopandas as gpd

# _, density_file_name, radius = sys.argv
# radius = float(radius)

class dbscan:
    def __init__(self, radius, density_file_name):
        self.radius = radius
        self.density_file_name = density_file_name
        self.dataset = pd.read_csv(self.density_file_name)
        self.dataset["Label"] = -100
        self.dataset["Label"] = self.dataset["Label"].astype("int16")
    

    def ExpandCluster(self, PointNeighbor, seeds):
        for neighbor in PointNeighbor:
            if (self.dataset["Label"][neighbor] == -100 or self.dataset["Label"][neighbor] == 0) and neighbor not in seeds:
                seeds.append(neighbor)

    def clustering (self):
        eps = self.radius
        m = self.dataset.shape[0]
        DistanceMatrix = distance_matrix(self.dataset[["Lon","Lat"]], self.dataset[["Lon","Lat"]])
        C = 0                   #Cluster Counter
        Min_Points = (self.dataset["Density"])
        print(f"Dataset with {m} points loaded. Starting Clustering with eps={eps} ...")
        for i in range(m):
            if self.dataset.Label[i] == -100:
                seeds = []    
                PointNeighbor = np.where(DistanceMatrix[i] <= eps)[0]
                if len(PointNeighbor) >= Min_Points[i]+1:
                    C = C+1
                    # 
                    seeds.append(i)
                    while len(seeds) != 0:
                        PointNeighbor = np.where(DistanceMatrix[seeds[0]]<=eps)[0]
                        self.dataset.loc[seeds[0],("Label")] = C
                        self.ExpandCluster(PointNeighbor, seeds)
                        seeds = seeds[1:]
                else:
                    self.dataset.loc[i,("Label")] = 0
            # print(f"{seeds}")       
            # print(f"Progress: {i+1}/{m} points clustered.", end="\r")
        return self.dataset
    
    
    def plot_clusters(self, **kwargs):
        """Plot the clusters on a map using geopandas and matplotlib
        ----------
        **kwargs:
        cmap_shp: str, default="grey"
            The colormap to use for the shape file in the background
        cmap_scatter: str, default="turbo"
            The colormap to use for the scatter plot
        shp_linewidth: float, default=2
            The linewidth of the shape file
        save_fig: bool, default=False
            Whether to save the figure or not, if so, it will be saved in the ExampleData folder
        save_fig_format: str, default="pdf"
            The format to save the figure in 
        shape_file_address: str, default=False
            The address of the shape file to plot in the background, you can use the World_Countries_Generalized.shp file in the ShapeFiles folder.
            shape_file_address="ShapeFiles/World_Countries_Generalized.shp"
           
        """
        cmap_shp = kwargs.get("cmap", "grey")
        cmap_scatter = kwargs.get("cmap", "turbo")
        shp_linewidth = kwargs.get("shp_linewidth", 2)
        save_fig = kwargs.get("save_fig", False)
        save_fig_format = kwargs.get("save_fig_format", "pdf")
        shape_file_address = kwargs.get("shape_file_address", False)


        x, y, c = self.dataset["Lon"][self.dataset.Label>0], self.dataset["Lat"][self.dataset.Label>0], self.dataset["Label"][self.dataset.Label>0]
        x_noise, y_noise, c_noise = self.dataset["Lon"][self.dataset.Label==0], self.dataset["Lat"][self.dataset.Label==0], self.dataset["Label"][self.dataset.Label==0]
        fig1, ax1 = plt.subplots(figsize=(7,8), dpi=600)
        min_lon, max_lon = self.dataset["Lon"].min(), self.dataset["Lon"].max()
        min_lat, max_lat = self.dataset["Lat"].min(), self.dataset["Lat"].max()

        #ploting background
        if shape_file_address:
            shape_file = gpd.read_file(shape_file_address)
            shape_file.plot(ax=ax1, color="black", linewidth=shp_linewidth, cmap=cmap_shp, alpha=0.3)
            plt.xlim(min_lon, max_lon)
            plt.ylim(min_lat, max_lat)

        #ploting clusters
        ax1.scatter(x_noise, y_noise, c="k",s=1, alpha=0.25)
        ax1.scatter(x, y, c=c, cmap=cmap_scatter,linewidths=0.05 ,edgecolor='k',s=10)

        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_title(f"DBSCAN Clustering with eps={self.radius}")
        
        if save_fig:
            fig1.savefig(f"Results/IMG_{self.radius}__model_{' '}_{self.density_file_name.split('.')[0].split('/')[0]}.{save_fig_format}", format=save_fig_format)
        plt.show()


