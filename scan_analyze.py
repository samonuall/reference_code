"""Parses advertisement data collected by BLE scanner using pickled
data frames stored in scan_files folder. Analyzes collected RSSI values
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

def most_frequent(Array): 
    occurence_count = Counter(Array) 
    return occurence_count.most_common(1)[0][0] 

def main():
	cur_dir = Path(os.getcwd())
	scan_data = list(cur_dir.glob('pi_pact_scan*'))
	fig, axs = plt.subplots(2)
	for i in range(len(scan_data)):
		data = pd.read_csv(scan_data[i])['RSSI'].to_numpy()
		x_axis = [x for x in range(data.shape[0])]
		axs[i].plot(x_axis, data, label='RSSI', marker='o')
		axs[i].plot(x_axis, [most_frequent(data)]*data.shape[0], linestyle='--',
					label='Mode')
		axs[i].set_ylabel('RSSI Value')
		axs[i].legend(loc='upper right')
		plt.show()
	

if __name__ == "__main__":
	main()
