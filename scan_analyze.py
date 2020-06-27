"""Parses advertisement data collected by BLE scanner by reading csv files and 
converting them to numpy arrays. Analyzes collected RSSI values
and attempts to predict the corresponding distance between the advertiser
and scanner. 
Optional arguments:
	-Specific csv files to be read
	-Prefix of csv files to be read
	-p at END of arguments specifies that each file's RSSI data will be plotted
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

#RSSI baseline: inches between scanner and advertiser. Based off of data with 
#no obstructions.

expected_values = {-28: '0-10', -35: '10-20', -39: '20-30', -48: '30-40',
					-58: '40-50', -65: '50-60', -71: '61+'}

def most_frequent(Array, f_count): 
    if len(Array) <= 1:
	    print('{} is empty'.format(scan_data[f_count]))
	    return 0
    occurence_count = Counter(Array) 
    return occurence_count.most_common(1)[0][0] 
    

def average(array):
	return round(np.sum(array) / array.shape[0], 2)



def estimate_dist(RSSI):
	for key in expected_values:
		if RSSI < key:
			continue
		else:
			no_obst_dist = expected_values[key]
			break
	else:
		no_obst_dist = expected_values[key]
	
	return no_obst_dist
		


#Plots RSSI data from csv files in scan_data list. Returns a list of the modes
#for each scan file
def plot_files(scan_data, plot):
	plots = []
	modes = []
	
	#If plot option is false, just return modes without plotting graphs
	if not plot:
		for file_count, file_name in enumerate(scan_data):
			data = pd.read_csv(file_name)
			data = data['RSSI'].to_numpy()
			mode = most_frequent(data, file_count)
			modes.append(mode)
		return modes
	
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
			modes.append(mode)
			axis.plot(x_axis, [mode]*data.shape[0], linestyle='--',
					label='Mode = {}'.format(mode))
		
			axis.plot(x_axis, [average(data[:j]) for j in range(data.shape[0])], 
					linestyle='--', label='Average')
			axis.set_ylabel('RSSI Value')
			axis.legend(loc='best')
			#Make name of subplot <prefix, date:minute>
			axis.title.set_text('{}, {}, {}'.format(os.path.basename(file_name)[:-20], 
											file_name[-14:-11], 
											file_name[-8:-4]))
			file_count += 1
		
	plt.show()
	return modes
	


def main():
	plot = False
	#Make list scan_data containing str names of each csv file in the directory
	if(len(sys.argv)) > 1:
		if '.' in sys.argv[1]:
			#Puts only csv files into scan_data, ignoring files without .csv ending
			scan_data = [sys.argv[i] for i in range(1, len(sys.argv)) 
									if '.csv' in sys.argv[i]]
		else:
			cur_dir = Path(os.getcwd())
			#glob all csv files with entered in prefix
			scan_data = []
			for i in range(1, len(sys.argv)):
				scan_data.extend(cur_dir.glob('{}*.csv'.format(sys.argv[i])))
			scan_data = [str(f) for f in scan_data]
			scan_data.sort()
	else:
		cur_dir = Path(os.getcwd())
		scan_data = [str(f) for f in cur_dir.glob('*.csv')]
		scan_data.sort()
	
	if sys.argv[-1] is 'p':
		plot = True
	modes = plot_files(scan_data, plot)
	for mode in modes:
		print(estimate_dist(mode))

if __name__ == "__main__":
	main()
