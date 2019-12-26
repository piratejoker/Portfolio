#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:12:16 2019

@author: mason
"""

import scipy.signal as ss
from scipy.io import wavfile
import numpy as np


def calculate_spectrogram(sound):
    """ Uses the file data and windows to calculate local periodograms

    Parameters
    ----------
    file : class ReadData
        the file we calculate window centers on
    windows : a vector
        window centers from Sound class defaults or user

    Returns
    -------
    matrix
        periodograms for each window as a matrix, with rows varying across
        window, and columns across frequency
    """
    sgram = ss.spectrogram(sound.data, fs = sound.framerate, 
                           window = 'blackman')
    return sgram


def calculate_signatures(spectrogram, songid = ''):
    """Calculates the signature of a spectrogram

    Parameters
    ----------
    periodogram_mat : a matrix
        periodograms for each window as a matrix, with rows varying across
        window, and columns across frequency

    Returns
    -------
    matrix
        signatures derived from the spectrogram, can be used as a
        easily hashable signature
    """
    frequencies = spectrogram[0]
    times = spectrogram[1]
    sgram = spectrogram[2]

    time_step = 25
    time_ranges = np.arange(0, len(times), time_step)

    freq_ranges = np.array([11, 22, 44, 88, 177, 355, 710, 1420, 2840, 
                            5680, 11360, 22720])
    nn = len(freq_ranges)
    bin_index = np.zeros(len(frequencies))
    for ii,_ in enumerate(frequencies):
        freq = frequencies[ii]
        bin_index[ii] = nn - sum(freq < freq_ranges)
    sigs = np.zeros((len(time_ranges)-1, len(freq_ranges)-1, 2))
    for ii in range(0, len(time_ranges)-1):
        left_time_index = time_ranges[ii]
        right_time_index = time_ranges[ii + 1]

        time_window = sgram[:, left_time_index:right_time_index]

        for jj in range(0, len(freq_ranges)-1):
            lower_freq_index = len(bin_index) - sum(bin_index >= jj)
            higher_freq_index = len(bin_index) - sum(bin_index > jj)
            if lower_freq_index == higher_freq_index:
                sigs[ii,jj] = 0
            else:
                window = time_window[lower_freq_index:higher_freq_index, :]
                index = np.argmax(window)
                time_index = index % len(window[0])
                freq_index = index // len(window[0])

                sigs[ii, jj] = lower_freq_index + freq_index

    # the ISMIR Paper does not specify how anchor points are chosen 
    # It LOOKS like they use each point as an anchor point, and reduce the
    # target zone rather than number of anchor points. I've
    # elected an alternate method, using simply the next three points
    # temporally
    sigs_dict = {}
    for sig_set in sigs:
        sigs_dict[tuple(sig_set.flatten())] = songid
    
    return sigs, sigs_dict
