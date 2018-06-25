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

from matplotlib.backends.backend_pdf import PdfPages 

path = './DPX_EEG_fMRI/EEG/'

# Choose a subject with a suitable reference ica (must contain representative
# cardioballistic artifact components)
ica = mne.preprocessing.read_ica(path + '/ICA/my-ica.fif.gz')
raw = mne.io.read_raw_fif(path + 'my-raw.fif.gz')

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

pp=PdfPages('sub_10_ica_scores.pdf')
pp.savefig(fig1)
pp.savefig(fig2)
pp.close()
