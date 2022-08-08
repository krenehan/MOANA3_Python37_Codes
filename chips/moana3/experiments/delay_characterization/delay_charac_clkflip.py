from includes import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from find_delay import *

# reading from csv data

data1 = pd.read_csv('../../data/dword0to100_sub454_clkflip.csv', header = None)
data2 = pd.read_csv('../../data/dword101to200_sub554_clkflip.csv', header = None)
data3 = pd.read_csv('../../data/dword201to256_sub654_clkflip.csv', header = None)

# dropping null value columns to avoid errors
data1.dropna(inplace = True)
data2.dropna(inplace = True)
data3.dropna(inplace = True)

#Convert to numpy array
arr1 = np.array(data1[1]).astype(int) #dword 0 to 100
arr1 = np.reshape(arr1, (101, 150)) #sub = 454
  
arr2 = np.array(data2[1]).astype(int) #dword 101 to 200
arr2 = np.reshape(arr2, (100, 150)) #sub = 554

arr3 = np.array(data3[1]).astype(int) #dword 201 to 256
arr3 = np.reshape(arr3, (55, 150)) #sub = 654

# Padded array shape
zero = np.zeros(100, dtype = int)
arr1_padded = np.empty((101, 350), dtype=int)
arr2_padded = np.empty((100,350), dtype=int)
arr3_padded = np.empty((55,350), dtype=int)
t = np.linspace(0,349,num = 350)*65 

# Pad histograms to remove subtractor value change effects
for histogram in range(len(arr1)):
    arr1_padded[histogram] = np.concatenate((zero, zero,arr1[histogram] ))
    plt.plot(arr1_padded[histogram])
    
for i in range(len(arr2)):
    arr2_padded[i] = np.concatenate((zero,arr2[i], zero))   
    plt.plot(arr2_padded[i])
    
for j in range(len(arr3)):
    arr3_padded[j] = np.concatenate((arr3[j],zero,zero))    
    plt.plot(arr3_padded[j])

# Concatenate arrays
arr_combined = np.concatenate((arr1_padded,arr2_padded,arr3_padded))

# Plot raw data
for h in range(len(arr_combined)):
    plt.plot(arr_combined[h])
    
delay = mean_time(t,arr_combined[0],arr_combined[1])
arr_delayed = np.empty((255), dtype = float)

# Find delay steps
for h in range(len(arr_delayed)):
    arr_delayed[h] = mean_time(t,arr_combined[h],arr_combined[h+1])*-1

# Find delay line for each step and convert from ps to ns     
step = np.empty((254), dtype = float)     
for h in range (len(step)):
    if (h == 0):
        step[0] = arr_delayed[0]/1000
    elif (h == 1):
        step[1] = np.sum((arr_delayed[0],arr_delayed[h]))/1000
    else:
        step[h] = np.sum((step[h-1],arr_delayed[h]/1000))
        
step = np.round(step,3)    

def get_step_clkflip():
    return step   
    
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

# Sum the array
arr_summed = np.empty_like(arr_delayed)
for i in range(len(arr_delayed)):
    arr_summed[i] = np.sum(arr_delayed[0:i])
arr_summed = arr_summed / 1000
    
# Print to text file
s = ''

val = round(arr_summed[1], 3)
prev_val = round(arr_summed[0], 3)
s = s + \
'''if (adjusted_delay_ns < {}):
    word = {}
    actual_delay_ns = {} + self.__base_delay_ns
    
'''.format(val, 0, prev_val)

for entry in range(1, len(arr_summed)-1):
    val = round(arr_summed[entry+1], 3)
    prev_val = round(arr_summed[entry], 3)
    s = s + \
    '''elif (adjusted_delay_ns < {}):
    word = {}
    actual_delay_ns = {} + self.__base_delay_ns
    
'''.format(val, entry, prev_val)

prev_val = round(arr_summed[254], 3)
s = s + \
'''else:
    word = {}
    actual_delay_ns = {} + self.__base_delay_ns
    raise DelayLineException("Delay value is too large")
    
'''.format(254, prev_val)
    
f = open('delay_charac_clkflip.txt', 'w')
f.write(s)
f.close()