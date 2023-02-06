Here we are presenting a new approach to use DBSCAN lgorithm which is more efficient when deaking with data with different density.
We developed the algorithm for using on Seismic Catalog to cluster earthquakes with similar rate of seismicity in an area and the paper related to it is under review right now.

The program here consisting of several files explained in the following.

Density_map.py	This file calaculate the density map required for the technique
DN_DBSCAN.py	This file applies the proposed DBSCAN algorithm.
run_job.sh	This file is for the situation you need to apply several parameters at the same time, and it uses the SHELL to be run.
