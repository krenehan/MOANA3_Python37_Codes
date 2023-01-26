# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:01:11 2020

The MultipleDataPlotter class interprets data coming off of one or more MOANA chips and plots it.

@author: Kevin Renehan
"""

import numpy as np
import matplotlib.pyplot as plt
from time import sleep

# ===========================================================
# Data Plotter class for parsing, plotting, and saving MOANA data
# ===========================================================
class MultipleDataPlotter:
    
    # Class options
    raw_plotting = False
    show_peak = False
    show_coarse_fine = False
    plot_logarithmic = False
    fix_y_max = False
    fast_mode = False
    show_plot_info = False
    
    # Number of chips
    __number_of_chips = 1
    
    # Frame variables
    __number_of_frames = 1
    __meas_per_patt = 1
    __patterns_per_frame = 1
    
    # Class variables
    __bins_per_histogram = 0
    __bin_size = 12
    __transfer_size = 1824
    
    # Subtractor value
    __subtractor_value = 0
    
    # VCSEL
    __vcsel_setting = 0
    __vcsel_setting_set = False
    __vcsel_delays = [0.12, 0.24, 0.36, 0.48]
    __vcsel_latency = 0.72
    
    # SPADs
    __spad_rise_time = 0
    __tdc_resolution = 65e-3
        
    # The current capture number
    __current_capture = 0 
    
    # Axis limits
    __ymax = 0.0
    
    # Plot status
    __plot_figure_spawned = False
    __plot_legend_spawned = False
    
    # Figure resized status
    __figure_resized = False
    __resized_dimensions = [0, 0]
    
    # Text handles
    __text_handle = None
    
    # Muted plots
    __muted_chips = []
    
    # Data packet object
    __packet = None
    
    # Pattern colors
    __colors = ('blue', 'orange', 'green', 'yellow', 'silver', 'plum', 'crimson', 'brown', 'pink', 'cyan', 'maroon', 'khaki', 'chartreuse', 'coral', 'indigo', 'navy', 'blue', 'orange', 'green', 'yellow', 'silver', 'plum', 'crimson', 'brown', 'pink', 'cyan', 'maroon', 'khaki', 'chartreuse', 'coral', 'indigo', 'navy')
    

    # ===========================================================
    # Constructor
    # ===========================================================
    def __init__(self, packet, time_limits=[-1, -1], number_of_chips_to_plot=None, patterns_to_plot=None):
        
        # Store packet handle
        self.__packet = packet
        
        # Initialize parameters
        self.__number_of_chips                  = self.__packet.number_of_chips
        self.__meas_per_patt                    = self.__packet.measurements_per_pattern
        self.__number_of_frames                 = self.__packet.number_of_frames
        self.__period                           = self.__packet.period
        self.__bins_per_histogram               = self.__packet.bins_per_histogram
        self.__timestep                         = 5e-3
        
        if number_of_chips_to_plot is None:
            self.__number_of_chips_to_plot      = self.__number_of_chips 
        else:
            self.__number_of_chips_to_plot      = number_of_chips_to_plot
            
        if patterns_to_plot is None:
            self.__patterns_per_frame           = self.__packet.patterns_per_frame
        else:
            self.__patterns_per_frame             = patterns_to_plot
        
        # Time limits for plotting
        if time_limits == [-1, -1]:
            self.__time_limits = [0, self.__period/2]
        else:
            self.__time_limits = time_limits
            
        # Time axis data for plot
        self.__time_axis = np.arange(0, self.__time_limits[1] + self.__timestep, self.__timestep)
        
        # Time array and data, sliding window based on gating delay
        self.__time_array = np.zeros((self.__number_of_chips, self.__bins_per_histogram), dtype=float)
        self.__time_data = np.zeros_like(self.__time_array, dtype=int)
        
        # Time data that has been adjusted ot full axis bounds
        self.__transformed_time_data = np.zeros((self.__number_of_chips, len(self.__time_axis)), dtype= np.intc)
        
        # Data structure for plotting pattern-dependent data
        self.__full_capture_data = np.empty((self.__number_of_chips, self.__number_of_frames, self.__patterns_per_frame, self.__bins_per_histogram), dtype=int)
        
        # Data structures for average data storage
        self.__capture_data = np.zeros((self.__number_of_chips, self.__bins_per_histogram), dtype=int)
        
        # Total counts
        self._total_counts = np.empty((self.__number_of_chips), dtype=float)
        
        # Gating delays
        self.__gate_delay = np.zeros((self.__number_of_chips), dtype=float)
        self.__delay_line_word = np.zeros((self.__number_of_chips), dtype=int)
        self.__coarse = ['0000'] * self.__number_of_chips
        self.__fine = ['000'] * self.__number_of_chips

        # Figure handles
        self.__plot_figure = None
        self.__plot_line = []
        self.__plot_bg = None
        self.__plot_axes = [None] * self.__number_of_chips
        self.__subplot_spawned = [False] * self.__number_of_chips
        self.__plot_peak_spawned = [False] * self.__number_of_chips
        self.__peak_point = [None] * self.__number_of_chips
        self.__plot_peak_text = [None] * self.__number_of_chips
        self.__plot_info_text_spawned = [False] * self.__number_of_chips
        self.__plot_info_text = [None] * self.__number_of_chips
        self.__plot_mean_text = [None] * self.__number_of_chips
        
        # Accessory line handles
        self.__vcsel_line_spawned = [False] * self.__number_of_chips
        self.__vcsel_line = [None] * self.__number_of_chips
        self.__gating_line_spawned = [False] * self.__number_of_chips
        self.__gating_line = [None] * self.__number_of_chips
        
        # Shape of subplots
        self.__subplot_rows = int(np.ceil(np.sqrt(self.__number_of_chips_to_plot)))
        self.__subplot_cols = int(np.ceil(np.sqrt(self.__number_of_chips_to_plot)))
        if (self.__subplot_rows - 1) * self.__subplot_cols >= self.__number_of_chips_to_plot:
            self.__subplot_rows = self.__subplot_rows - 1
    
    
    # ===========================================================
    # Place the data in time based on the time gating delay
    # ===========================================================
    def __place_data_in_time(self):
        
        # Loop through chips
        for chip in range(self.__number_of_chips):
        
            # Create the time array
            self.__time_array[chip] = np.arange(self.__gate_delay[chip], self.__gate_delay[chip] + self.__tdc_resolution * self.__bins_per_histogram, self.__tdc_resolution)
            
            # Set the time data equal to the capture data
            self.__time_data[chip] = self.__capture_data[chip]
            
            # Remove the 0th bin
            self.__time_data[chip][0] = 0
            
        # Adjust time data to fit axis
        self.__transform_time_data()
        
        # Reset transformed time data to 0
        self.__transformed_time_data.fill(0)
        
        # Loop through chips
        for chip in range(self.__number_of_chips):
      
            # Loop through the averaged data, bin-by-bin
            for bin_number in range(1, self.__bins_per_histogram):
                
                # Find the time index based on the gating delay
                time_index = int( round((self.__gate_delay[chip] + bin_number * self.__tdc_resolution) / self.__timestep, 0))
                
                # Place the counts for the bin into the time_data array
                if (time_index < len(self.__time_axis)):
                    self.__transformed_time_data[chip][time_index] = self.__time_data[chip][bin_number]
                    
                    
    # ===========================================================
    # Transform the time data so that it fits the full time axis
    # ===========================================================
    def __transform_time_data(self):
        
        # Reset transformed time data to 0
        self.__transformed_time_data.fill(0)
        
        # Loop through chips
        for chip in range(self.__number_of_chips):
      
            # Loop through the averaged data, bin-by-bin
            for bin_number in range(1, self.__bins_per_histogram):
                
                # Find the time index based on the gating delay
                time_index = int( round((self.__gate_delay[chip] + bin_number * self.__tdc_resolution) / self.__timestep, 0))
                
                # Place the counts for the bin into the time_data array
                if (time_index < len(self.__time_axis)):
                    self.__transformed_time_data[chip][time_index] = self.__time_data[chip][bin_number]
        
        
    # ===========================================================        
    # Plot raw data as fast as is possible with Matplotlib.pyplot.
    # This function implements blitting, which dramatically increases the speed of the plot function, but comes at a cost.
    # Disadvantages:
    #   - Plot y-axis limit is fixed and is not updated dynamically
    #   - Size of plot figure cannot be changed. Currently no callback function to handle changes in figure size.
    #   - Plot features (log plotting, time plotting, plot info, peak, mean time, etc) not supported in this mode
    # TODO: Allow selectable patterns to be plotted
    # ===========================================================
    def __plot_raw_fast_pattern(self):
                
        if (self.__plot_figure_spawned) is False or (self.__figure_resized is True):
            
            # Close existing figures
            plt.close('all')
        
            # Figure handle
            self.__plot_figure, axes_structure = plt.subplots(self.__subplot_rows, self.__subplot_cols, sharex=True, sharey=True)
            
            # Maximize figure
            if not self.__plot_figure_spawned:
                figManager = plt.get_current_fig_manager()
                figManager.window.showMaximized()
            else:
                px = 1/plt.rcParams['figure.dpi']  # pixel in inches
                self.__plot_figure.set_size_inches(self.__resized_dimensions[0]*px, self.__resized_dimensions[1]*px)
            
            # Label graphs
            for ax in range(self.__number_of_chips_to_plot):
                
                self.__plot_axes[ax] = axes_structure.flat[ax]
                
                # Subplot title
                self.__plot_axes[ax].set_title('Chip ' + str(ax))
                
                # Subplot axis labels
                self.__plot_axes[ax].set(xlabel='Bin Number', ylabel='Counts')
                
                # Show units only on outer plots
                self.__plot_axes[ax].label_outer()
                
                # Set x-axis range
                self.__plot_axes[ax].set_xlim((0, 150))
                
                # Set y-axis range
                ymin = 1 if self.plot_logarithmic else 0
                if self.fix_y_max:
                    self.__plot_axes[ax].set_ylim((ymin, self.__ymax))
                else:
                    self.__plot_axes[ax].set_ylim((ymin, 1048575))
                
                # Spawn subplots
                for pattern in range(self.__patterns_per_frame):
                    
                    if self.plot_logarithmic:
                        
                        # Plot the data
                        self.__plot_line.append(self.__plot_axes[ax].semilogy(range(self.__bins_per_histogram), self.__full_capture_data[ax][0][pattern], color=self.__colors[pattern], animated=True, marker=None)[0])
                    
                    else:
                
                        # Plot the data
                        self.__plot_line.append(self.__plot_axes[ax].plot(range(self.__bins_per_histogram), self.__full_capture_data[ax][0][pattern], color=self.__colors[pattern], animated=True, marker=None)[0])
                    
                    # Add plot lines as artists
                    # self.__plot_axes[ax].add_artist
                                
                # Indicate the figure has been spawned
                self.__subplot_spawned[ax] = True
                
            # Get handles
            legend = ["Pattern " + str(z) for z in range(self.__patterns_per_frame)]
            self.__plot_figure.legend(legend, loc='upper right')
                
            # Advance GUI event loop so that plot is displayed
            plt.show(block=False)
            plt.pause(0.5)
                        
            # Capture background of plot
            self.__plot_bg = self.__plot_figure.canvas.copy_from_bbox(self.__plot_figure.bbox)
            
            # Draw the animated artist
            for chip in range(self.__number_of_chips_to_plot):
                for pattern in range(self.__patterns_per_frame):
                
                    # Draw artists
                    self.__plot_axes[chip].draw_artist(self.__plot_line[chip*self.__patterns_per_frame+pattern])
                
            # Push updates to screen
            self.__plot_figure.canvas.blit(self.__plot_figure.bbox)
                
            # Indicate plot has been spawned
            self.__plot_figure_spawned = True
            self.__figure_resized = False
            
            # Register callback for figure resize event
            if self.__plot_figure_spawned:
                self.__plot_figure.canvas.mpl_connect('resize_event', self.__on_resize)
             
        else:
            
            # Reset background
            self.__plot_figure.canvas.restore_region(self.__plot_bg)
        
            # Draw animated artists
            for chip in range(self.__number_of_chips_to_plot):
                
                for pattern in range(self.__patterns_per_frame):
    
                    # Update the line
                    self.__plot_line[chip*self.__patterns_per_frame+pattern].set_ydata(self.__full_capture_data[chip][0][pattern])

                    # Draw artists
                    self.__plot_axes[chip].draw_artist(self.__plot_line[chip*self.__patterns_per_frame+pattern])

        # Update y-axis range of all figures
        # self.__plot_axes[0].set_ylim([0, np.round(np.amax(self.__full_capture_data) * 1.1 + 1)])
                
        # Push updates to screen
        self.__plot_figure.canvas.blit(self.__plot_figure.bbox)
        self.__plot_figure.canvas.flush_events() 
        
        # Increment the capture count
        self.__current_capture = self.__current_capture + 1
        
        
    # ===========================================================        
    # Initialize the plot before plot_raw_fast_pattern
    # TODO: Determine if this is still needed
    # ===========================================================
    def __on_resize(self, event):
        self.__resized_dimensions[0] = event.width
        self.__resized_dimensions[1] = event.height
        self.__figure_resized = True
        
        
    # ===========================================================        
    # Initialize the plot before plot_raw_fast_pattern
    # TODO: Determine if this is still needed
    # ===========================================================
    def plot_init(self):
        
        if not self.__plot_figure_spawned:
            
            # Figure handle
            self.__plot_figure, axes_structure = plt.subplots(self.__subplot_rows, self.__subplot_cols, sharex=True, sharey=True)
            self.plot_figure = self.__plot_figure
            
            # Maximize figure
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            
            # Label graphs
            for ax in range(self.__number_of_chips):
                
                # Flatten axis for easier indexing
                self.__plot_axes[ax] = axes_structure.flat[ax]
                
                # Subplot title
                self.__plot_axes[ax].set_title('Chip ' + str(ax))
                
                # Subplot axis labels
                self.__plot_axes[ax].set(xlabel='Bin Number', ylabel='Counts')
                
                # Show units only on outer plots
                self.__plot_axes[ax].label_outer()
                
                # Set x-axis range
                self.__plot_axes[ax].set_xlim((0, 150))
                
                  # Set y-axis range
                self.__plot_axes[ax].set_ylim((0, 1048575))
                
            # Indicate plot has been spawned
            self.__plot_figure_spawned = True
            
        # Plot title with updated capture number
        self.__suptitle = self.__plot_figure.suptitle("Capture")

        # Loop through chips
        for chip in range(self.__number_of_chips):
        
            # Spawn the figure
            if not self.__subplot_spawned[chip]:
                
                for pattern in range(self.__patterns_per_frame):
                
                    # Plot the data
                    self.__plot_line.append(self.__plot_axes[chip].plot(range(self.__bins_per_histogram), self.__full_capture_data[chip][0][pattern], marker='.', color=self.__colors[pattern])[0])
                    
                    # Add plot lines as artists
                    self.__plot_axes[chip].add_artist
                                
                # Indicate the figure has been spawned
                self.__subplot_spawned[chip] = True
        

    # ===========================================================
    # Create a plot of the data wihtout time information
    # ===========================================================
    def __plot_raw(self):
        
        if not self.__plot_figure_spawned:
        
            # Close all figures
            plt.close('all')
            
            # Figure handle
            self.__plot_figure, axes_structure = plt.subplots(self.__subplot_rows, self.__subplot_cols, sharex=True, sharey=True)
            
            # Maximize figure
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            
            # Label graphs
            for ax in range(self.__number_of_chips):
                
                self.__plot_axes[ax] = axes_structure.flat[ax]
                
                # Subplot title
                self.__plot_axes[ax].set_title('Chip ' + str(ax))
                
                # Subplot axis labels
                self.__plot_axes[ax].set(xlabel='Bin Number')
                
                # Label y-axis
                self.__plot_axes[ax].set(ylabel="Counts")
                
                # Show units only on outer plots
                self.__plot_axes[ax].label_outer()
                
                # Set x-axis range
                self.__plot_axes[ax].set_xlim([0, 150])
                                    
            # Indicate plot has been spawned
            self.__plot_figure_spawned = True
            
        # Plot title with updated capture number
        self.__plot_figure.suptitle("Capture {}".format(self.__current_capture))
        
        # Minimum y-value has to be set differently if logarithmic plotting is enabled
        ymin = 1 if self.plot_logarithmic else 0
            
        # Figure y-limits if fixed
        if self.plot_logarithmic:
            ymax = self.__ymax if self.fix_y_max else np.round(np.amax(self.__capture_data) * 11 + 1)
        else:
            ymax = self.__ymax if self.fix_y_max else np.round(np.amax(self.__capture_data) * 1.1 + 1)
        
        # Update y-limits
        ymin, ymax = self.__plot_axes[0].set_ylim((ymin, ymax))
                        
        # Loop through chips
        for chip in range(self.__number_of_chips):
            
            # Spawn the figure
            if not self.__subplot_spawned[chip]:
                
                # Plot the data on log scale
                if self.plot_logarithmic:
                    
                    # Plot and append to line list
                    self.__plot_line.append(self.__plot_axes[chip].semilogy(range(150), self.__capture_data[chip], color='#00008B', marker='.')[0])
                
                # Plot the data on a linear scale
                else:
                    
                    # Plot and append to line list
                    self.__plot_line.append(self.__plot_axes[chip].plot(range(150), self.__capture_data[chip], color='#00008B', marker='.')[0])
                             
                # Indicate the figure has been spawned
                self.__subplot_spawned[chip] = True
            
            # Update the figure
            else:
                
                # Update the line
                # TODO: Does set_ydata preserve log scale?
                self.__plot_line[chip].set_ydata(self.__capture_data[chip])

            # Find the peak
            if self.show_peak:
                self.__update_peak(chip)

            # Add figure text to indicate the counts
            if self.show_plot_info:
                self.__update_plot_info(chip, ymax)

        # Assemble the legend and handles
        legend = ['Data']
        handles = [self.__plot_line[0]]
        if self.show_peak:
            legend.append('Peak')
            handles.append(self.__peak_point[0])
        
        # Add a legend to the plot
        if not self.__plot_legend_spawned:
            self.__plot_figure.legend(handles, legend, loc='upper right', fontsize='small')
            self.__plot_legend_spawned = True
        
        # Show
        plt.show()
        plt.pause(0.1)
        sleep(0.1)
        
        # Increment the capture count
        self.__current_capture = self.__current_capture + 1
        
        
    # ===========================================================
    # Update plot with chip configuration information and photon count
    # ===========================================================
    def __update_plot_info(self, chip, ymax):
        
        # Add figure text to indicate the counts
        if not self.__plot_info_text_spawned[chip]:
            self.__plot_info_text[chip] = self.__plot_axes[chip].text(  self.__time_limits[1] * .05, ymax * .95, \
                                                                        "Total Counts: " + str(self._total_counts[chip]) + "\n" + \
                                                                        "Subtractor: " + str(self.__subtractor_value) + "\n" + \
                                                                        "Delay Word: " + str(self.__delay_line_word[chip]) + "\n" + \
                                                                        "Coarse: " + str(self.__coarse[chip]) + "\n" + \
                                                                        "Fine: " + str(self.__fine[chip]), \
                                                                        fontsize=8, \
                                                                        verticalalignment='top')
            self.__plot_info_text_spawned[chip] = True
        else:
            self.__plot_info_text[chip].set_text(                       "Total Counts: " + str(self._total_counts[chip]) + "\n" + \
                                                                        "Subtractor: " + str(self.__subtractor_value) + "\n" + \
                                                                        "Delay Word: " + str(self.__delay_line_word[chip]) + "\n" + \
                                                                        "Coarse: " + str(self.__coarse[chip]) + "\n" + \
                                                                        "Fine: " + str(self.__fine[chip]) )
            self.__plot_info_text[chip].set_position([self.__time_limits[1] * .05, ymax * .95])
            
            
    # ===========================================================
    # Update plot with peak point and label
    # ===========================================================
    def __update_peak(self, chip):
        
        # Find the peak index
        peak_index = np.argmax(self.__capture_data[chip])
        
        # Store peak value
        if self.plot_logarithmic:
            peak_value = np.log10(self.__capture_data[chip][peak_index])
        else:
            peak_value = self.__capture_data[chip][peak_index]
        
        # Place text
        if not self.__plot_peak_spawned[chip]:
            
            # Spawn peak point and text
            self.__peak_point[chip] = self.__plot_axes[chip].plot(peak_index, peak_value, 'ro')[0]
            self.__plot_peak_text[chip] = self.__plot_axes[chip].text(peak_index + self.__time_limits[1] * .02, peak_value, "Bin " + str(peak_index))
            self.__plot_peak_spawned[chip] = True
            
        else:
            
            # Replot peak point and text
            self.__peak_point[chip].set_ydata(peak_value)
            self.__plot_peak_text[chip].set_position([peak_index + self.__time_limits[1] * .02, peak_value])
            self.__plot_peak_text[chip].set_text("Bin " + str(peak_index))

    
    # ===========================================================
    # Create a plot of the data
    # ===========================================================
    def __plot(self):
        
        if not self.__plot_figure_spawned:
        
            # Close all figures
            plt.close('all')
            
            # Figure handle
            self.__plot_figure, axes_structure = plt.subplots(self.__subplot_rows, self.__subplot_cols, sharex=True, sharey=True)
            
            # Maximize figure
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            
            # Label graphs
            for ax in range(self.__number_of_chips):
                
                self.__plot_axes[ax] = axes_structure.flat[ax]
                
                # Subplot title
                self.__plot_axes[ax].set_title('Chip ' + str(ax))
                
                # Subplot axis labels
                self.__plot_axes[ax].set(xlabel='Time (ns)')
                
                # Label y-axis depending on logarithmic plotting
                self.__plot_axes[ax].set(ylabel="Counts")
                
                # Show units only on outer plots
                self.__plot_axes[ax].label_outer()
                
                # Set x-axis range
                self.__plot_axes[ax].set_xlim(self.__time_limits)
                                    
            # Indicate plot has been spawned
            self.__plot_figure_spawned = True
            
        # Plot title with updated capture number
        self.__plot_figure.suptitle("Capture {}".format(self.__current_capture))
        
        # Minimum y-value has to be set differently if logarithmic plotting is enabled
        ymin = 1 if self.plot_logarithmic else 0
            
        # Figure y-limits if fixed
        if self.plot_logarithmic:
            ymax = self.__ymax if self.fix_y_max else np.round(np.amax(self.__capture_data) * 11 + 1)
        else:
            ymax = self.__ymax if self.fix_y_max else np.round(np.amax(self.__capture_data) * 1.1 + 1)
        
        # Update y-limits
        ymin, ymax = self.__plot_axes[0].set_ylim((ymin, ymax))
        
        # Create the VCSEL signal
        if self.__vcsel_setting_set:
            vcsel_signal = 0.75 * ymax * (np.heaviside(self.__time_axis - self.__vcsel_latency, 0.5) - np.heaviside(self.__time_axis - self.__vcsel_latency - self.__vcsel_delays[self.__vcsel_setting], 0.5))
                        
        # Loop through chips
        for chip in range(self.__number_of_chips):
            
            # Spawn the figure
            if not self.__subplot_spawned[chip]:
                
                # Plot the data on log scale
                if self.plot_logarithmic:
                    
                    # Plot and append to line list
                    self.__plot_line.append(self.__plot_axes[chip].semilogy(self.__time_array[chip], self.__time_data[chip], color='#00008B', marker='.')[0])
                
                # Plot the data on a linear scale
                else:
                    
                    # Plot and append to line list
                    self.__plot_line.append(self.__plot_axes[chip].plot(self.__time_array[chip], self.__time_data[chip], color='#00008B', marker='.')[0])
                             
                # Indicate the figure has been spawned
                self.__subplot_spawned[chip] = True
            
            # Update the figure
            else:
                
                # Update the line
                # TODO: Does set_ydata preserve log scale?
                self.__plot_line[chip].set_ydata(self.__time_data[chip])
                     
            # Find the peak
            if self.show_peak:
                self.__update_peak(chip)
            
            # If the VCSEL setting has been set, plot it
            if self.__vcsel_setting_set:
                
                # Check if VCSEL signal has already been plotted
                if not self.__vcsel_line_spawned[chip]:
                    
                    # Plot the VCSEL signal
                    self.__vcsel_line[chip] = self.__plot_axes[chip].plot(self.__time_axis, vcsel_signal, color = 'g')[0]
                    
                    self.__vcsel_line_spawned[chip] = True
                    
                else:
                    
                    # Replot VCSEL signal
                    self.__vcsel_line[chip].set_ydata(vcsel_signal)
                    
            # Create and plot the gating signal
            gating_signal = 0.75 * ymax * (np.heaviside(self.__time_axis - self.__gate_delay[chip] - self.__spad_rise_time, 0.5) - np.heaviside(self.__time_axis - self.__gate_delay[chip] - self.__period / 2, 0.5))
            
            # Check if gating signal has already been plotted
            if not self.__gating_line_spawned[chip]:
                
                # Plot the gating signal
                self.__gating_line[chip] = self.__plot_axes[chip].plot(self.__time_axis, gating_signal, color='r')[0]
                self.__gating_line_spawned[chip] = True
                
            else:
                
                # Replot gating signal
                self.__gating_line[chip].set_ydata(gating_signal)
            
            # Add figure text to indicate the counts
            if self.show_plot_info:
                self.__update_plot_info(chip, ymax)

        # Assemble the legend and handles
        legend = ['Data']
        handles = [self.__plot_line[0]]
        if self.show_peak:
            legend.append('Peak')
            handles.append(self.__peak_point[0])
        legend.append('Gating Window')
        handles.append(self.__gating_line[0])
        if self.__vcsel_setting_set:
            legend.append('VCSEL Pulse')
            handles.append(self.__vcsel_line[0])
        
        # Add a legend to the plot
        if not self.__plot_legend_spawned:
            self.__plot_figure.legend(handles, legend, loc='upper right', fontsize='small')
            self.__plot_legend_spawned = True
        
        # Show
        plt.show()
        plt.pause(0.1)
        sleep(0.1)
        
        # Increment the capture count
        self.__current_capture = self.__current_capture + 1
        
        
    # ===========================================================
    # Set coarse and fine values for display on plots
    # ===========================================================
    def set_coarse_fine(self, coarse, fine):
        
        # Check that time_gating_delays has the correct size
        if (len(coarse) != self.__number_of_chips) or (len(fine) != self.__number_of_chips):
            print("Input to set_coarse_fine should have one coarse and one fine value per chip")
            raise Exception
        
        # Loop through chips
        for chip in range(self.__number_of_chips):
            
            # Set the value
            self.__delay_line_word[chip] = (coarse[chip] << 3) + fine[chip]
            self.__coarse[chip] = np.binary_repr(coarse[chip], 4)
            self.__fine[chip] = np.binary_repr(fine[chip], 3)
            
            
    # ===========================================================
    # Set subtractor value
    # ===========================================================
    def set_subtractor_value(self, subtractor_value):
        # Set the value
        self.__subtractor_value = subtractor_value
            
                
    # ===========================================================
    # Set gating delay
    # ===========================================================
    def set_gate_delay(self, time_gating_delays):
        
        # Check that time_gating_delays has the correct size
        if len(time_gating_delays) != self.__number_of_chips:
            print("Input to set_gate_delay should have one delay value per chip")
            raise Exception
        
        # Loop through chips
        for chip in range(self.__number_of_chips):
        
            # Adjust the gate delay to be aligned with current clock cycle
            if (time_gating_delays[chip] + (self.__period / 2) > self.__period):
                self.__gate_delay[chip] = time_gating_delays[chip] - self.__period
            else:
                self.__gate_delay[chip] = time_gating_delays[chip]
    
    
    # ===========================================================
    # Passing the time gate settings for the current frame and the data displays a plot of the current counts
    # ===========================================================
    def update_plot(self, manual_input=None, use_manual_input=False, pattern_to_plot=0):
        
        # Fast mode overrides settings
        if self.fast_mode:
            self.raw_plotting = True
            self.accumulated_plotting = False
            self.show_peak = False
            self.show_plot_info = False
            
        # Fill full capture data structure
        if use_manual_input==False:
            self.__full_capture_data = self.__packet.data.copy()
        else:
            self.__full_capture_data = manual_input.copy()
        
        # Zero out the zeroeth bin
        for chip in range(self.__number_of_chips):
            for frame in range(self.__number_of_frames):
                for pattern in range(self.__patterns_per_frame):
                    self.__full_capture_data[chip][frame][pattern][0] = 0
        
        # Fill capture data structure if not using fast mode
        if not self.fast_mode:
            
            # Fill capture data structure
            for chip in range(self.__number_of_chips):
                if not (chip in self.__muted_chips):
                    self.__capture_data[chip] = self.__full_capture_data[chip][0][pattern_to_plot]
                    
        # Fill the counts structure
        if self.show_plot_info:
            self._total_counts = np.sum(self.__capture_data, axis=1)
            
        # Raw plotting
        if self.raw_plotting:
            
            # Fast mode
            if self.fast_mode:
                
                # Plot quickly
                self.__plot_raw_fast_pattern()
            
            # Non-fast mode
            else:
                
                # Plot detailed
                self.__plot_raw()
             
        # Standard plotting
        else:
            
            # Time the data
            self.__place_data_in_time()
            
            # Plot
            self.__plot()


    # ===========================================================
    # Turn on or off raw plotting
    # ===========================================================
    def set_raw_plotting(self, boolean):
        self.raw_plotting = bool(boolean)
     
        
    # ===========================================================
    # Turn on or off plotted average
    # ===========================================================
    def set_show_peak(self, boolean):
        self.show_peak = bool(boolean)
        
        
    # ===========================================================
    # Turn on or off coarse and fine values
    # ===========================================================
    def set_show_plot_info(self, boolean):
        self.show_plot_info = bool(boolean)
        
        
    # ===========================================================
    # Turn on or off logarithmic plotting
    # ===========================================================
    def set_plot_logarithmic(self, boolean):
        self.plot_logarithmic = bool(boolean)
    
    
    # ===========================================================
    # Turn on or off fixed y-max value
    # ===========================================================
    def set_fix_y_max(self, boolean, ymax):
        self.fix_y_max = bool(boolean)
        self.__ymax = float(ymax)
        
        
    # ===========================================================
    # Turn on or off fast mode
    # ===========================================================
    def set_fast_mode(self, boolean, time=0.5):
        self.fast_mode = bool(boolean)
        self.__fast_mode_time = time
    
    
    # ===========================================================
    # Set the vcsel setting
    # TODO: VCSEL setting should depend on chip that was acting as source during this capture
    # ===========================================================
    def set_vcsel_setting(self, setting):
        
        # Verify that setting is correct
        if (setting < 0) or (setting > 3):
            
            # Default the VCSEL setting to 0
            self.__vcsel_setting = 0
            
            # VCSEL setting becomes unknown
            self.__vcsel_setting_set = False
            
        else:
            
            # Set the VCSEL setting
            self.__vcsel_setting = setting
            
            # VCSEL setting becomes known
            self.__vcsel_setting_set = True
            
    
    # ===========================================================
    # Get the plotted data
    # ===========================================================
    def get_plotted_data(self):

        # Return the data from the plot
        if self.raw_plotting:
            return (np.arange(0, 150),)*self.__number_of_chips, self.__capture_data
        else:
            return self.__time_array, self.__time_data
    

    # ===========================================================
    # Get the shape of the time axis
    # ===========================================================
    def get_time_axis_shape(self):
        
        # Return the shape
        return np.shape(self.__time_axis)
    
    
    # ===========================================================
    # Get the shape of the time axis
    # ===========================================================
    def get_time_array_shape(self):
        
        # Return the shape
        return np.shape(self.__time_array)
    
    
    # ===========================================================
    # Set plots to mute
    # ===========================================================
    def set_muted_chips(self, muted_chips):
    
        # Set the muted plots
        self.__muted_chips = muted_chips
    
    
    # ===========================================================
    # Close the dataplotter and release all figures
    # ===========================================================
    def close(self):
        plt.close(self.__plot_figure)
    
    
    # ===========================================================
    # Main function for separately exporting data or saving figures
    # ===========================================================
    if __name__ == "__main__":
        pass
