"""
Created on Fri Dec 06 05:56:37 2017

@author: Malte
"""

# Script for plotting ERPs as line plots for selected channels and conditions (cues and probes)
# and saving the plots as pdfs

# Instances of evoked have to be averaged epochs for a specific subject and condition
# Appnending them to create a list, enables plotting confindence intervals or standradr errors
# as shaded areas around the line plots

import mne

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

listA = [evokedA_1, evokedA_2, evokedA_3, evokedA_4, evokedA_5, evokedA_6, 
         evokedA_7, evokedA_8, evokedA_9,evokedA_10, evokedA_11, evokedA_12, evokedA_13]

listB = [evokedB_1, evokedB_2, evokedB_3, evokedB_4, evokedB_5, evokedB_6, 
         evokedB_7, evokedB_8, evokedB_9,evokedB_10, evokedB_11, evokedB_12, evokedB_13]

listAX = [evokedAX_1, evokedAX_2, evokedAX_3, evokedAX_4, evokedAX_5, evokedAX_6, 
          evokedX_7, evokedAX_8, evokedAX_9,evokedAX_10, evokedAX_11, evokedAX_12, evokedAX_13]

listBX = [evokedBX_1, evokedBX_2, evokedBX_3, evokedBX_4, evokedBX_5, evokedBX_6, 
          evokedBX_7, evokedBX_8, evokedBX_9,evokedBX_10, evokedBX_11, evokedBX_12, evokedBX_13]

listAY = [evokedAY_1, evokedAY_2, evokedAY_3, evokedAY_4, evokedAY_5, evokedAY_6, 
          evokedAY_7, evokedAY_8, evokedAY_9,evokedAY_10, evokedAY_11, evokedAY_12, evokedAY_13]

listBY = [evokedBY_1, evokedBY_2, evokedBY_3, evokedBY_4, evokedBY_5, evokedBY_6, 
          evokedBY_7, evokedBY_8, evokedBY_9,evokedBY_10, evokedBY_11, evokedBY_12, evokedBY_13]

colors1 = dict(CueA="CornFlowerBlue", CueB="darkblue")
colors2 = dict(AX="CornFlowerBlue", AY="darkblue")
colors3 = dict(BX="CornFlowerBlue", BY="darkblue")

linestyles1 = dict(CueA='-', CueB='--')
linestyles2 = dict(AX='-', AY='-')
linestyles3 = dict(BX='-', BY='-')

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


pp = PdfPages('compare_cues_EEGfMRI.pdf')
pp.savefig(evoked_cues_pz)
pp.savefig(evoked_cues_fz)
pp.close()

pp = PdfPages('compare_probes_EEGfMRI.pdf')
pp.savefig(evoked_AXAY_pz)
pp.savefig(evoked_BXBY_pz)
pp.savefig(evoked_AXAY_fz)
pp.savefig(evoked_BXBY_fz)
pp.close()
