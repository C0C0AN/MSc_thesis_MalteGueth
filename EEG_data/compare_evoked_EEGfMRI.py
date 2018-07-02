"""
Created on Fri Dec 06 05:56:37 2017

@author: Malte
"""

# Script for plotting ERPs as line plots for selected channels and conditions (cues and probes)
# and saving the plots as pdfs

# Instances of evoked have to be averaged epochs for a specific subject and condition
# Appnending them to create a list, enables plotting confindence intervals or standradr errors
# as shaded areas around the line plots

import os
import glob

import mne

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
    
colors1 = dict(CueA='CornFlowerBlue', CueB='darkblue')
colors2 = dict(AX='CornFlowerBlue', AY='darkblue')
colors3 = dict(BX='CornFlowerBlue', BY='darkblue')

linestyles1 = dict(CueA='-', CueB='--')
linestyles2 = dict(AX='-', AY='--')
linestyles3 = dict(BX='-', BY='--')

picks1 = chanlabels.index('Pz')
picks2 = chanlabels.index('Fz')

evoked_dict1 = {'CueA': listA,'CueB': listB}
evoked_dict2 = {'AX': listAX, 'AY': listAY}
evoked_dict3 = {'BX': listBX, 'BY': listBY}

vlines = list([0])

evoked_cues_pz = mne.viz.plot_compare_evokeds(evoked_dict1, picks=picks1, truncate_yaxis='max_ticks', 
                             truncate_xaxis='max_ticks', show_legend=True, title=None,
                             invert_y=True, ci=0.90, linestyles=linestyles1, 
                             colors=colors1, ylim = dict(eeg=[-4,8.5]), vlines=vlines)

evoked_cues_fz = mne.viz.plot_compare_evokeds(evoked_dict1, picks=picks2, truncate_yaxis='max_ticks', 
                             truncate_xaxis='max_ticks', show_legend=True, title=None,
                             invert_y=True, ci=0.90, linestyles=linestyles1, 
                             colors=colors1, ylim = dict(eeg=[-4,6]), vlines=vlines)

evoked_AXAY_pz = mne.viz.plot_compare_evokeds(evoked_dict2, picks=picks1, truncate_yaxis='max_ticks', 
                             truncate_xaxis='max_ticks', show_legend=True, title=None,
                             invert_y=True, ci=0.90, linestyles=linestyles2, 
                             colors=colors2, ylim = dict(eeg=[-6,12]), vlines=vlines)

evoked_BXBY_pz = mne.viz.plot_compare_evokeds(evoked_dict3, picks=picks1, truncate_yaxis='max_ticks', 
                             truncate_xaxis='max_ticks', show_legend=True, title=None,
                             invert_y=True, ci=0.90, linestyles=linestyles3, 
                             colors=colors3, ylim = dict(eeg=[-6,12]), vlines=vlines)

evoked_AXAY_fz = mne.viz.plot_compare_evokeds(evoked_dict2, picks=picks2, truncate_yaxis='max_ticks', 
                             truncate_xaxis='max_ticks', show_legend=True, title=None,
                             invert_y=True, ci=0.90, linestyles=linestyles2, 
                             colors=colors2, ylim = dict(eeg=[-6,12]), vlines=vlines)

evoked_BXBY_fz = mne.viz.plot_compare_evokeds(evoked_dict3, picks=picks2, truncate_yaxis='max_ticks', 
                             truncate_xaxis='max_ticks', show_legend=True, title=None,
                             invert_y=True, ci=0.90, linestyles=linestyles3, 
                             colors=colors3, ylim = dict(eeg=[-6,12]), vlines=vlines)

evoked_cues_pz.savefig('./evoked_cues_pz.pdf')
evoked_cues_fz.savefig('./evoked_cues_fz.pdf')
evoked_AXAY_pz.savefig('./evoked_AXAY_pz.pdf')
evoked_BXBY_pz.savefig('./evoked_BXBY_pz.pdf')
evoked_AXAY_fz.savefig('./evoked_AXAY_fz.pdf')
evoked_BXBY_fz.savefig('./evoked_BXBY_fz.pdf')

