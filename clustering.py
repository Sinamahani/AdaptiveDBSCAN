import sys
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
# from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
import matplotlib
import geopandas as gpd

# _, density_file_name, radius = sys.argv
# radius = float(radius)

class dbscan:
    def __init__(self, radius, density_file_name):
        self.radius = radius
        self.density_file_name = density_file_name
        self.dataset = pd.read_csv(density_file_name)
        self.dataset["Label"] = ''

    def ExpandCluster(self, PointNeighbor, seeds):
        for neighbor in PointNeighbor:
            if (self.dataset["Label"][neighbor] == '' or self.dataset["Label"][neighbor] == 0) and neighbor not in seeds:
                seeds.append(neighbor)

    def clustering (self):
        eps = self.radius
        m = self.dataset.shape[0]
        DistanceMatrix = distance_matrix(self.dataset[["Lon","Lat"]], self.dataset[["Lon","Lat"]])
        C = 0                   #Cluster Counter
        Min_Points = (self.dataset["Density"])

        for i in range(m):
            if self.dataset.Label[i] == '':
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
        return self.dataset
    
    # def plot_cluster_names(self):
    #     """this function is written to plot clusters names in the map"""
    #     loc = self.cluster_center_location
    #     for ind in loc.index:
    #         plt.text(loc["Lon"][ind], loc["Lat"][ind], f"{loc['Label'][ind]}", size=12, color="white")
    
    # def cluster_center(self):
    #     self.cluster_center_location = self.dataset.groupby("Label").mean()
    #     return self.cluster_center_location
    
    def plot_clusters(self):
        x, y, c = self.dataset["Lon"][self.dataset.Label>0], self.dataset["Lat"][self.dataset.Label>0], self.dataset["Label"][self.dataset.Label>0]
        x_noise, y_noise, c_noise = self.dataset["Lon"][self.dataset.Label==0], self.dataset["Lat"][self.dataset.Label==0], self.dataset["Label"][self.dataset.Label==0]
        colors  = [f"C{i}" for i in np.arange(1, c.max()+1)]
        cmap, norm = matplotlib.colors.from_levels_and_colors(np.arange(1, c.max()+2), colors)
        fig1, ax1 = plt.subplots(figsize=(5,5))
        model = "tahernia"
        if model != "None":
            shape_file = gpd.read_file(f"shape-files/{model}.shp")
            shape_file.plot(ax=ax1, color="black", linewidth=2)
        scatter2 = ax1.scatter(x_noise, y_noise, c="k",s=1, alpha=0.25)
        scatter1 = ax1.scatter(x, y, c=c, cmap="turbo",linewidths=0.05,edgecolor='k',s=10)
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_title(f"DBSCAN Clustering with eps={self.radius}")
        #add topo map
        m = Basemap(projection='mill',llcrnrlat=24,urcrnrlat=40,\
                    llcrnrlon=44,urcrnrlon=64,resolution='c')
        # ax1.legend(*scatter1.legend_elements(), loc="upper right", title="Clusters", framealpha=0.3)
        fig1.savefig(f"results/dn_{self.radius}__model_{model}_{self.density_file_name.split('.')[0]}.pdf", format="pdf")
        plt.show()


