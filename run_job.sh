#!/bin/bash
#conda activate dbscan
#cd Documents/Course/AD\ Seismology\ 2/DBSCAN/test\ 2/
#Read the string value

# Set comma as delimiter
IFS=','

#Read the split words into an array based on comma delimiter
read -a strarr <<< "$text"

#for i in 40,0.243 45,0.192 50,0.155 55,0.1289 60,0.108 65,0.0922 70,0.0795 75,0.0692 80,0.060898
for i in 55,0.1289 60,0.108 65,0.0922
do
	read -a strarr <<< "$i"
	echo 
	echo 
	echo ">>>>>>> Processing Cell:${strarr[0]}, Radius:${strarr[1]}"
	echo 
	echo 
	python density.py "${strarr[0]}"
	python MagDBSCAN.py "${strarr[0]}" "${strarr[1]}"
done