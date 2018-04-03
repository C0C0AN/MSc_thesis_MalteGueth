#####
##### Code snippets for linear mixed effects regression as reported in the thesis paper
##### 

# Read in tables for EEG data as pre-processed in 'first_preprocessing_EEG_annotated.py'
# and 'second_preprocessing_EEG_annotated.py'

require(lme4)
require(car)

# Read in single trial EEG data and arrange it
setwd('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/MNE/')
eeg_data <- read.table("eeg_subjects_epochs_points_cond.csv", header = TRUE, 
                       sep = ",", na.strings = "NA", dec = ".", strip.white = TRUE)
eeg_data <- dplyr::select(eeg_data, subject, epoch, time, condition, Pz)
eeg_data$condition <- plyr::revalue(eeg_data$condition, 
                                    c('B5(S70)' = 1, 'B5(S71)' = 1, 'B5(S72)' = 1, 'B5(S73)' = 1,
                                      'B5(S74)' = 1,
                                      'B6(S75)' = 2, 'B6(S76)' = 2, 'B6(S77)' = 2, 'B6(S78)' = 2,
                                      'B6(S79)' = 2, 'B6(S80)' = 2, 'B6(S81)' = 2, 'B6(S82)' = 2,
                                      'B6(S83)' = 2))

eeg_data$condition <- as.factor(eeg_data$condition)
eeg_data$subject <- as.factor(eeg_data$subject)
eeg_data$epoch <- as.factor(eeg_data$epoch)

# Pick only time points from roughly 250 ms to 1000 ms, since this interval contains the sustained positivity
# Additionally, some more buffer time is included to account for regular signal fluctuation
eeg_epochs <- eeg_data[ which(eeg_data$time >= 187.5 & eeg_data$time <= 250), ]

# Average across time points to receive one mean amplitude at pz per epochs with descriptive statistics
eeg_epochs <- plyr::ddply(eeg_data, c('subject', 'epoch', 'condition'), dplyr::summarise,
                          points    = sum(!is.na(Pz)),
                          Mean_Amp = mean(Pz),
                          sd   = sd(Pz),
                          se   = sd / sqrt(points),
                          ci   = se * qt(.95/2 + .5, points-1))

# Set up regression equation with random slopes for trialtypes and intercepts for each block, 
# nested within each participant for each dependent variable

eeg_lmm <- lmer(Mean_Amp ~ condition + (1 | subject), data = eeg_epochs, REML = TRUE)
summary(eeg_lmm)
Anova(eeg_lmm)
