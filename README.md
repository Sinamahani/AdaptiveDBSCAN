[![DOI](https://zenodo.org/badge/528950247.svg)](https://zenodo.org/doi/10.5281/zenodo.10088081)
![Static Badge](https://img.shields.io/badge/License-MIT-yellow) ![Static Badge](https://img.shields.io/badge/ML-tested-blue) ![GitHub Repo stars](https://img.shields.io/github/stars/sinamahani/AdaptiveDBSCAN) ![GitHub all releases](https://img.shields.io/github/downloads/sinamahani/AdaptiveDBSCAN/total) 
<br>
![logo](https://github.com/Sinamahani/AdaptiveDBSCAN/blob/main/logo-dadbscan.png)
<br>
# AdaptiveDBSCAN

This is a normalized form of DBSCAN alogorithm that is based on varying number of neighbour. This algorithm is useful when your data has different density pattern. To get more information about the algorithm, please refer to the paper.

# installation
For the best performance, it is recommended to create a new environment and then install the package:
```
conda create -n dadbscan python
```

To install the package, you can use pip:<br>
```
pip install dadbscan
```

# Getting Started
After installing the package, you can use it as follows by importing the modules:

```
from dadbscan.density import EQ_Density
from dadbscan.clustering import dbscan
```

------------------------------------------------------------------------------------<br>
### Phase1.
The first line is being used for creating a density map and the second one is for applying the Density-Adaptive DBSCAN algorithm. 
Now by defining the N value you have database as a CSV file, and you can run the density algorithm:

initiating the EQ_density class:

In the new version of Adaptive DBSCAN, we have added a filering option that can used as below"
```
filters = {"col":["num_picks", "Lat", "Lat", "Lon", "Lon"],  #select column
           "op":['>', '>=', '<=', ">=", "<="],   # it is an string format like >, =, >=, !=
           "val":[3, 55, 70, -105, -70] #it can be string or digits}
N = 65 # number of cells like NxN
density = EQ_Density(N, data_file='YOUR_FILE_PATH', min_year=1900, max_year=2050, min_mag=1, max_mag=9,  filters=filters, map_extenion_value=0.1) #map_extension_value can used to extend the frame 
```

#### ! Remember to appropriately configure filters such as min_year, max_year, and others in your catalogue. Setting these values correctly according to your dataset is crucial; failing to do so may result in partial or complete filtering out of your catalogue.

To test the program, you can download the test file from the GitHub repo and use decl_cat.csv as a database. 
```
YOUR_FILE_PATH = 'decl_cat.csv'
```

! It should be noted that your dataset must have a header like below (order is not important but it is case-sensitive):
__Lat, Lon, (Depth,Year, Month, Mw)__
! If you have more columns in your dataset, you do NOT need to remove them. Lat and Lon are essentail and they are case sensitive.

running calc_density method:
```
heat_matrix = density.calc_density(minimum_density=10)  #setting the background value by minimum_density
```
In the command above, by adding `minimum_density = ...`, you can define the threshold for the minimum value of the density for each cell. The default value is 10.

plotting the density map:
```
density.plot_density()
```

a feature that can be used is smoothing the density map. This can be done by using the following method:
```
smoothed_heat_matrix = density.cell_smoother(apply_smooth=True)
```

! All the matrixes are saved physically in the folder 'Results' in two formats, __PNG__ and __CSV__.

------------------------------------------------------------------------------------<br>
### Phase2.
Now that you have the density map, you can run the Density-Adaptive DBSCAN algorithm. To do so, you need to define the following parameters:

```
radius = density.radius
density_file_name = "Results/den_decl_cat__65_smooth.csv"
```
! **be careful to correctly name the `density_file_name`.**

As can be seen above, the radius can be derived from the density class.
now it is time to initiate the dbscan class and run the algorithm:

```
clustering = dbscan(radius, density_file_name)
```
Step below can take  a few minutes to be done...
```
final = clustering.clustering()
```
```
clustering.plot_clusters()
```
If you have a shape file to plot it on the background, you can use it here.

```
clustering.plot_clusters(shape_file_address="data/ShapeFiles/World_Countries_Generalized.shp")
```

You can finally save the calculation results in a file by command below:
```
final.to_csv(f"Results/R__final.csv")
```

When plotting the clustered data, you have some options:
```
plot_clusters(self, **kwargs):
        """
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
```



## Reference
Sina Sabermahani, Andrew W. Frederiksen (2023), Improved Earthquake Clustering Using a Density‐Adaptive DBSCAN Algorithm: An Example from Iran. Seismological Research Letters, doi: https://doi-org.uml.idm.oclc.org/10.1785/0220220305

## License

This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
