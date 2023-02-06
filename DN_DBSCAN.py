# from datetime import datetime
# now = datetime.now()
import sys
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
import matplotlib
import geopandas as gpd

file_name, cell_number, radius = sys.argv
cell_number = int(cell_number)
radius = float(radius)


#-------------------------------------------------------------------------------
#HERE ARE FUNCTIONS FOR OPERATING DBSCAN ALGO.
#HERE ARE FUNCTIONS FOR OPERATING DBSCAN ALGO.
def ExpandCluster(dataset, PointNeighbor, seeds):
    for neighbor in PointNeighbor:
        if (dataset["Label"][neighbor] == '' or dataset["Label"][neighbor] == 0) and neighbor not in seeds:
            seeds.append(neighbor)

       
def MagDBSCAN (dataset, eps):
    # max_magnitude = np.max(dataset["Mw"])
    m = dataset.shape[0]
    
    DistanceMatrix = distance_matrix(dataset[["Lon","Lat"]], dataset[["Lon","Lat"]])
    C = 0                   #Cluster Counter
    
    Min_Points = (dataset["Density"])
    # Min_Points = 1*np.ceil(dataset["Mw"])
    # eps = np.ceil(dataset["Mw"])*0.1
    
    #print(Min_Points)

    for i in range(m):
        if dataset.Label[i] == '':
            seeds = []    
            
            PointNeighbor = np.where(DistanceMatrix[i] <= eps)[0]

            if len(PointNeighbor) >= Min_Points[i]+1:
                C = C+1
                # 
                seeds.append(i)
                
                while len(seeds) != 0:
                    PointNeighbor = np.where(DistanceMatrix[seeds[0]]<=eps)[0]
                    dataset.loc[seeds[0],("Label")] = C
                    ExpandCluster(dataset, PointNeighbor, seeds)
                    seeds = seeds[1:]
                    
            else:
                dataset.loc[i,("Label")] = 0
                

    return dataset


def plot_cluster_names(cluster_center_location):
    """this function is written to plot clusters names in the map"""
    loc = cluster_center_location
    for ind in loc.index:
        plt.text(loc["Lon"][ind], loc["Lat"][ind], f"{loc['Label'][ind]}", size=12, color="white")
        
#-------------------------------------------------------------------------------              
#Running the code 

##LOADING DATA
dataset = pd.read_csv(r"den_cat.csv")
dataset["Label"] = ''
#radius  = 0.1559

final = MagDBSCAN(dataset, radius)


#-------------------------------------------------------------------------------
##Plotting Part
x,y,c = final.Lon[final.Label>0], final.Lat[final.Label>0], final.Label[final.Label>0]
x_noise, y_noise, c_noise = final.Lon[final.Label==0], final.Lat[final.Label==0], final.Label[final.Label==0]
colors  = [f"C{i}" for i in np.arange(1, c.max()+1)]
cmap, norm = matplotlib.colors.from_levels_and_colors(np.arange(1, c.max()+2), colors)


fig1, ax1 = plt.subplots(figsize=(5,5))


print(final.groupby("Label").count())


#-------------------------------------------------------------------------------
##Plotting Part
#first I want to define the model to compare with
#model="None"
#model="mirzaei98"
#model="zafarani"
#model ="Ansari"
#model="Berberian76"
model="tahernia"

#here after using Basemap from Matplotlib module, the basemap will be plotted and then, using sctter, earthquaes will be plotted
###final.to_csv(f"Result__{radius}_dens_{cell_number}_model_{model}.csv")
m = Basemap( projection='cyl',llcrnrlat=24.8,urcrnrlat=41,llcrnrlon=42.5,urcrnrlon=63.5,resolution='f')  #for resulotion "l" means low and "f" means full quality.
#zooming in
#m = Basemap( projection='cyl',llcrnrlat=35.2,urcrnrlat=36.1,llcrnrlon=48.5,urcrnrlon=49.5,resolution='f')
#m.drawcoastlines()
m.drawparallels(np.arange(19,50,4),dashes=[6,6], labels=[1,0,0,0], color='grey')  #labels shows the side I want to indicate the axis
m.drawmeridians(np.arange(37,70,4),dashes=[6,6], labels=[0,0,0,1], color='grey')
m.drawcountries(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
m.shadedrelief(scale=0.5)
if model != "None":
    shape_file = gpd.read_file(f"shape-files/{model}.shp")
    shape_file.plot(ax=ax1, color="white", linewidth=2)

scatter2 = ax1.scatter(x_noise, y_noise, c="k",s=1, alpha=0.25)
    
scatter1 = ax1.scatter(x, y, c=c, cmap="turbo",linewidths=0.05,edgecolor='k',s=10)

ax1.legend(*scatter1.legend_elements(), loc="upper right", title="Clusters", framealpha=0.3)

#plt.show()
fig1.savefig(f"results/dn_{radius}_dens_{cell_number}_model_{model}.pdf", format="pdf")
print("---")
print(f"dn_{radius}_dens_{cell_number}_model_{model}.pdf is successfully saved!")
print("---")