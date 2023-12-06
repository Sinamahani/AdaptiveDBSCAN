[![DOI](https://zenodo.org/badge/528950247.svg)](https://zenodo.org/doi/10.5281/zenodo.10088081)
![Static Badge](https://img.shields.io/badge/License-MIT-yellow) ![Static Badge](https://img.shields.io/badge/ML-tested-blue) ![GitHub Repo stars](https://img.shields.io/github/stars/sinamahani/AdaptiveDBSCAN) ![GitHub all releases](https://img.shields.io/github/downloads/sinamahani/AdaptiveDBSCAN/total) 
<br>
![logo](https://github.com/Sinamahani/AdaptiveDBSCAN/blob/main/logo.png)
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
from dadbscan.dbscan import EQ_DBSCAN
```

------------------------------------------------------------------------------------<br>
###Phase1.
The first line is being used for creating density map and the second one is for applying the Density-Adaptive DBSCAN algorithm. 
Now by defining the N value you having database as a csv file, you can run the density algorithm:

initiating the EQ_density class:
```
N = 65
density = EQ_Density(N, database)
```

To test the program, you can download the test file from the github repo and use decl_cat.csv as database.
```
database = 'decl_cat.csv'
```

running calc_density method:
```
heat_matrix = density.calc_density()
```

plotting the density map:
```
density.plot_density(heat_matrix)
```

a feature that can be used is smoothing the density map. This can be done by using the following method:
```
smoothed_heat_matrix = density.cell_smoother(apply_smooth=True)
```

! All the matrixes are saved physically in the folder 'Results'.

------------------------------------------------------------------------------------<br>
###Phase2.
Now that you have the density map, you can run the Density-Adaptive DBSCAN algorithm. To do so, you need to define the following parameters:

```
radius = density.radius
density_file_names = f"Results/den_decl_cat__65_smooth.csv"
```

As it can be seen above, radius can be derived from the denisty class.
now it is time to initiate the dbscan class and run the algorithm:

```
clustering = clustering = dbscan(radius, density_file_name)
final = clustering.clustering()
clustering.plot_clusters()
final.to_csv(f"Results/R__{density_file_name}")
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
Sina Sabermahani, Andrew W. Frederiksen; Improved Earthquake Clustering Using a Density‐Adaptive DBSCAN Algorithm: An Example from Iran. Seismological Research Letters 2023; doi: https://doi-org.uml.idm.oclc.org/10.1785/0220220305

## License

This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
