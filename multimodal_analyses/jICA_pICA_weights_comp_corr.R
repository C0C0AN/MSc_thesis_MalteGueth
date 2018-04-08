#####
##### Code for plotting joint and parallel ICA results
#####

# Read tables for EEG components, correlation coefficients, ICA weights and other data from ICA

names_cues <- c('points', 'microvolt')
jica_eeg_cue_a <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/jICA/jICA_cues_joint_comp_ica_feature_3_008.asc", 
                   header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE, 
                   col.names = names_cues)
jica_eeg_cue_b <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/jICA/jICA_cues_joint_comp_ica_feature_4_008.asc", 
                            header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE, 
                            col.names = names_cues)

names_weights <- c('condition', 'component', 'beta_weight')
jica_beta_weights <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/jICA/jICA_cues_beta_weight_comb_1.txt", 
                                header = TRUE, sep = '', na.strings = "NA", dec = ".", strip.white = TRUE,
                                col.names = names_weights)
jica_beta_weights$condition <- revalue(jica_beta_weights$condition, c('A' = 0, 'B' = 1))

names_corr <- c('fMRI_feature', 'EEG_feature', 'correlation')
pica_corr_a <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/pICA/pica_cue_a/pica_a2_para_ica_correlations.txt", 
                                  header = TRUE, sep = '', na.strings = "NA", dec = ".", strip.white = TRUE,
                                  col.names = names_corr, blank.lines.skip = TRUE)
pica_corr_a$condition <- 0

pica_corr_b <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/pICA/pica_b3_para_ica_correlations.txt", 
                          header = TRUE, sep = '', na.strings = "NA", dec = ".", strip.white = TRUE,
                          col.names = names_corr, blank.lines.skip = TRUE)
pica_corr_b$condition <- 1

pica_corr <- rbind(pica_corr_a, pica_corr_b)
