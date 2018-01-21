"""
Created on Sat Dec 09 15:44:55 2017

@author: Malte R. Güth
"""

import mne
import seaborn as sns

# Create ERPs with Global Field Power (GFP) for preprocessed EEG data (see Preprocessing folder)
# and save the plots as pdf. Load single subject evoked data and create lists for all epochs (i.e. Cue A and B).

listA = [evoked1_A, evoked2_A, evoked3_A, evoked4_A, evoked5_A, evoked6_A, evoked7_A, 
         evoked8_A, evoked9_A, evoked10_A, evoked11_A, evoked12_A, evoked13_A]

listB = [evoked1_B, evoked2_B, evoked3_B, evoked4_B, evoked5_B, evoked6_B, evoked7_B, 
         evoked8_B, evoked9_B, evoked10_B, evoked11_B, evoked12_A, evoked13_A]


evoked_A = mne.grand_average(listA)
evoked_B = mne.grand_average(listB)

sns.set(style="dark")
sns.set_context("poster")

ts_args = dict(gfp=True, zorder='std',
               ylim =dict(eeg=[-6,8]), unit=True)
topomap_args = dict(sensors=False, vmax=8, vmin=-6, average=0.05, contours=7)
gfp_A_EEGfMRI = evoked_A.plot_joint(title=None,
                  times=[.2, .35, .45, .6],
                  ts_args=ts_args, topomap_args=topomap_args)

ts_args = dict(gfp=True, zorder='std',
               ylim =dict(eeg=[-6,8]), unit=True)
topomap_args = dict(sensors=False, vmax=8, vmin=-6, average=0.05, contours=7)
gfp_B_EEGfMRI = evoked_B.plot_joint(title=None,
                  times=[.2, .35, .5, .6],
                  ts_args=ts_args, topomap_args=topomap_args)

from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('gfp_cues_EEGfMRI.pdf')
pp.savefig(gfp_A_EEGfMRI)
pp.savefig(gfp_B_EEGfMRI)
pp.close()
