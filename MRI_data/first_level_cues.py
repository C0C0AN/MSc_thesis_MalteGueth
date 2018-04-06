"""
Created on Sat Mar  17 09:15:16 2018

@author: Malte Gueth
"""

# First level analysis for fMRI data (only accounting for cue-related activations) based on examples provided in
# nipype tutorials (https://miykael.github.io/nipype_tutorial/notebooks/example_1stlevel.html#Specify-GLM-Model)

from os.path import join as opj
import json
from nipype.interfaces.spm import Level1Design, EstimateModel, EstimateContrast
from nipype.algorithms.modelgen import SpecifySPMModel
from nipype.interfaces.utility import Function, IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.pipeline.engine import Workflow, Node

from nilearn.plotting import plot_stat_map
from nilearn.plotting import plot_glass_brain

experiment_dir = '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output'
output_dir = '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/data'
working_dir = '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/workingdir'

# list of subject identifiers
subject_list = ['sub01', 'sub02', 'sub03', 'sub04', 'sub05',
                'sub06', 'sub07', 'sub08', 'sub09', 'sub10',
                'sub11', 'sub12', 'sub13']

# TR of functional images
with open('/data/dpx_bold.json', 'rt') as dpx:
    task_info = json.load(dpx)
TR = task_info['RepetitionTime']

# Smoothing withds used during preprocessing
fwhm = 5

# SpecifyModel - Generates SPM-specific Model
modelspec = Node(SpecifySPMModel(concatenate_runs=False,
                                 input_units='secs',
                                 output_units='secs',
                                 time_repetition=TR,
                                 high_pass_filter_cutoff=90),
                 name="modelspec")

# Level1Design - Generates an SPM design matrix
level1design = Node(Level1Design(bases={'hrf': {'derivs': [1, 0]}},
                                 timing_units='secs',
                                 interscan_interval=TR,
                                 model_serial_correlations='FAST'),
                    name="level1design")

# EstimateModel - estimate the parameters of the model
level1estimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      name="level1estimate")

# EstimateContrast - estimates contrasts
level1conest = Node(EstimateContrast(), name="level1conest")

# Condition names
condition_names = ['CueA', 'CueB']

# Contrasts
con_01 = ['average',        'T', condition_names, [1/2., 1/2.]]
con_02 = ['CueA',         'T', condition_names, [1, 0]]
con_03 = ['CueB',           'T', condition_names, [0, 1]]
con_04 = ['CueA > CueB','T', condition_names, [1, -1]]
con_05 = ['CueB > CueA',  'T', condition_names, [-1, 1]]

contrast_list = [con_01, con_02, con_03, con_04, con_05]

def subjectinfo(subject_id):

    import pandas as pd
    from nipype.interfaces.base import Bunch
    
    trialinfo = pd.read_table('/Volumes/INTENSO/DPX_EEG_fMRI/eventfiles/all_cues.csv')
    trialinfo.head()
    conditions = []
    onsets = []
    durations = []

    for group in trialinfo.groupby('trial_type'):
        conditions.append(group[0])
        durations.append(group[1].duration.tolist())

    subject_info = [Bunch(conditions=conditions,
                          onsets=onsets,
                          durations=durations)]

    return subject_info  # this output will later be returned to infosource

# Get Subject Info - get subject specific condition information
getsubjectinfo = Node(Function(input_names=['subject_id'],
                               output_names=['subject_info'],
                               function=subjectinfo),
                      name='getsubjectinfo')
    
# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id',
                                            'fwhm_id',
                                            'contrasts'],
                                    contrasts=contrast_list),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list),
                        ('fwhm_id', fwhm)]

# SelectFiles - to grab the data (alternativ to DataGrabber)
templates = {'func': opj(output_dir, 'preproc', '{subject_id}', 'task-{task_id}',
                         'fwhm-{fwhm_id}_s{subject_id}_ses-test_task-{task_id}_bold.nii'),
             'mc_param': opj(output_dir, 'preproc', '{subject_id}', 'task-{task_id}',
                             '{subject_id}_ses-test_task-{task_id}_bold.par'),
             'outliers': opj(output_dir, 'preproc', '{subject_id}', 'task-{task_id}', 
                             'art.{subject_id}_ses-test_task-{task_id}_bold_outliers.txt')}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir,
                               sort_filelist=True),
                   name="selectfiles")
selectfiles.inputs.task_id = 'dpx'

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_subject_id_', '')]
subjFolders = [('_fwhm_id_%s%s' % (f, sub), '%s/fwhm-%s' % (sub, f))
               for f in fwhm
               for sub in subject_list]
substitutions.extend(subjFolders)
datasink.inputs.substitutions = substitutions

# Initiation of the 1st-level analysis workflow
l1analysis = Workflow(name='l1analysis')
l1analysis.base_dir = opj(experiment_dir, working_dir)

# Connect up the 1st-level analysis components
l1analysis.connect([(infosource, selectfiles, [('subject_id', 'subject_id'),
                                               ('fwhm_id', 'fwhm_id')]),
                    (infosource, getsubjectinfo, [('subject_id',
                                                   'subject_id')]),
                    (getsubjectinfo, modelspec, [('subject_info',
                                                  'subject_info')]),
                    (infosource, level1conest, [('contrasts', 'contrasts')]),
                    (selectfiles, modelspec, [('func', 'functional_runs')]),
                    (selectfiles, modelspec, [('mc_param', 'realignment_parameters'),
                                              ('outliers', 'outlier_files')]),
                    (modelspec, level1design, [('session_info',
                                                'session_info')]),
                    (level1design, level1estimate, [('spm_mat_file',
                                                     'spm_mat_file')]),
                    (level1estimate, level1conest, [('spm_mat_file',
                                                     'spm_mat_file'),
                                                    ('beta_images',
                                                     'beta_images'),
                                                    ('residual_image',
                                                     'residual_image')]),
                    (level1conest, datasink, [('spm_mat_file', '1stLevel.@spm_mat'),
                                              ('spmT_images', '1stLevel.@T'),
                                              ('con_images', '1stLevel.@con')
                                              ]),
                    ])
             
l1analysis.run('MultiProc', plugin_args={'n_procs': 4})

# Plotting after L1 analysis

anatimg = '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/structural/VP13/structural.nii'

ABase = plot_stat_map(
    '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output/datasink/1stLevel/sub13/fwhm-5/spmT_0001.nii', title='CueA', dim=1,
    bg_img=anatimg, threshold=2, vmax=8, display_mode='z', cut_coords=(55, 0, -5, -10), cmap='magma');
AB = plot_stat_map(
    '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output/datasink/1stLevel/sub13/fwhm-5/spmT_0004.nii', title='CueA>CueB', dim=1,
    bg_img=anatimg, threshold=2, vmax=8, display_mode='y', cut_coords=(55, 35, 15), cmap='magma');
glassA = plot_glass_brain(
    '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output/datasink/1stLevel/sub13/fwhm-5/spmT_0004.nii', colorbar=True,
    threshold=2, display_mode='lyrz', black_bg=True, vmax=8, title='CueA');
