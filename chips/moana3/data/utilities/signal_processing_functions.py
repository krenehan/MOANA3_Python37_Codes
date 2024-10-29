# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 10:28:01 2024

@author: Dell-User
"""


import numpy as np
import scipy.signal as sig



def butterlp_filtfilt(data, highcut, fs, order=5, axis=0, filttype='butter'):
    '''Apply a lowpass butter filtfilt to single axis of multidimensional data'''
    
    # Filter coefficients
    if filttype == 'butter':
        sos = sig.butter(order, highcut, fs=fs, output='sos')
    elif filttype == 'bessel':
        sos = sig.bessel(order, highcut, fs=fs, output='sos')
    
    # Copy data
    d = np.copy(data)
    
    # Axis
    if axis < 0:
        axis = data.ndim + axis
    
    if data.ndim > 1:
    
        # Get the new data shape to work with
        d_new_axes = list(range(data.ndim))
        del d_new_axes[axis]
        d_new_axes = d_new_axes + [axis]
        
        # Unmap the indices for transposing back later
        d_old_axes = [np.where(np.array(d_new_axes) == i)[0][0] for i in range(data.ndim)]
        
        # Transpose to move filtering axis to last
        d = np.transpose(d, axes=d_new_axes)
        
        # Reshape to compress all dimensions except last that will be filtered
        d_old_shape = np.shape(d)
        d_new_shape = list(np.shape(d))
        d_new_shape.pop()
        d_new_shape = [np.prod(d_new_shape), np.shape(d)[-1]]
        d = np.reshape(d, d_new_shape)
        
        # Run filter
        for i in range(len(d)):
            d[i] = sig.sosfiltfilt(sos, d[i])
            
        # Revert to original shape and axes order
        d = np.reshape(d, newshape=d_old_shape)
        d = np.transpose(d, axes=d_old_axes)
        
    else:
        
        d = sig.sosfiltfilt(sos, d)
        
    # Return
    return d



# Function to highpass filtfilt with butterworth filter
def butterhp_filtfilt(data, lowcut, fs, order=5, axis=0):
    '''Apply a highpass butter filtfilt to single axis of multidimensional data'''
    
    # Filter coefficients
    sos = sig.butter(order, lowcut, btype='highpass', fs=fs, output='sos')
    
    # Axis
    if axis < 0:
        axis = data.ndim + axis
    
    # Copy data
    d = np.copy(data)
    
    if data.ndim > 1:
    
        # Get the new data shape to work with
        d_new_axes = list(range(data.ndim))
        del d_new_axes[axis]
        d_new_axes = d_new_axes + [axis]
        
        # Unmap the indices for transposing back later
        d_old_axes = [np.where(np.array(d_new_axes) == i)[0][0] for i in range(data.ndim)]
        
        # Transpose to move filtering axis to last
        d = np.transpose(d, axes=d_new_axes)
        
        # Reshape to compress all dimensions except last that will be filtered
        d_old_shape = np.shape(d)
        d_new_shape = list(np.shape(d))
        d_new_shape.pop()
        d_new_shape = [np.prod(d_new_shape), np.shape(d)[-1]]
        d = np.reshape(d, d_new_shape)
        
        # Run filter
        for i in range(len(d)):
            d[i] = sig.sosfiltfilt(sos, d[i])
            
        # Revert to original shape and axes order
        d = np.reshape(d, newshape=d_old_shape)
        d = np.transpose(d, axes=d_old_axes)
        
    else:
        
        d = sig.sosfiltfilt(sos, d)
        
    # Return
    return d



# Function to notch specific frequencies
def notch_filtfilt(data, notch_freq, quality_factor, fs, axis=0):
    '''Apply a notch filtfilt to single axis of multidimensional data'''
    
    # Create filter
    b, a = sig.iirnotch(notch_freq, quality_factor, fs=fs)
    
    # Axis
    if axis < 0:
        axis = data.ndim + axis
    
    # Copy data
    d = np.copy(data)
    
    if data.ndim > 1:
    
        # Get the new data shape to work with
        d_new_axes = list(range(data.ndim))
        del d_new_axes[axis]
        d_new_axes = d_new_axes + [axis]
        
        # Unmap the indices for transposing back later
        d_old_axes = [np.where(np.array(d_new_axes) == i)[0][0] for i in range(data.ndim)]
        
        # Transpose to move filtering axis to last
        d = np.transpose(d, axes=d_new_axes)
        
        # Reshape to compress all dimensions except last that will be filtered
        d_old_shape = np.shape(d)
        d_new_shape = list(np.shape(d))
        d_new_shape.pop()
        d_new_shape = [np.prod(d_new_shape), np.shape(d)[-1]]
        d = np.reshape(d, d_new_shape)
        
        # Run filter
        for i in range(len(d)):
            d[i] = sig.filtfilt(b, a, d[i])
            
        # Revert to original shape and axes order
        d = np.reshape(d, newshape=d_old_shape)
        d = np.transpose(d, axes=d_old_axes)
        
    else:
        
        d = sig.filtfilt(b, a, d) 
        
    # Return
    return d


def decimate(data, ratio, axis=0):
    '''Decimate along a single dimension of multi-dimensional data'''
    
    # Copy data for safety and because I don't care about speed
    d = data.copy()
    
    # Collect the length of the axis to be decimated and create integer number of samples along this axis that is divisible by the ratio
    d_ax_len = np.shape(d)[axis]
    new_size = int(np.floor(d_ax_len / ratio))
    
    # Take this number of samples from the axis to be decimated
    d = np.take(d, indices=np.arange(0, new_size*ratio), axis=axis)
    
    # Find the new shape of the data for reshaping purposes
    new_shape = list(np.shape(d))
    new_shape.pop(axis)
    new_shape.insert(axis, ratio)
    new_shape.insert(axis, new_size)
    d = np.reshape(d, newshape=new_shape)
    
    # Decimate
    d = np.mean(d, axis=axis+1)
    
    # Return
    return d


def detrend(data, axis=0, type='linear'):
    ''' Detrend data along axis'''
    
    # Passthrough
    return sig.detrend(data, axis=axis, type=type)



def block_average(t, stim_onset, data, t_prior=2, t_after=20, axis=0, return_std=False):
    ''' Block average a single dimension of multidimensional data within a specified time window '''
    
    # Axis
    if axis < 0:
        axis = data.ndim + axis

    # Create a time axis for the block averages
    tstep = t[1] - t[0]
    tbi = int(t_prior / tstep)
    tba = int(t_after / tstep)
    t_axis = np.arange(tbi + tba) * tstep - tbi*tstep
    
    # Timestamps for t_prior before each onset
    t_idcs_before = np.where(np.isclose(stim_onset, 1))[0] - tbi
    
    # Timestamps for t_after after each onset
    t_idcs_after = np.where(np.isclose(stim_onset, 1))[0] + tba

    # Create an array of data windowed around each onset
    segmented_data = np.array([np.take(data, np.arange(t_idcs_before[i], t_idcs_after[i]), axis=axis) for i in range(len(t_idcs_before))])
    
    # Get standard deviation if requested
    if return_std:
        std = np.std(segmented_data, axis=0)
    
    # Average windows
    segmented_data = np.mean(segmented_data, axis=0)
    
    # Find the baseline
    baseline = np.take(segmented_data, np.arange(tbi), axis=axis)
    baseline = np.mean(baseline, axis=axis, keepdims=True)
    
    # Old axes and new axes for transpose and reverse
    new_axes = list(np.arange(baseline.ndim))
    new_axes.pop(axis)
    new_axes = [axis] + new_axes
    old_axes = [np.where(np.array(new_axes) == i)[0][0] for i in range(baseline.ndim)]
    
    # Transpose the baseline, replicate the mean value, remove redundant axis and transpose back
    baseline = np.transpose(baseline, axes=new_axes)
    baseline = np.array([baseline for i in range(segmented_data.shape[axis])])
    baseline = np.mean(baseline, axis=1)
    baseline = np.transpose(baseline, axes=old_axes)
    
    # Subtract the baseline
    segmented_data = segmented_data  - baseline
    
    # Return
    if return_std:
        return t_axis, segmented_data, std
    else:
        return t_axis, segmented_data


def mean_time(t, data, axis=-1):
    '''Calculate mean time of single dimension from multi-dimensional data'''
    
    # Copy data
    d = np.copy(data)

    # Replicate data structure
    t_rep = np.repeat(t, repeats=len(d.flat)//len(t))
    t_rep = np.reshape(t_rep, (len(t), len(d.flat)//len(t)))
    t_rep = np.transpose(t_rep).flat
    t_rep = np.reshape(t_rep, newshape=np.shape(d))
    
    # Calculate the mean time for background and roi
    mt_s = list(np.shape(d))
    mt_s.pop(axis)
    mt = np.zeros(mt_s)
    mt = np.divide(np.sum(np.multiply(t_rep, d), axis=axis), np.sum(d, axis=axis), where=np.sum(d, axis=axis)>0, out=mt)
    
    # Return
    return mt


def laplace(t, data, normalize=True, Ls=-1e-4, axis=-1):
    '''Calculate laplace of single dimension from multi-dimensional data'''
    
    # Copy data
    d = np.copy(data)

    # Replicate data structure
    t_rep = np.repeat(t, repeats=len(d.flat)//len(t))
    t_rep = np.reshape(t_rep, (len(t), len(d.flat)//len(t)))
    t_rep = np.transpose(t_rep).flat
    t_rep = np.reshape(t_rep, newshape=np.shape(d))

    # Convert to ps
    t_rep_ps = t_rep * 1e12
    
    # Calculate Laplace
    L = np.trapz(np.exp(Ls*t_rep_ps)*data, t_rep_ps, axis=axis)
    if normalize:
        L_norm = np.zeros_like(L)
        L_norm = np.divide(L, np.sum(data, axis=axis), where=np.sum(data, axis=axis)>0, out=L_norm)
    
    # Return
    if normalize:
        return L_norm
    else:
        return L
    
    
def od(cw_data, exp_t_axis=0, add_dc_offset=True):
    '''Calculate optical density (OD)'''
    
    # Copy data
    d = np.copy(cw_data)
    
    # Check that cw_data does not include negative values
    if np.nanmin(d) < 0:
        print("Warning: cw_data includes negative values")
    
        # Additional warnings
        if add_dc_offset:
            print("Adding dc offset to data before OD conversion")
        else:
            raise Exception("Cannot convert to OD with negative CW values")
            
    # Correct
    if add_dc_offset:
        d = d + np.nanmin(d) + 1
    
    # Find mean of data
    d_m = np.repeat(np.nanmean(np.abs(d), axis=exp_t_axis, keepdims=True), repeats=np.shape(cw_data)[exp_t_axis], axis=exp_t_axis)

    # Calculate the OD
    # This is based on Homer2's hmrIntensity2OD function
    od = -np.log(np.abs(d)/d_m)

    # Return
    return od


# def mt_od(t, data, exp_t_axis=0, hist_axis=-1):
#     '''Calculate mean time of single dimension from multi-dimensional data'''

#     # Calculate the cw and the mean time
#     cw = np.sum(data, axis=hist_axis)
    
#     # Calculate the mean of the CW trace for each S/D/W combination
#     cw_mean = np.mean(cw, axis=exp_t_axis)
#     cw_mean = np.reshape(cw_mean, newshape=(1,)+np.shape(cw_mean))
#     cw_mean = np.repeat(cw_mean, repeats=np.shape(cw)[exp_t_axis], axis=0)
    
#     # Transpose back to original
#     new_axes = list(np.arange(cw_mean.ndim)[1:])
#     new_axes.insert(exp_t_axis, 0)
#     cw_mean = np.transpose(cw_mean, axes=new_axes)
    
#     # Calculate R
#     R = np.zeros_like(cw, dtype=float)
#     R = np.divide(cw, R, where=R>0, out=R)
    
#     # Speed of light term
#     n = 1.4
#     c = 299792458
    
#     # Return
#     return mt
















