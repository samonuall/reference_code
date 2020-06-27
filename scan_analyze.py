"""Parses advertisement data collected by BLE scanner by reading csv files and 
converting them to numpy arrays. Analyzes collected RSSI values
and attempts to predict the corresponding distance between the advertiser
and scanner. 
Optional arguments:
	-Specific csv files to be read
	-If no arguments entered, all csv files in directory are analyzed
"""
from pathlib import Path
from collections import Counter
import sys
import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

expected_values = {}

def most_frequent(Array, f_count): 
    if len(Array) <= 1:
	    print('{} is empty'.format(scan_data[f_count]))
	    return 0
    occurence_count = Counter(Array) 
    return occurence_count.most_common(1)[0][0] 
    

def average(array):
	return round(np.sum(array) / array.shape[0], 2)



#Make list scan_data containing str names of each csv file in the directory
if(len(sys.argv)) > 1:
	#Puts only csv files into scan_data, ignoring files without .csv ending
	scan_data = [sys.argv[i] for i in range(1, len(sys.argv)) 
							if '.csv' in sys.argv[i]]
else:
	cur_dir = Path(os.getcwd())
	scan_data = [str(f) for f in cur_dir.glob('*.csv')]
	scan_data.sort()
def main():
	plots = []
	#create figures each containing at most two graphs
	for l in range(len(scan_data) // 2):
		plots.append(plt.subplots(2))
	if len(scan_data) % 2 is 1:
		plots.append(plt.subplots())
	#iterate through subplots, two graphs per figure. file_count keeps
	#track of which csv file to parse from the scan_data list
	file_count = 0
	for fig, axs in plots:
		for ax_count in range(2):
			if not isinstance(axs, np.ndarray):
				 if file_count == len(scan_data):
					 continue
				 axis = axs
			else:
				axis = axs[ax_count]
			file_name = scan_data[file_count]
			data = pd.read_csv(file_name)
			data = data['RSSI'].to_numpy()
			x_axis = [x for x in range(data.shape[0])]
			axis.scatter(x_axis, data, marker='o')
		
			mode = most_frequent(data, file_count)
			axis.plot(x_axis, [mode]*data.shape[0], linestyle='--',
					label='Mode = {}'.format(mode))
		
			axis.plot(x_axis, [average(data[:j]) for j in range(data.shape[0])], 
					linestyle='--', label='Average')
			axis.set_ylabel('RSSI Value')
			axis.legend(loc='best')
			#Make name of subplot <date, time>
			axis.title.set_text('{}, {}:{}'.format(file_name[-15:-11], 
											file_name[-10:-8], 
											file_name[-7:-5]))
			file_count += 1
		
	plt.show()
	

if __name__ == "__main__":
	main()
