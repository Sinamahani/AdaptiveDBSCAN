import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.spatial import distance_matrix
from mpl_toolkits.basemap import Basemap

##LOADING DATA
dataset = pd.read_csv(r"M_cat2.csv")
dataset["Label"] = ''


#-------------------------------------------------------------------------------
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
    
    print(Min_Points)

    for i in range(m):
        if dataset["Label"][i] == '':
            seeds = []    
            
            PointNeighbor = np.where(DistanceMatrix[i] <= eps)[0]

            if len(PointNeighbor) >= Min_Points[i]:
                C = C+1
                # 
                seeds.append(i)
                
                while len(seeds) != 0:
                    PointNeighbor = np.where(DistanceMatrix[seeds[0]]<=eps)[0]
                    dataset["Label"][seeds[0]] = C
                    ExpandCluster(dataset, PointNeighbor, seeds)
                    seeds = seeds[1:]
                    
            else:
                dataset["Label"][i] = 0
                

    return dataset
#-------------------------------------------------------------------------------              
#Running the code          
dataset = MagDBSCAN(dataset, 0.225)


#-------------------------------------------------------------------------------
##Plotting Part
#here after using Basemap from Matplotlib module, the basemap willm be plotted and then, using sctter, earthquaes will be plotted
dataset.to_csv(r"New_225.csv")
m = Basemap( projection='cyl',llcrnrlat=23,urcrnrlat=44,llcrnrlon=41.3,urcrnrlon=65.1,resolution='l')  #for resulotion "l" means low and "f" means full quality.
m.drawcoastlines()
m.drawparallels(np.arange(20,50,5),labels=[1,0,0,0])  #labels shows the side I want to indicate the axis
m.drawmeridians(np.arange(40,70,5), labels=[0,0,0,1])
m.shadedrelief()
#plotting earthquakes 
plt.scatter(dataset["Lon"], dataset["Lat"], c=dataset["Label"],marker=".")
plt.savefig("map.png",dpi=400)
plt.show()