import sys
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
import matplotlib
import geopandas as gpd

##LOADING DATA
dataset = pd.read_csv(r"den_cat.csv")

x, y, z, density = dataset["Lon"], dataset["Lat"], dataset["Mw"], dataset["Density"]

#-------------------------------------------------------------------------------



ax = plt.axes(projection='3d')






#here after using Basemap from Matplotlib module, the basemap will be plotted and then, using sctter, earthquaes will be plotted
m = Basemap( projection='cyl',llcrnrlat=24.8,urcrnrlat=41,llcrnrlon=42.5,urcrnrlon=63.5,resolution='f')  #for resulotion "l" means low and "f" means full quality.
#zooming in
#m = Basemap( projection='cyl',llcrnrlat=35.2,urcrnrlat=36.1,llcrnrlon=48.5,urcrnrlon=49.5,resolution='f')
#m.drawcoastlines()
#m.drawparallels(np.arange(19,50,4),dashes=[6,6], labels=[1,0,0,0], color='grey')  #labels shows the side I want to indicate the axis
#m.drawmeridians(np.arange(37,70,4),dashes=[6,6], labels=[0,0,0,1], color='grey')
#m.drawcountries(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
#m.shadedrelief(scale=0.5)


scatter2 = ax.plot_trisurf(x, y, density, cmap='viridis', edgecolor='none')
    

plt.show()
fig1.savefig(f"density.pdf", format="pdf")
