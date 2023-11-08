from sklearn.cluster import DBSCAN, SpectralClustering
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
import numpy as np

#dataset = pd.read_csv(r"M_cat1_1.csv")
X = pd.DataFrame(zip(dataset.Lat, dataset.Lon), columns=["Lat","Lon"])
clustering = DBSCAN(eps=0.246, min_samples=5).fit(X)

final = pd.DataFrame(zip(dataset.Lat, dataset.Lon, clustering.labels_),
                     columns=["Lat","Lon", "Label"])

# m = Basemap( projection='cyl',llcrnrlat=23,urcrnrlat=44,llcrnrlon=41.3,urcrnrlon=65.1,resolution='f')  #for resulotion "l" means low and "f" means full quality.
# m.drawcoastlines()
# m.drawparallels(np.arange(20,50,5),labels=[1,0,0,0])  #labels shows the side I want to indicate the axis
# m.drawmeridians(np.arange(40,70,5), labels=[0,0,0,1])
# m.shadedrelief()
#plotting earthquakes 
final_final = final[final.Label >= 0]
s = 10 * np.ones(len(final_final))
plt.scatter(final_final["Lon"], final_final["Lat"], c=final_final["Label"], s=s,marker=".")
plt.show()
