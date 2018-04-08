"""
Created on Sun Mar  18 12:15:16 2018

@author: maltegueth
"""

from os.path import join as opj
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.interfaces.spm import (OneSampleTTestDesign, EstimateModel,
                                   EstimateContrast, Threshold)
from nipype.interfaces.utility import IdentityInterface
from nipype.pipeline.engine import Workflow, Node
from nipype.algorithms.misc import Gunzip

from nilearn.plotting import plot_stat_map
from nilearn.plotting import plot_glass_brain

experiment_dir = '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output'
output_dir = '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/data'
working_dir = '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/workingdir'

# Smoothing withds used during preprocessing
fwhm = 5

# Which contrasts to use for the 2nd-level analysis
contrast_list = ['con_0001', 'con_0002', 'con_0003', 'con_0004', 'con_0005']

mask = "/usr/local/fsl/data/standard/MNI152_T1_1mm_brain_mask_dil.nii.gz"

# Gunzip - unzip the mask image
gunzip = Node(Gunzip(in_file=mask), name="gunzip")

# OneSampleTTestDesign - with only two cues being tested for differences, a one sample T-Test Design
# is sufficient
onesamplettestdes = Node(OneSampleTTestDesign(),
                         name="onesampttestdes")

# EstimateModel - estimates the model
level2estimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      name="level2estimate")

# EstimateContrast - estimates group contrast
level2conestimate = Node(EstimateContrast(group_contrast=True),
                         name="level2conestimate")
cont1 = ['Group', 'T', ['mean'], [1]]
level2conestimate.inputs.contrasts = [cont1]

# Threshold - thresholds contrasts
level2thresh = Node(Threshold(contrast_index=1,
                              use_topo_fdr=True,
                              use_fwe_correction=False,
                              extent_threshold=0,
                              height_threshold=0.005,
                              height_threshold_type='p-value',
                              extent_fdr_p_threshold=0.05),
                    name="level2thresh")

# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['contrast_id', 'fwhm_id']),
                  name="infosource")
infosource.iterables = [('contrast_id', contrast_list),
                        ('fwhm_id', fwhm)]

# SelectFiles - to grab the data (alternativ to DataGrabber)
templates = {'cons': opj(output_dir, 'norm_spm', 'sub*_fwhm{fwhm_id}',
                         'w{contrast_id}.nii')}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir,
                               sort_filelist=True),
                   name="selectfiles")

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_contrast_id_', '')]
subjFolders = [('%s_fwhm_id_%s' % (con, f), 'spm_%s_fwhm%s' % (con, f))
               for f in fwhm
               for con in contrast_list]
substitutions.extend(subjFolders)
datasink.inputs.substitutions = substitutions

# Initiation of the 2nd-level analysis workflow
l2analysis = Workflow(name='spm_l2analysis')
l2analysis.base_dir = opj(experiment_dir, working_dir)

# Connect up the 2nd-level analysis components
l2analysis.connect([(infosource, selectfiles, [('contrast_id', 'contrast_id'),
                                               ('fwhm_id', 'fwhm_id')]),
                    (selectfiles, onesamplettestdes, [('cons', 'in_files')]),
                    (gunzip, onesamplettestdes, [('out_file',
                                                  'explicit_mask_file')]),
                    (onesamplettestdes, level2estimate, [('spm_mat_file',
                                                          'spm_mat_file')]),
                    (level2estimate, level2conestimate, [('spm_mat_file',
                                                          'spm_mat_file'),
                                                         ('beta_images',
                                                          'beta_images'),
                                                         ('residual_image',
                                                          'residual_image')]),
                    (level2conestimate, level2thresh, [('spm_mat_file',
                                                        'spm_mat_file'),
                                                       ('spmT_images',
                                                        'stat_image'),
                                                       ]),
                    (level2conestimate, datasink, [('spm_mat_file',
                                                    '2ndLevel.@spm_mat'),
                                                   ('spmT_images',
                                                    '2ndLevel.@T'),
                                                   ('con_images',
                                                    '2ndLevel.@con')]),
                    (level2thresh, datasink, [('thresholded_map',
                                               '2ndLevel.@threshold')]),
                    ])

l2analysis.run('MultiProc', plugin_args={'n_procs': 4})

# Plotting after L2 analysis

anatimg = '/usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz'

AB1 = plot_stat_map(
    '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output/datasink/2ndLevel/spm_con_0001_fwhm5/spmT_0001_thr.nii', 
    title='A>B, FWE<0.05 cluster-corrected', dim=1, bg_img=anatimg, threshold=2, vmax=8, display_mode='z', 
    cut_coords=(10, 5, 0, -3), cmap='inferno');
AB2 = plot_stat_map(
    '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output/datasink/2ndLevel/spm_con_0004_fwhm5/spmT_0004_thr.nii', 
    title='A>B, FWE<0.05 cluster-corrected', dim=1, bg_img=anatimg, threshold=2, vmax=8, display_mode='y', 
    cut_coords=(35, 31, 25), cmap='inferno');
glassAB = plot_glass_brain(
    '/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/output/datasink/2ndLevel/spm_con_0004_fwhm5/spmT_0004_thr.nii',
    colorbar=True, threshold=2, display_mode='lyrz', black_bg=True, vmax=8, 
    title='A>B, FWE<0.05 cluster-corrected', cmap='inferno');

AB1.savefig('/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/L2_AB_axial.pdf')
AB2.savefig('/Volumes/INTENSO/DPX_EEG_fMRI/fMRI/L2_AB_coronal.pdf')
glassAB.savefig('/Volumes/INTENSO/DPX_EEG_fMRI/L2_AB_glass.pdf')
