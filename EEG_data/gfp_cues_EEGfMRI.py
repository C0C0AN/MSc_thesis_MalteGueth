"""
Created on Sat Dec 09 15:44:55 2017

@author: Malte R. Güth
"""

import os
import glob

import mne

# Create ERPs with Global Field Power (GFP) for pre-processed EEG data and save the plots as pdf. 
# Load single subject evoked data and create lists for all epochs (i.e. Cue A and B).

path = './evoked/'
evoked_a = []
for file in glob.glob(os.path.join(path, '*A-ave.fif')):

    evoked = mne.read_evokeds(file) 
    evoked_a.append(evoked)
    
path = './evoked/'
evoked_b = []
for file in glob.glob(os.path.join(path, '*B-ave.fif')):

    evoked = mne.read_evokeds(file) 
    evoked_b.append(evoked)
    
evoked_a = mne.grand_average(evoked_a)
evoked_b = mne.grand_average(evoked_b)

evoked_a.apply_baseline(baseline=(-0.25, 0))
evoked_b.apply_baseline(baseline=(-0.25, 0))


ts_args = dict(gfp=True, zorder='std',
               ylim =dict(eeg=[-6,8]), unit=True)
topomap_args = dict(sensors=False, vmax=8, vmin=-6, average=0.025, contours=2)
gfp_A_EEGfMRI = evoked_A.plot_joint(title=None,
                                    times=[.2, .35, .45, .6],
                                    ts_args=ts_args, topomap_args=topomap_args)

ts_args = dict(gfp=True, zorder='std',
               ylim =dict(eeg=[-6,8]), unit=True)
topomap_args = dict(sensors=False, vmax=8, vmin=-6, average=0.025, contours=2)
gfp_B_EEGfMRI = evoked_B.plot_joint(title=None,
                                    times=[.2, .35, .5, .6],
                                    ts_args=ts_args, topomap_args=topomap_args)

gfp_A_EEGfMRI.savefig('./gfp_A_EEGfMRI.pdf')
gfp_B_EEGfMRI.savefig('./gfp_B_EEGfMRI.pdf')
