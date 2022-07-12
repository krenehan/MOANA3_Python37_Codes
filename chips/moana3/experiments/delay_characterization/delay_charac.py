from includes import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from find_delay import *

# reading from csv data
data1 = pd.read_csv('../../data/delay_characterization/dword_0to100_rising_sub354.csv', header = None)
data2 = pd.read_csv('../../data/delay_characterization/dword_101to200_rising_sub454.csv', header = None)
data3 = pd.read_csv('../../data/delay_characterization/dword_201to256_rising_sub554.csv', header = None)

# dropping null value columns to avoid errors
data1.dropna(inplace = True)
data2.dropna(inplace = True)
data3.dropna(inplace = True)

# Convert to numpy array
arr1 = np.array(data1[1]).astype(int) #dword 0 to 100
arr1 = np.reshape(arr1, (101, 150)) #sub = 354
  
arr2 = np.array(data2[1]).astype(int) #dword 101 to 200
arr2 = np.reshape(arr2, (100, 150)) #sub = 454

arr3 = np.array(data3[1]).astype(int) #dword 201 to 256
arr3 = np.reshape(arr3, (55, 150)) #sub = 554

# Padded array shape
zero = np.zeros(100, dtype = int)
arr1_padded = np.empty((101, 350), dtype=int)
arr2_padded = np.empty((100,350), dtype=int)
arr3_padded = np.empty((55,350), dtype=int)

# Time axis creation
t = np.linspace(0,349,num = 350)*65 

# Pad histograms to remove subtractor value change effects
for histogram in range(len(arr1)):
    arr1_padded[histogram] = np.concatenate((zero, zero,arr1[histogram] ))
    # plt.plot(arr1_padded[histogram])

for i in range(len(arr2)):
    arr2_padded[i] = np.concatenate((zero,arr2[i], zero))   
    # plt.plot(arr2_padded[i])
    
for j in range(len(arr3)):
    arr3_padded[j] = np.concatenate((arr3[j],zero,zero))    
    # plt.plot(arr3_padded[j])

# Concatenate arrays
arr_combined = np.concatenate((arr1_padded,arr2_padded,arr3_padded))

# Plot raw data
for h in range(len(arr_combined)):
    plt.plot(arr_combined[h])
    
# Find delay steps
arr_delayed = np.empty((255), dtype = float)
for h in range(len(arr_delayed)):
    arr_delayed[h] = find_delay(t,arr_combined[h],arr_combined[h+1]) * -1
    
# Plot delay step versus code
plt.figure()
plt.plot(arr_delayed)
plt.title("Delay Step vs Input Code")
plt.xlabel("Delay Step")
plt.ylabel("Delay Step (ps)")

# Print some stats
print("Mean Step (ps): " + str(np.mean(arr_delayed)))
print("Median Step (ps): " + str(np.median(arr_delayed)))
print("Standard Deviation (ps): " + str(np.std(arr_delayed)))
print("Minimum Delay Step (ps): " + str(np.amin(arr_delayed)))
print("Maximum Delay Step (ps): " + str(np.amax(arr_delayed)))
print("Full Range (ns): " + str(np.sum(arr_delayed)/1000))