"""
Created on Sat Dec 01 17:36:23 2017

@author: Malte R. Güth
"""

# Create simple seaborn line plots with single error of the mean with subjects from 
# the conventional EEG experiment (Dot-Pattern-Expectancy Task; rt_eeg.txt) along with subjects from the 
# simultaneous assessment (rt_eegfmri.txt) and save the plots as pdf.
# Data must be long data format with ID, block, rt and trial type as columns converted to pandas dataframe.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_pdf import PdfPages

sns.set(style="dark")
sns.set_context("poster")

df_eegfmri = pd.DataFrame({'ID': id_eegfmri,
                   'block': block_eegfmri,
                   'trialtype': trialtype_eegfmri,
                   'reaction time [ms]': rt_eegfmri})
f1, ax = plt.subplots()
figfmri = sns.tsplot(data=df_eegfmri, time="block", unit = "ID",
           condition="trialtype", value="reaction time [ms]", 
           err_style="ci_band", ci=60)
figfmri.set(xticks=df_eegfmri.block[0::4])
handles, labels = ax.get_legend_handles_labels()
ax.legend_.remove()

sns.set(style="dark")
sns.set_context("poster")

df_eeg = pd.DataFrame({'ID': id_eeg,
                   'block': block_eeg,
                   'trialtype': trialtype_eeg,
                   'reaction time [ms]': rt_eeg})
f2, ax = plt.subplots()
figeeg = sns.tsplot(data=df_eeg, time="block", unit = "ID",
           condition="trialtype", value="reaction time [ms]", 
           err_style="ci_band", ci=60)
figeeg.set(xticks=df_eeg.block[0::4])
handles, labels = ax.get_legend_handles_labels()
ax.legend_.remove()

pp = PdfPages('rt_eeg_eegfmri.pdf')
pp.savefig(f1)
pp.savefig(f2)
pp.close()
