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

# Specify channel selections   
picks_eeg = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, ecg=False,
                       stim=False)
picks_ecg = mne.pick_types(raw.info, meg=False, eeg=False, eog=False, ecg=True,
                       stim=False) 

raw.filter(0.5, 30., n_jobs=1, fir_design='firwin', picks=picks_eeg) 
raw.filter(1, 20., n_jobs=1, fir_design='firwin', picks=picks_ecg) 

# Specify the offline reference for your data with TP9 and TP10 
# as mastoid reference
raw.set_eeg_reference(ref_channels=['TP9','TP10']) 

# Resample the data from 5 kHz to 250 Hz
raw.resample(250, npad="auto") 

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
reject_eeg = dict(eeg=1000e-6)
reject_ecg = dict(ecg=2000e-6)

# Create ICA object
ica = ICA(n_components=n_components, method=method) 
# Fit ICA on raw data
ica.fit(raw, picks=picks_eeg, decim=decim, reject=reject_eeg) 

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
                    exclude=[0,1,3,5,6,7,10,11,12,14], 
                    show=True, 
                    axhline=0.5)

# To improve your selection, inspect the ica components' 
# source signal time course and compare it to the average ecg artifact 
fig2 = ica.plot_sources(ecg_average, exclude=[0,1,3,5,6,7,10,11,12,14])  

pp=PdfPages('sub10.pdf')
pp.savefig(fig1)
pp.savefig(fig2)
pp.close()
