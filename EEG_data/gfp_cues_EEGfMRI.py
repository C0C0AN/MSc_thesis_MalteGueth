"""
Created on Sat Dec 09 15:44:55 2017

@author: Malte R. Güth
"""

import mne

import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Build the digital montage of your eeg system
# It's also possible to specifiy a path to a montage file
# with ‘.elc’, ‘.txt’, ‘.csd’, ‘.elp’, ‘.hpts’, ‘.sfp’, ‘.loc’ 
# (‘.locs’ and ‘.eloc’) or .bvef as supported data formats

montage = mne.channels.read_montage(kind='standard_1005')
s_freq = 250
chanlabels = ['Fp1',	'Fp2',	'F3',	'F4',	'C3',	'C4',	'P3',	'P4',	
              'O1',	'O2',	'F7',	'F8',	'T7',	'T8',	'P7',	'P8',	
              'Fz',	'Cz',	'Pz',	'Oz',	'FC1',	'FC2',	'CP1',	'CP2',	
              'FC5',	'FC6',	'CP5',	'CP6',	'TP9',	'TP10', 'POz']
ch_types = ['eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
            'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
            'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
            'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg', 'eeg']
montage = mne.channels.read_montage(kind='standard_1005')
info_custom = mne.create_info(chanlabels, s_freq, ch_types, montage=montage)
info_custom['description'] = 'Simultaneously recorded data with customized info file'

# Create ERPs with Global Field Power (GFP) for preprocessed EEG data (see Preprocessing folder)
# and save the plots as pdf. Load single subject evoked data and create lists for all epochs (i.e. Cue A and B).

listA = [evoked1_A, evoked2_A, evoked3_A, evoked4_A, evoked5_A, evoked6_A, evoked7_A, 
         evoked8_A, evoked9_A, evoked10_A, evoked11_A, evoked12_A, evoked13_A]

listB = [evoked1_B, evoked2_B, evoked3_B, evoked4_B, evoked5_B, evoked6_B, evoked7_B, 
         evoked8_B, evoked9_B, evoked10_B, evoked11_B, evoked12_A, evoked13_A]

evoked_A = mne.grand_average(listA)
evoked_B = mne.grand_average(listB)

sns.set(style="white")
sns.set_context("poster")

ts_args = dict(gfp=True, zorder='std',
               ylim =dict(eeg=[-6,8]), unit=True)
topomap_args = dict(sensors=False, vmax=6, vmin=-6, average=0.025, contours=8, cmap='magma')
gfp_A_EEGfMRI = evoked_A.plot_joint(title=None,
                  times=[.2, .35, .45, .6],
                  ts_args=ts_args, topomap_args=topomap_args)

ts_args = dict(gfp=True, zorder='std',
               ylim =dict(eeg=[-6,8]), unit=True)
topomap_args = dict(sensors=False, vmax=6, vmin=-6, average=0.025, contours=8, cmap='magma')
gfp_B_EEGfMRI = evoked_B.plot_joint(title=None,
                  times=[.2, .35, .5, .6],
                  ts_args=ts_args, topomap_args=topomap_args)

pp = PdfPages('gfp_cues_EEGfMRI.pdf')
pp.savefig(gfp_A_EEGfMRI)
pp.savefig(gfp_B_EEGfMRI)
pp.close()
