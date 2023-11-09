![Static Badge](https://img.shields.io/badge/License-MIT-yellow) ![Static Badge](https://img.shields.io/badge/ML-tested-blue)
![Logo](https://github.com/Sinamahani/AdaptiveDBSCAN/logo.png](https://github.com/Sinamahani/AdaptiveDBSCAN/blob/main/logo.png)

# AdaptiveDBSCAN
This is a normalized form of DBSCAN alogorithm that is based on varying number of neighbour. This algorithm is useful when your data has different density pattern. To get more information about the algorithm, please refer to the paper.

# installation
To install the package, you can use pip:
```pip install dadbscan```

# Getting Started
After installing the package, you can use it as follows by importing the modules:

```from dadbscan.density import EQ_Density```
```from dadbscan.dbscan import EQ_DBSCAN```

###Phase1.
The first line is being used for creating density map and the second one is for applying the Density-Adaptive DBSCAN algorithm. 
Now by defining the N value you having database as a csv file, you can run the density algorithm:

initiating the EQ_density class:
```
N = 65
density = EQ_Density(N, database)```

running calc_density method:
```heat_matrix = density.calc_density()```

plotting the density map:
```density.plot_density(heat_matrix)```

a feature that can be used is smoothing the density map. This can be done by using the following method:
```smoothed_heat_matrix = density.cell_smoother(apply_smooth=True)```

! All the matrixes are saved physically in the folder 'Results'.


###Phase2.
Now that you have the density map, you can run the Density-Adaptive DBSCAN algorithm. To do so, you need to define the following parameters:

```radius = density.radius
density_file_names = f"Results/den_decl_cat__65_smooth.csv"```

As it can be seen above, radius can be derived from the denisty class.
now it is time to initiate the dbscan class and run the algorithm:

```clustering = clustering = dbscan(radius, density_file_name)
final = clustering.clustering()
clustering.plot_clusters()
final.to_csv(f"Results/R__{density_file_name.split('/')[1]}")```



## Reference
Sabermahani, S., Frederiksen, A., 2023, Improved earthquake clustering using a Density-Adaptive DBSCAN algorithm: an example from Iran, Seismological Research Letters

## License

This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
