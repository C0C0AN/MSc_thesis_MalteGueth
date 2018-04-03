"""
Created on Thu Jan  4 11:44:46 2018

@author: maltegueth
"""

# First attempt at second half of preprocessing of filtered and referenced data corrected 
# for gradient artifacts, ecg artifacts and eye movement with ica

import mne

import os.path as op

import pandas as pd
import numpy as np

for x in range(1, 14):
    
    # Each time the loop goes through a new iteration, 
    # add a subject integer to the data path
    data_path = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/'
    
    subject_dir = op.join(data_path, 'MNE/Sub%d_preprocessed_raw.fif') % (x) 
    event_dir = op.join(data_path, 'events/Sub%d_preprocessed_raw-eve.fif') % (x) 
    output_dir = op.join(data_path, 'MNE/epochs/Sub%d_preprocessed_epochs.fif') % (x)

    
    # Read the raw EEG data that has been preprocessed
    raw = mne.io.read_raw_fif(subject_dir, event_id=None, preload=True)
    
    # Define the stimulus labels for epoching
    event_id = {'A': {70, 71, 72, 73, 74}, 'B': {75, 76, 77, 78, 79, 80, 81, 82, 83}}
    events = mne.read_events(event_dir)
    
    # Epoch the preprocessed data with a baseline of -200 ms and 1000 ms after the stimulus onset,
    # save the data as fif and as a pandas DataFrame
    epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.2, tmax=1.0)
    epochs.save(output_dir)
    df
    
    # Average epoched data over conditions
    evoked_cueA = epochs['A'].average()
    evoked_cueB = epochs['B'].average()
    

# Preprare single trial data for higher level analyses in Python as well as for importing data to R
# To achieve a sensible data structure all trials are transformed to a Pandas DataFrame
# Here are two easy ways to arrange data in a suitable manner for applications in both languages

# 1) Combine all subject data sets by looping through all epochs, converting them to DataFrames, appending
# them with '.append' and save them to a csv with '.to_csv'

for i in range(1, 14):
    index, scaling_time = ['epoch', 'time'], 1e3
    epochs = '/Sub%d_preprocessed_epochs.fif' % (i)
    current_epochs = mne.read_epochs(epochs)
    df = current_epochs.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)  
    df_all1 = df_all1.append(df)

df_all1.to_csv('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/MNE/epochs/eeg_epochs.csv')

# 2) Load all single subject data sets separately, convert them each to a DataFrame, use pandas concat function, add
# a column for subject number with the length of all subjects' trials and, again, save the DataFrame to a csv

df1 = epochs1.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df2 = epochs2.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df3 = epochs3.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df4 = epochs4.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df5 = epochs5.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df6 = epochs6.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df7 = epochs7.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df8 = epochs8.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df9 = epochs9.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df10 = epochs10.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df11 = epochs11.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df12 = epochs12.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)
df13 = epochs13.to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)

df_all2 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13])

df_all['subject'] = np.r_[np.ones(len(df1)), np.ones(len(df2)) + 1, np.ones(len(df3)) + 2,
      np.ones(len(df4)) + 3, np.ones(len(df5)) + 4, np.ones(len(df6)) + 5, np.ones(len(df7)) + 6,
      np.ones(len(df8)) + 7, np.ones(len(df9)) + 8, np.ones(len(df10)) + 9, np.ones(len(df11)) + 10,
      np.ones(len(df12)) + 11, np.ones(len(df13)) + 12]

df_all2.to_csv('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/MNE/epochs/eeg_epochs.csv')
