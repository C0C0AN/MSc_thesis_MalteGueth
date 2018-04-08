#####
##### Code snippets for EEG parameter convolution, txt file export and single trial export
##### 

# Read tables for single trial EEG data as pre-processed in 'first_preprocessing_EEG_annotated.py'
# and 'second_preprocessing_EEG_annotated.py'

require(neuRosim)
require(dplyr)
require(plyr)

setwd('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/MNE/')
eeg_data <- read.table("eeg_subjects_epochs_points_cond.csv", header = TRUE, 
                       sep = ",", na.strings = "NA", dec = ".", strip.white = TRUE)
eeg_data <- select(eeg_data, subject, epoch, time, condition, Pz)

eeg_data$condition <- revalue(eeg_data$condition, 
                              c('B5(S70)' = 0, 'B5(S71)' = 0, 'B5(S72)' = 0, 'B5(S73)' = 0,
                                'B5(S74)' = 0,
                                'B6(S75)' = 1, 'B6(S76)' = 1, 'B6(S77)' = 1, 'B6(S78)' = 1,
                                'B6(S79)' = 1, 'B6(S80)' = 1, 'B6(S81)' = 1, 'B6(S82)' = 1,
                                'B6(S83)' = 1))

eeg_data$condition <- as.factor(eeg_data$condition)
eeg_data$subject <- as.factor(eeg_data$subject)
eeg_data$epoch <- as.factor(eeg_data$epoch)

# Build the canonical hemodynamic response function and convolve EEG parameters
hrf <- canonicalHRF(1:500)
eeg_data$Pz <- convolve(eeg_data$Pz, hrf, type="open")

# Pick only time points from roughly 250 ms (187.5) to 1000 ms (250), since this interval contains 
# the sustained positivity
# With a sampling rate of 250 Hz there are 500 points per epoch
# Additionally, some buffer time is included to account for baseline noise in the signal
eeg_epochs_p3 <- eeg_data[ which(eeg_data$time >= 187.5 & eeg_data$time <= 250), ]

# Average across time points to receive one mean amplitude at Pz per epoch (for single trial BOLD prediction) 
# with descriptive statistics and in a separate data frame also average over epochs but with all points
# to receive first level parameters (for jICA, pICA)
eeg_epochs_p3 <- ddply(eeg_epochs_p3, c('subject', 'epoch', 'condition'), summarise,
                        points    = sum(!is.na(time)),
                        Mean_Amp = mean(Pz),
                        sd   = sd(Pz),
                        se   = sd / sqrt(points),
                        ci   = se * qt(.95/2 + .5, points-1))

eeg_mean_epoch <- ddply(eeg_data, c('subject', 'time', 'condition'), summarise,
                        trials    = sum(!is.na(epoch)),
                        Mean_Amp = mean(Pz),
                        sd   = sd(Pz),
                        se   = sd / sqrt(trials),
                        ci   = se * qt(.95/2 + .5, trials-1))

# Split the large data frame into subjects and divide them by condition
subs_mean_epoch <- split(eeg_mean_epoch, f = eeg_mean_epoch$subject)
subs_epochs_p3 <- split(eeg_epochs_p3, f = eeg_epochs_p3$subject)

subs_mean_epoch_cues <- split(subs_mean_epoch, f = eeg_mean_epoch$condition)
subs_epochs_p3_cues <- split(subs_epochs_p3, f = eeg_epochs_p3$condition)

# Write averaged data files
setwd('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Rtables/A/')
write.table(subs_mean_epoch_cues$`0`$`1`, './sub1_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`2`, './sub2_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`3`, './sub3_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`4`, './sub4_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`5`, './sub5_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`6`, './sub6_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`7`, './sub7_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`8`, './sub8_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`9`, './sub9_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`10`, './sub10_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`11`, './sub11_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`12`, './sub12_mean_epoch_A.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`0`$`13`, './sub13_mean_epoch_A.txt', row.names = F, sep = '\t')

setwd('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Rtables/B/')
write.table(subs_mean_epoch_cues$`1`$`1`, './sub1_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`2`, './sub2_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`3`, './sub3_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`4`, './sub4_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`5`, './sub5_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`6`, './sub6_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`7`, './sub7_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`8`, './sub8_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`9`, './sub9_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`10`, './sub10_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`11`, './sub11_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`12`, './sub12_mean_epoch_B.txt', row.names = F, sep = '\t')
write.table(subs_mean_epoch_cues$`1`$`13`, './sub13_mean_epoch_B.txt', row.names = F, sep = '\t')

# Write single trial data files
setwd('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Rtables/A/')
write.table(subs_epochs_p3_cues$`0`$`1`, './sub1_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`2`, './sub2_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`3`, './sub3_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`4`, './sub4_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`5`, './sub5_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`6`, './sub6_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`7`, './sub7_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`8`, './sub8_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`9`, './sub9_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`10`, './sub10_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`11`, './sub11_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`12`, './sub12_single_trial_A.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`0`$`13`, './sub13_single_trial_A.txt', row.names = F, sep = '\t')

setwd('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Rtables/B/')
write.table(subs_epochs_p3_cues$`1`$`1`, './sub1_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`2`, './sub2_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`3`, './sub3_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`4`, './sub4_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`5`, './sub5_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`6`, './sub6_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`7`, './sub7_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`8`, './sub8_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`9`, './sub9_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`10`, './sub10_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`11`, './sub11_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`12`, './sub12_single_trial_B.txt', row.names = F, sep = '\t')
write.table(subs_epochs_p3_cues$`1`$`13`, './sub13_single_trial_B.txt', row.names = F, sep = '\t')
