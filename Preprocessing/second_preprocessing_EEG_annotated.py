"""
Created on Thu Jan  4 11:44:46 2018

@author: maltegueth
"""

# First attempt at second half of preprocessing of filtered and referenced data corrected 
# for gradient artifacts, ecg artifacts and eye movement with ica

import mne
import os.path as op


for x in range(1, 14):
    
    # Each time the loop goes through a new iteration, 
    # add a subject integer to the data path
    data_path = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/'
    
    subject_dir = op.join(data_path, 'preprocessed_data/Sub%d_preprocessed_raw.fif') % (x) 
    event_dir = op.join(data_path, 'events/Sub%d_preprocessed_raw-eve.fif') % (x) 
    output_dir = op.join(data_path, 'epoched_data/Sub%d_preprocessed_epochs.fif') % (x)

    
    # Read the raw EEG data that has been preprocessed
    raw = mne.io.read_raw_fif(subject_dir, event_id=None, preload=True)
    
    # Define the stimulus labels for epoching
    event_id = {'A': {70, 71, 72, 73, 74}, 'B': {75, 76, 77, 78, 79, 80, 81, 82, 83}}
    events = mne.read_events(event_dir)
    
    # Epoch the preprocessed data with a baseline of -200 ms and 1000 ms after the stimulus onset
    # and save the data
    epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.2, tmax=1.0)
    epochs.save(output_dir)
    
    # Average epoched data over conditions
    evoked_cueA = epochs['A'].average()
    evoked_cueB = epochs['B'].average()
