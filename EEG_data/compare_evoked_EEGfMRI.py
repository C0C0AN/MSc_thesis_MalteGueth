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

colors1 = dict(CueA="cyan", CueB="darkblue")
linestyles1 = dict(CueA='-', CueB='--')
picks1 = ch_names.index('Pz')
evoked_dict1 = {'CueA': lisA,'CueB': listB}

evoked_cues_pz = mne.viz.plot_compare_evokeds(evoked_dict1, picks=picks1, truncate_yaxis=False, 
                             title='Cue A (light blue) and Cue B (dark blue) at Pz averaged over all blocks',
                             invert_y=True, ci=0.90, linestyles=linestyles, 
                             colors=colors, ylim = dict(eeg=[-4,8]))


colors2 = dict(AX="lightcoral", BX="crimson",
               AY="lightcoral", BY="crimson",)
linestyles2 = dict(AX='-', BX='--',
                   AY='-', BY='--')
picks2 = ch_names.index('Fz')
evoked_dict2 = {'AX': listAX, 'BX': listBX, 'AY': listAY, 'BY': listBY}

evoked_probes_pz = mne.viz.plot_compare_evokeds(evoked_dict2, picks=picks2, truncate_yaxis=False, 
                             title='AX (light blue, solid), BX (red, solid), AY (light blue, dashed) and BY (red, dashed) probe-locked at Pz over all blocks',
                             invert_y=True, ci=0.90, linestyles=linestyles2, 
                             colors=colors2, ylim = dict(eeg=[-4,10]))

colors1 = dict(CueA="cyan", CueB="darkblue")
linestyles1 = dict(CueA='-', CueB='--')
picks1 = ch_names.index('Fz')
evoked_dict1 = {'CueA': lisA,'CueB': listB}

evoked_cues_fz = mne.viz.plot_compare_evokeds(evoked_dict1, picks=picks1, truncate_yaxis=False, 
                             title='Cue A (light blue) and Cue B (dark blue) at Fz averaged over all blocks',
                             invert_y=True, ci=0.90, linestyles=linestyles, 
                             colors=colors, ylim = dict(eeg=[-4,8]))


colors2 = dict(AX="lightcoral", BX="crimson",
               AY="lightcoral", BY="crimson",)
linestyles2 = dict(AX='-', BX='--',
                   AY='-', BY='--')
picks2 = ch_names.index('Fz')
evoked_dict2 = {'AX': listAX, 'BX': listBX, 'AY': listAY, 'BY': listBY}

evoked_probes_fz = mne.viz.plot_compare_evokeds(evoked_dict2, picks=picks2, truncate_yaxis=False, 
                             title='AX (light blue, solid), BX (red, solid), AY (light blue, dashed) and BY (red, dashed) probe-locked at Pz over all blocks',
                             invert_y=True, ci=0.90, linestyles=linestyles2, 
                             colors=colors2, ylim = dict(eeg=[-4,10]))


pp = PdfPages('compare_cues_probes_allblocks.pdf')
pp.savefig(evoked_cues_pz)
pp.savefig(evoked_probes_pz)
pp.savefig(evoked_cues_fz)
pp.savefig(evoked_probes_fz)
pp.close()
