"""
Created on Wed Oct 25 06:07:15 2017

@author: Malte R. Güth
"""
# First attempt at transferring the first half of EEG preprocessing from matlab to mne python

import mne
import mne.io.eeglab

from mne.preprocessing import ICA
from mne.preprocessing import create_ecg_epochs
from mne.preprocessing.ica import corrmap 

# Build the digital montage of your eeg system
# It's also possible to specifiy a path to a montage file
# with ‘.elc’, ‘.txt’, ‘.csd’, ‘.elp’, ‘.hpts’, ‘.sfp’, ‘.loc’ 
# (‘.locs’ and ‘.eloc’) or .bvef as supported data formats

montage = mne.channels.read_montage(kind='standard_1005')
s_freq = 5000
chanlabels = ['Fp1',	'Fp2',	'F3',	'F4',	'C3',	'C4',	'P3',	'P4',	
              'O1',	'O2',	'F7',	'F8',	'T7',	'T8',	'P7',	'P8',	
              'Fz',	'Cz',	'Pz',	'Oz',	'FC1',	'FC2',	'CP1',	'CP2',	
              'FC5',	'FC6',	'CP5',	'CP6',	'TP9',	'TP10', 'POz', 'ECG']
ch_types = ['eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
            'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
            'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
            'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg', 'eeg', 'ecg']
montage = mne.channels.read_montage(kind='standard_1005')
info_custom = mne.create_info(chanlabels, s_freq, ch_types, montage=montage)
info_custom['description'] = 'Simultaneously recorded data with customised info file'

# Start a for loop for basic preprocessing (filter, resampling, rereferencing, ICA)
# with each iteration of x added to your data path indicating the subject
for x in range(1, 14):
    
    # Each time the loop goes through a new iteration, 
    # add a subject integer to the data path
    data_path = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/GradCorrected/Sub%d.set' % (x) 
    
    # Read the raw EEG data that has been corrected for gradient artefacts
    raw = mne.io.read_raw_eeglab(data_path, montage=montage, event_id=None, 
                               event_id_func='strip_to_integer', preload=True, 
                               verbose=None, uint16_codec=None) 
    
    # Replace the mne info structure with the customised one
    # that has the corect labels, channel types and positions
    raw.info = info_custom
    
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
    raw.filter(0.5, 30., n_jobs=1, fir_design='firwin', picks=picks_eeg) 
    raw.filter(1, 20., n_jobs=1, fir_design='firwin', picks=picks_ecg) 
    
    # Specify the offline reference for your data with TP9 and TP10 
    # as mastoid reference
    raw.set_eeg_reference(ref_channels=['TP9','TP10']) 
    
    # Resample the data from 5 kHz to 250 Hz
    raw.resample(250, npad="auto") 
    
    # Save raw data with same naming convention as above
    # with the addition of _preprocessed_raw.fif.gz
    raw.save('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Sub%d_preprocessed_raw.fif.gz' % (x)) 
    
    # Specifiy ICA arguments
    # Specify the number of components for the ICA 
    # with decreasing explained variance of PCA
    n_components = 25  
    # Specify the ICA algorithm 
    method = 'extended-infomax'
    # decim argument specifies the increment for selecting each nth time slice
    # If None, all samples within start and stop are used
    # Higher decimation decreases statistics accuracy, but saves time
    decim = 3 
    # Specify data rejection parameters with reject argument 
    # to avoid the distortion of ica components by large artefacts
    reject_eeg = dict(eeg=600e-6)
    reject_ecg = dict(ecg=2000e-6)
    
    # Create ICA object
    ica = ICA(n_components=n_components, method=method) 
    # Fit ICA on raw data
    ica.fit(raw, picks=picks_eeg, decim=decim, reject=None) 
    # Save ICA object
    ica.save('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Sub%d-ica.fif.gz' % (x)) 
    # Look at topomaps for all n components
    ica.plot_components() 
    # Plot specific properties (i.e. spectrum, activity image, etc)
    # of a component with picks argument as component number
    ica.plot_properties(raw, picks=0, psd_args={'fmax': 30.}) 
    
    # Create ECG epochs around likely artefact events and average them 
    # excluding data sections which represent large outliers
    # Rejection parameters are based on peak-to-peak amplitude
    ecg_average = create_ecg_epochs(raw, reject=None).average()
    
    # Create ECG epochs around likely artefact events and correlate them
    # to all ICA component source signal time course
    # Build artefact scores via the correlation anaylsis
    ecg_epochs = create_ecg_epochs(raw, reject=None)
    ecg_inds, scores = ica.find_bads_ecg(ecg_epochs)
    
    # Plot the artefact scores / correlations across ICA components
    # and retrieve component numbers of sources likely representing
    # caridoballistic artefacts
    ica.plot_scores(scores, exclude=ecg_inds)
    
    # To improve your selection, inspect the ica components' 
    # source signal time course and compare it to the average ecg artefact 
    ica.plot_sources(ecg_average, exclude=ecg_inds)  
    
    # If no fruther artefact rejection improvement is required, use the ica.apply
    # for ica components to be zeroed out and removed from the source signal in the raw EEG data
    # Enter an array of bad indices in exclude to remove components
    # start and end arguments mark the first and last sample of the set to be affected by the removal
    # Alternitavely, use the attribute ica.exclude
    
    ica.apply(raw, exclude=None, start=None, end=None)
        
# Choose a subject with a suitable reference ica (must contain representative
# cardioballistic artefact components)
# Build a reference ica and a list of all remaining icas from other subjects
# Loop through all the remaining subejcts to load them in and append in the list
reference_ica = ica
icas_remaining_subjects = list()

for i in range(1, 14):
     data_path2 = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Sub%d-ica.fif.gz' % (i)
     current_ica = mne.preprocessing.read_ica(data_path2)
     icas_remaining_subjects.append(current_ica)

all_icas = [reference_ica] + icas_remaining_subjects

# Build a tuple with the reference ica and the index of the representative
# component
cardio_template = (0, ecg_inds[0])
    
# Run the corrmap algorithm to compare the artefact template to all other 
# components from the remaining subjects
# Find all components that correlate to the template
fig_template, fig_detected = corrmap(all_icas, template=cardio_template, 
                                     label="cardio", show=True, threshold=None,
                                     ch_type='eeg')
ica.exclude.extend(ecg_inds)
