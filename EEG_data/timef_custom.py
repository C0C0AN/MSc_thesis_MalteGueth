"""
Created on Sat Jun 16 21:14:04 2018
@author: Malte
"""

# A custom code for time frequency analysis originally written in Matlab, adapted for python and R 
# by Jose Alanis (https://github.com/JoseAlanis) and me.

import mne
import numpy as np
import math

import glob
import os

elec=65

def nextpow2(n):
    m_f = np.log2(n)
    m_i = np.ceil(m_f)
    return int(np.log2(2**m_i))

output_dir = 'your output directory for time-frequency results'
data_path = 'your path to all your epoched files' 

for epochs in glob.glob(os.path.join(data_path, '*.fif')):

    EEG = mne.read_epochs(epochs)

    for E in range(1,elec):
        
        tmin=min(EEG.times)
        tmax=max(EEG.times)
        
        min_frex =  1
        max_frex = 30
        num_frex = 30
        
        time = np.arange(-1, 1.0001, 1/EEG.info['sfreq'])
        pnts = int(EEG.info['sfreq']*(tmax+(tmin*-1))+1)
        frex = np.logspace(np.log10(min_frex), np.log10(max_frex), num_frex)
        cycles = np.logspace(np.log10(3), np.log10(10), num_frex)/(2*np.pi*frex)
        
        n_wavelet            = time.size
        n_data               = pnts*len(EEG)
        n_convolution        = n_wavelet+n_data-1
        n_conv_pow2          = int(math.pow(2,nextpow2(n_convolution)))
        half_of_wavelet_size = (n_wavelet-1)/2
        
        data = EEG.get_data()
        eegfft = np.fft.fft(np.reshape(data[:,E,:], (1, int(pnts*len(EEG)))), n_conv_pow2)
        
        timef = np.zeros((num_frex,pnts,int(len(EEG))))
        
        baseidx = EEG.time_as_index((-1.7, -0.3))
        
        for fi in range(1,num_frex):
            
            w = math.sqrt(1/(cycles[fi]*math.sqrt(np.pi))) * np.exp(np.multiply(2*1j*np.pi*frex[fi], time))
            wavelet = np.fft.fft(np.multiply(w, np.exp(-time**2./(2*(cycles[fi]**2)))), n_conv_pow2 )
            
            eegconv = np.fft.ifft(wavelet*eegfft)
            eegconv = eegconv[0:n_convolution]
            eegconv = eegconv[int(half_of_wavelet_size+1):int(eegconv.size-half_of_wavelet_size)]

            temppower = np.mean(abs(np.reshape(eegconv, (pnts,len(EEG))))**2,2)
            timef[fi,:] = 10*np.log10(temppower/np.mean(temppower[baseidx[1]:baseidx[2]]))

        filepath, filename = os.path.split(epochs)
        np.savetxt(output_dir + filename + '_timef.csv', timef)
