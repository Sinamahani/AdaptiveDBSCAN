Introducing a more efficient approach to using the DBSCAN algorithm for data with varying densities. Our solution has been specifically developed for clustering earthquakes in a seismic catalog based on similar seismicity rates in a given area. The related paper is currently under review.

This repository consists of several files, which will be outlined below.

Density_map.py	This file calaculate the density map required for the technique
DN_DBSCAN.py	This file applies the proposed DBSCAN algorithm.
run_job.sh	This file is for the situation you need to apply several parameters at the same time, and it uses the SHELL to be run.
