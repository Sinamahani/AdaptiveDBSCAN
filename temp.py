import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.spatial import distance_matrix

dataset = pd.read_excel(r"data_isc.xlsx")



DistanceMatrix = distance_matrix(dataset[["Lon.","Lat."]], dataset[["Lon.","Lat."]])
C = 0                   #Cluster Counter
DB_radius = np.mean(DistanceMatrix)
DBBB = np.ravel(DistanceMatrix)
DBBB = np.sort(DBBB)
plt.plot(DBBB)
print(DBBB)



