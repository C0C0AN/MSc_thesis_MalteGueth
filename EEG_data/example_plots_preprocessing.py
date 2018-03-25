"""
Created on Sun Mar 25 15:41:40 2018

@author: Malte R. Gueth
"""

# Create examplery plots for demonstrating the use of ICA-based rejection of BCG artefact components
# for EEG pre-processing of simultaneously recorded data

import mne
import mne.io.eeglab

from mne.preprocessing import ICA
from mne.preprocessing import create_ecg_epochs
from mne.preprocessing.ica import corrmap

from matplotlib.backends.backend_pdf import PdfPages 

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
info_custom['description'] = 'Simultaneously_recorded_data_with_customized_info_file'

data_path = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/GradCorrected/fMRICorrected_Short_0521.set'

# Read the raw EEG data that has been corrected for everything besides BCG artefacts
raw = mne.io.read_raw_eeglab(data_path, montage=montage, event_id=None, 
                             event_id_func='strip_to_integer', preload=True, 
                             verbose=None, uint16_codec=None) 

# Replace the mne info structure with the customised one
# that has the corect labels, channel types and positions
raw.info = info_custom

raw.save('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/GradCorrected/Sub1_preprocessed_raw.fif.gz') 

# Specify channel selections   
picks_eeg = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, ecg=False,
                       stim=False)
picks_ecg = mne.pick_types(raw.info, meg=False, eeg=False, eog=False, ecg=True,
                       stim=False) 

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
# to avoid the distortion of ica components by large artifacts
reject_eeg = dict(eeg=100e-6)
reject_ecg = dict(ecg=2000e-6)

# Create ICA object
ica = ICA(n_components=n_components, method=method) 
# Fit ICA on raw data
ica.fit(raw, picks=picks_eeg, decim=decim, reject=None) 

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
fig1 = ica.plot_scores(scores, title='ICA component scores subject 10',
                    exclude=[5,10,17,18,24], 
                    show=True, 
                    axhline=0.5)

# To improve your selection, inspect the ica components' 
# source signal time course and compare it to the average ecg artifact 
fig2 = ica.plot_sources(ecg_average, exclude=ecg_inds)  

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

for i in range(1, 14):
     data_path2 = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Sub%d-ica.fif.gz' % (i)
     current_ica = mne.preprocessing.read_ica(data_path2)
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

pp=PdfPages('fig.pdf')
pp.savefig(fig)
pp.close()
