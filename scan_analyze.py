"""Parses advertisement data collected by BLE scanner by reading csv files and 
converting them to numpy arrays. Analyzes collected RSSI values
and attempts to predict the corresponding distance between the advertiser
and scanner."""
from pathlib import Path
from collections import Counter
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


cur_dir = Path(os.getcwd())
scan_data = list(cur_dir.glob('pi_pact_scan*'))
scan_data.sort()
def main():
	plots = []
	#create figures each containing at most two graphs
	for l in range(len(scan_data) // 2):
		plots.append(plt.subplots(2))
	if len(scan_data) % 2 is 1:
		plots.append(plt.subplots())
	#iterte through subplots, two graphs per figure. file_count keeps
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
			data = pd.read_csv(scan_data[file_count])
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
			axis.title.set_text('File {}'.format(file_count))
			file_count += 1
		
	plt.show()
	

if __name__ == "__main__":
	main()
