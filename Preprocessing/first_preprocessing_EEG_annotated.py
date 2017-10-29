"""
Created on Wed Oct 25 06:07:15 2017

@author: Malte R. Güth
"""
# First attempt at transferring the first half of EEG preprocessing from matlab to mne python

import mne
import mne.io.eeglab

from mne.preprocessing import ICA

# Build the digital montage of your eeg system
# It's also possible to specifiy a path to a montage file
# with ‘.elc’, ‘.txt’, ‘.csd’, ‘.elp’, ‘.hpts’, ‘.sfp’, ‘.loc’ 
# (‘.locs’ and ‘.eloc’) or .bvef as supported data formats
montage = mne.channels.read_montage(kind='standard_1005')

# Start a for loop for basic preprocessing (filter, resampling, rereferencing, ICA)
# with each iteration of x added to your data path indicating the subject
for x in range(1, 14):
    data_path = 'G:\\DPX_EEG_fMRI\\EEG\\GradCorrected\\Sub%d.set' % (x) # Each time the loop goes through a new iteration, 
                                                                        # add a subject integer to the data path
    raw = mne.io.read_raw_eeglab(data_path, montage=montage, event_id=None, 
                               event_id_func='strip_to_integer', preload=True, 
                               verbose=None, uint16_codec=None) # Read the raw EEG data
                                                                # that has been corrected for gradient artifacts
    raw.filter(0.5, 30., n_jobs=1, fir_design='firwin') # Apply a band-pass filter with 0.5 Hz as lower cut-off 
                                                        # and 30 Hz as higher cut-off,
                                                        # n_jobs as amount of parallel jobs to run (default = 1),
                                                        # and fir_design as specification of your finite impulse response filter
    raw.set_eeg_reference(ref_channels=['TP9','TP10']) # Specify the offline reference for your data
                                                        # with TP9 and TP10 as mastoid reference
    raw.resample(250, npad="auto") # Resample the data from 5 kHz to 250 Hz
    picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, ecg=True,
                           stim=False)  # Specify channel types
    raw.save('G:\\DPX_EEG_fMRI\\EEG\\Sub%d_preprocessed_raw.fif.gz' % (x)) # Save raw data with same naming convention as above
                                                                            # with the addition of _preprocessed_raw.fif.gz
    # Specifiy ICA arguments
    n_components = 35  # Specify the number of components for the ICA 
                        # with decreasing explained variance of PCA
    method = 'extended-infomax'  # Specify the ICA algorithm 
    decim = 3  # decim argument specifies the increment for selecting each nth time slice
                # If None, all samples within start and stop are used
                # Higher decimation decreases statistics accuracy, but saves time
    # Additionally, specify data rejection parameters with reject argument 
    # to avoid the distortion of ica components by large artifacts
    ica = ICA(n_components=n_components, method=method) # Create ICA object
    ica.fit(raw, picks=None, decim=decim, reject=None) # Fit ICA on raw data
    ica.save('G:\\DPX_EEG_fMRI\\EEG\\Sub%d-ica.fif.gz' % (x)) # Save ICA object
    ica.plot_components() # Look at topomaps for all n components
    ica.plot_properties(raw, picks=0, psd_args={'fmax': 30.}) # Plot specific properties (i.e. spectrum, activity image, etc)
                                                                # of a component with picks argument as component number
