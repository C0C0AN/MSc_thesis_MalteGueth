"""
Created on Wed Oct 25 06:07:15 2017

@author: Malte R. Güth
"""
import mne
import mne.io.eeglab

import glob
import os

from mne.preprocessing import ICA
from mne.preprocessing import create_ecg_epochs
from mne.preprocessing.ica import corrmap 

# Build the digital montage of your eeg system
# It's also possible to specifiy a path to a montage file
# with ‘.elc’, ‘.txt’, ‘.csd’, ‘.elp’, ‘.hpts’, ‘.sfp’, ‘.loc’ 
# (‘.locs’ and ‘.eloc’) or .bvef as supported data formats.

# This step is not necessary for everything to work, 
# but serves the documentation of system details.

montage = mne.channels.read_montage(kind='standard_1005')

path = './EEG/GradCorrected/'

# Start a for loop for basic pre-processing (filter, resampling, rereferencing, ICA)
# with each iteration representing a data set in the path where you stored the raw data. Note that
# each data set has been previously cut to the length of the actual experiment
# and has been corrected for gradient artefacts in eeglab with the Bergen toolbox 
# (http://fmri.uib.no/tools/bergen_plugin.htm). For this reason, data sets have to be imported
# with 'read_raw_eeglab' and have been saved as raw '.set' files.
for file in glob.glob(os.path.join(path, '*.set')):
  
    filepath, filename = os.path.split(file)
    filename, ext = os.path.splitext(filename)
   
    # Read the raw EEG data that has been corrected for gradient artifacts
    raw = mne.io.read_raw_eeglab(file, montage=montage, event_id=None, 
                                 event_id_func='strip_to_integer', preload=True)
    
    # Specify channel selections   
    picks_eeg = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, ecg=False,
                           stim=False)
    picks_ecg = mne.pick_types(raw.info, meg=False, eeg=False, eog=False, ecg=True,
                           stim=False) 
    picks_all = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, ecg=True,
                           stim=False) 
    
    # Apply a band-pass filter with 0.5 Hz as lower cut-off and 30 Hz 
    # as higher cut-off, n_jobs as amount of parallel jobs to run (default = 1),
    # and fir_design as specification of your finite impulse response filter
    # Apply a second band-pass filter only to the ECG channel
    raw.filter(0.1, 30, fir_design='firwin', picks=picks_eeg) 
    raw.filter(1, 20, ir_design='firwin', picks=picks_ecg) 
    
    # Specify the offline reference for your data with TP9 and TP10 
    # as mastoid reference
    raw.set_eeg_reference(ref_channels=['TP9','TP10']) 
    
    # Resample the data from 5 kHz to 250 Hz. Please mind that for optimal results 
    # the data should be kept at the original sampling rate of 5 kHz when fitting 
    # the ICA. When running tests or example data, you can resample to 250 Hz to make 
    # the ICA run a lot faster. Otherwise, plan in some time for the ICA to run.
    raw.resample(250) 
    
    # Save raw data with same naming convention as above
    # with the addition of _preprocessed_raw.fif.gz
    raw.save('./DPX_EEG_fMRI/EEG/ + filename + '-raw.fif.gz') 
    
    # Specifiy ICA arguments
    # Specify the number of components for the ICA 
    # with decreasing explained variance of PCA
    n_components = 35  
    # Specify the ICA algorithm. Again, for tests you can run the quicker algorithm 'fastica'.
    method = 'extended-infomax'
    # decim argument specifies the increment for selecting each nth time slice
    # If None, all samples within start and stop are used
    # Higher decimation decreases statistics accuracy, but saves time
    decim = None
    # If required, specify data rejection parameters with reject argument 
    # to avoid the distortion of ica components by large artifacts
    reject_eeg = dict(eeg=600e-6)
    reject_ecg = dict(ecg=2000e-6)
    
    # Create ICA object
    ica = ICA(n_components=n_components, method=method) 
    # Fit ICA on raw data
    ica.fit(raw, picks=picks_all, decim=decim, reject=None) 
    # Save ICA object
    ica.save('./DPX_EEG_fMRI/EEG/ICA/ + filename + '-ica.fif.gz') 
    
    
# Look at topomaps for all n components of a subject
ica.plot_components() 
# Plot specific properties (i.e. spectrum, activity image, etc)
# of a component with picks argument as component number
ica.plot_properties(raw, picks=0, psd_args={'fmax': 30.}) 

# Create ECG epochs around likely artifact events and average them 
# excluding data sections which represent large outliers
# Rejection parameters are based on peak-to-peak amplitude
ecg_average = create_ecg_epochs(raw, reject=None).average()

# Create ECG epochs around likely artifact events and correlate them
# to all ICA component source signal time course
# Build artifact scores via the correlation anaylsis
ecg_epochs = create_ecg_epochs(raw, reject=None)
ecg_inds, scores = ica.find_bads_ecg(ecg_epochs)

# Plot the artifact scores / correlations across ICA components
# and retrieve component numbers of sources likely representing
# caridoballistic artifacts
ica.plot_scores(scores, exclude=ecg_inds)

# To improve your selection, inspect the ica components' 
# source signal time course and compare it to the average ecg artifact 
ica.plot_sources(ecg_average, exclude=ecg_inds)  

# If no fruther artifact rejection improvement is required, use the ica.apply
# for ica components to be zeroed out and removed from the signal
# Enter an array of bad indices in exclude to remove components
# start and end arguments mark the first and last sample of the set to be
# affected by the removal

ica.apply(raw, exclude=None, start=None, end=None)
    
  
    
# Choose a subject with a suitable reference ica (must contain representative
# cardioballistic artifact components)
# Build a reference ica and a list of all remaining icas from other subjects
# Loop through all the remaining subejcts to load them in and append in the list
reference_ica = ica
icas_remaining_subjects = list()

path_ica = path + '/ICA'
for file in glob.glob(os.path.join(path_ica, '*.set')):
  
    filepath, filename = os.path.split(file)
    filename, ext = os.path.splitext(filename)
             
    current_ica = mne.preprocessing.read_ica(file)
    icas_remaining_subjects.append(current_ica)

all_icas = [reference_ica] + icas_remaining_subjects

# Build a tuple with the reference ica and the index of the representative
# component
cardio_template = (0, ecg_inds[0])
    
# Run the corrmap algorithm to compare the artifact template to all other 
# components from the remaining subjects
# Find all components that correlate to the template
fig_template, fig_detected = corrmap(all_icas, template=cardio_template, 
                                     label="cardio", show=True, threshold=None,
                                     ch_type='eeg')
ica.exclude.extend(ecg_inds)
