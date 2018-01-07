"""
Created on Fri Jan 5 12:14:15 2018

@author: Malte
"""

# Script for computing a head model and forward modeling
# Before running you need to preprocess your sMRI data with freesurfer and perform three computations:
#
# (1) BEM surfaces (triangulations of the interfaces between different tissues)
# (2) A transformation file with the ending '-trans.fif' 
# (info file from coregestering the MRI data with a subject’s head shape 
# to position the head and the sensors in a common coordinate system)
# (3) A source space (positions of the candidate source locations)
#
# (1) can be done using mne watershed_bem or mne flash_bem in the terminal
# These require the subject directory from freesurfer and a subject name
# (2) can be computed by either using the command line tools mne_analyze (Unix) or mne coreg
# A guide on how to perform the coregistration and creating the trans fif file 
# can be found here: https://de.slideshare.net/mne-python/mnepythyon-coregistration-28598463
# (3) can be setup very conviently with the function mne.setup_source_space 
# by providing a subject directory and the raw eeg file

import mne

subjects_dir = '/Users/maltegueth/Documents/dpx_freesurfer/freesurfer/'
subject_mri = 'VP02'
subject_eeg = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Sub2_raw.fif'

mne.viz.plot_bem(subject=subject_mri, subjects_dir=subjects_dir,
                 brain_surfaces='white', orientation='coronal')

# The transformation file obtained by coregistration
trans = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Sub2_raw-trans.fif'

info = mne.io.read_info(subject_eeg)
mne.viz.plot_alignment(info, trans, subject=subject_mri, dig=True,
                       meg=['helmet', 'sensors'], subjects_dir=subjects_dir)

src = mne.setup_source_space(subject_mri, spacing='oct6',
                             subjects_dir=subjects_dir, add_dist=False)
print(src)

import numpy as np  # noqa
from mayavi import mlab  # noqa
from surfer import Brain  # noqa

brain = Brain('sample', 'lh', 'inflated', subjects_dir=subjects_dir)
surf = brain.geo['lh']

vertidx = np.where(src[0]['inuse'])[0]

mlab.points3d(surf.x[vertidx], surf.y[vertidx],
              surf.z[vertidx], color=(1, 1, 0), scale_factor=1.5)

conductivity = (0.3, 0.006, 0.3)  # for single layer
# conductivity = (0.3, 0.006, 0.3)  # for three layers
model = mne.make_bem_model(subject='sample', ico=4,
                           conductivity=conductivity,
                           subjects_dir=subjects_dir)
bem = mne.make_bem_solution(model)

fwd = mne.make_forward_solution(subject_eeg, trans=trans, src=src, bem=bem,
                                meg=True, eeg=False, mindist=5.0, n_jobs=2)
print(fwd)

leadfield = fwd['sol']['data']
print("Leadfield size : %d sensors x %d dipoles" % leadfield.shape)

fwd_fixed = mne.convert_forward_solution(fwd, surf_ori=True, force_fixed=True,
                                         use_cps=True)
leadfield = fwd_fixed['sol']['data']
print("Leadfield size : %d sensors x %d dipoles" % leadfield.shape)

n_dipoles = leadfield.shape[1]
vertices = [src_hemi['vertno'] for src_hemi in fwd_fixed['src']]
stc = mne.SourceEstimate(1e-9 * np.eye(n_dipoles), vertices, tmin=0., tstep=1)
leadfield = mne.apply_forward(fwd_fixed, stc, info).data / 1e-9

mne.write_forward_solution() 
mne.read_forward_solution()
