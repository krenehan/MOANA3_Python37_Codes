from includes import *
import matplotlib.pyplot as plt
from copy import deepcopy


# =============================================================================
# Top-level parameters
# =============================================================================
# Number of reads to time and average
iterations = 1000
    
    
try:
    # =============================================================================
    # Test Platform setup
    # =============================================================================

    # Start and stop values
    start = 300
    stop = 8000000
    
    # Packet size
    packet_size = np.logspace(np.log10(start), np.log10(stop), 100, dtype=int)
    packet_size = packet_size // 2 * 2
    
    # Packet time
    packet_trigger_time_ms = np.zeros_like(packet_size, dtype=float)
    packet_read_time_ms = np.zeros_like(packet_size, dtype=float)
    
    # Pipeout address
    addr = 0XB8

    for p_idx, p_val in enumerate(packet_size):
        
        # Print packet size
        print("---------------------------------- Packet size is " + str(p_val/1e6) + " MB ----------------------------------")
        
        # Create packet of correct size
        packet = bytearray(p_val)

        trigger_time_ns = np.zeros( (iterations,), dtype=float)
        read_time_ns = np.zeros( (iterations,), dtype=float)
        
        # Instantiate test platform
        dut = test_platform.TestPlatform("moana3")

        # Program the FPGA
        dut.init_fpga(bitfile_path = paths.bitfile_path, refclk_freq=50e6)
        
        for i in range(iterations):
            
            t_start = time.perf_counter_ns()
            dut.check_ram_trigger()
            t_middle = time.perf_counter_ns()
            dut.fpga_interface.xem.ReadFromPipeOut(addr, packet)
            t_end = time.perf_counter_ns()
            
            trigger_time_ns[i] = t_middle - t_start
            read_time_ns[i] = t_end - t_middle
            
        dut.fpga_interface.xem.Close()
            
        # Take the averages
        packet_trigger_time_ms[p_idx] = round(np.mean(trigger_time_ns) / 1e6, 3)
        packet_read_time_ms[p_idx] = round(np.mean(read_time_ns) / 1e6, 3)
        
        # Print
        print("Average trigger time was " + str(packet_trigger_time_ms[p_idx]) + " ms")
        print("Average read time was " + str(packet_read_time_ms[p_idx]) + " ms")
                
    
# =============================================================================
# Disable supplies, close plots, log files, and FPGA on exit
# =============================================================================
finally:
    print("Closing FPGA")
    dut.fpga_interface.xem.Close()
    
    
#%%

plt.close('all')

# Calculate total time for packet readout
# packet_total_time_ms = packet_trigger_time_ms + packet_read_time_ms

packet_size = np.array([    300,     332,     368,     408,     452,     500,     556, \
           616,     682,     756,     838,     930,    1030,    1142, \
          1266,    1404,    1556,    1726,    1912,    2120,    2350, \
          2604,    2888,    3200,    3548,    3932,    4360,    4832, \
          5356,    5936,    6580,    7294,    8086,    8962,    9934, \
         11010,   12204,   13528,   14996,   16622,   18424,   20420, \
         22636,   25090,   27810,   30826,   34168,   37872,   41980, \
         46532,   51576,   57168,   63368,   70238,   77854,   86296, \
         95652,  106024,  117520,  130262,  144386,  160040,  177394, \
        196628,  217948,  241578,  267772,  296806,  328988,  364658, \
        404196,  448022,  496600,  550444,  610128,  676282,  749608, \
        830884,  920974, 1020832, 1131518, 1254204, 1390192, 1540926, \
       1708002, 1893194, 2098466, 2325994, 2578194, 2857738, 3167590, \
       3511040, 3891730, 4313694, 4781412, 5299842, 5874482, 6511430, \
       7217440, 8000000], dtype=int) 
packet_total_time_ms = np.array([  2.575,   2.669,   2.665,   2.727,   2.694,   2.725,   2.525, \
         2.572,   2.727,   2.723,   2.722,   2.681,   3.642,   3.69 , \
         3.679,   3.659,   3.707,   3.727,   3.709,   3.715,   3.67 , \
         3.682,   3.737,   3.343,   3.758,   3.796,   3.867,   3.871, \
         3.908,   3.937,   3.975,   4.034,   4.025,   4.093,   4.154, \
         4.148,   4.122,   4.221,   3.948,   4.369,   4.354,   4.427, \
         4.598,   4.598,   4.652,   4.804,   4.919,   4.925,   5.094, \
         5.285,   4.953,   5.616,   5.831,   5.963,   6.121,   6.445, \
         6.646,   6.778,   7.262,   7.261,   7.937,   8.519,   8.851, \
         9.373,  10.218,  10.798,  11.19 ,  12.206,  12.978,  13.965, \
        15.214,  16.554,  17.637,  19.303,  20.669,  22.427,  24.285, \
        27.309,  29.064,  31.891,  34.687,  38.071,  41.562,  45.676, \
        50.076,  54.801,  60.305,  66.589,  73.424,  80.904,  89.073, \
        98.367, 108.704, 120.023, 132.573, 146.523, 161.907, 179.712, \
       198.774, 219.585])

# Calculate data rate
data_rate_MBPS = (packet_size / 1e6) / (packet_total_time_ms / 1000)

# Plot transfer size vs time
plt.figure()
plt.title("Readout Time vs Packet Size")
plt.xlabel("Packet Size (MB)")
plt.ylabel("Readout Time (ms)")
plt.plot(packet_size / 1e6, packet_total_time_ms)

# Plot data rate vs packet size including trigger read time
plt.figure()
plt.title("Data Rate vs Transfer Size")
plt.xlabel("Transfer Size (MB)")
plt.ylabel("Data Rate (MBPS)")
plt.plot(packet_size / 1e6, data_rate_MBPS, marker='.')
plt.axvline(.0768, color='red', linestyle='--')


