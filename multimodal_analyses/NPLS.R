#####
##### Script and examples for multiway partial least squares in R as recently implemented in the sNPLS package
##### by David Hervas (https://github.com/David-Hervas) in NPLS Regression with L1 Penalization
##### View on CRAN: https://cran.r-project.org/web/packages/sNPLS/index.html
#####

# Example:

require(sNPLS)
X_npls<-array(rpois(7500, 10), dim=c(50, 50, 3))

Y_npls<-matrix(2+0.4*X_npls[,5,1]+0.7*X_npls[,10,1]-0.9*X_npls[,15,1]+
                 0.6*X_npls[,20,1]- 0.5*X_npls[,25,1]+rnorm(50), ncol=1)

fit<-sNPLS(X_npls, Y_npls, ncomp=3, keepJ = rep(2,3) , keepK = rep(1,3))

# Out:
# Component number  1 
# Number of iterations:  1 
# Component number  2 
# Number of iterations:  1 
# Component number  3 
# Number of iterations:  1 

# Inputs are a time series of EEG data and a time series of fMRI data divided by experimental condition on single 
# subject level:
# EEG: 1) trial parameter (amplitude) per electrode over all trials modeled in the fMRI or ...
#      2) measures derived from single trial time-frequency analysis in the alpha (8-12 Hz) and theta (4-7 Hz) domain
#         with the same time points as in the fMRI as rows and frequencies by electrodes as columns (values in cells
#         equal power of frequency band from stimulus onset to 800 ms after, baseline corrected for a 
#         time period -1700 ms to -300 ms before stimulus onset
#         
# fMRI: time course signal for all relevant voxels modeled in a condition (i.e., activation time course
#       of a voxel with high intensity values in glm; if only one voxel/cluster was of interest, fMRI would
#       be a single vector with voxel activation over time)
# Per subject?

# Model using EEG amplitudes as EEG measure

setwd('/Volumes/INTENSO/DPX_EEG_fMRI')
names_fmri <- c('data','reduced data', 'partial model fit', 'full model fit')
time_series_a_fmri <- read.table('fMRI/FSL/functional/ts_data/VP01/ts_zstat1.txt', 
                             header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE, 
                             col.names = names_fmri)
time_series_a_fmri$partial.model.fit <- NULL
times_series_a_fmri$full.model.fit <- NULL

time_series_a_eeg <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Rtables/A/sub1_mean_epoch_A.txt", 
                                header = TRUE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_a_eeg$subject <- NULL
time_series_a_eeg$condition <- NULL
time_series_a_eeg$epoch <- NULL

time_series_b_fmri <- read.table("fMRI/FSL/functional/ts_data/VP01/ts_zstat2.txt", 
                                  header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE, 
                                  col.names = names_fmri)

time_series_b_eeg <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/EEG/Rtables/B/sub1_mean_epoch_B.txt", 
                                header = TRUE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_b_eeg$subject <- NULL
time_series_b_eeg$condition <- NULL
time_series_b_eeg$epoch <- NULL

time_series_b_fmri <- read.table("fMRI/FSL/functional/ts_data/VP02/ts_zstat2.txt", 
                                  header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE, 
                                  col.names = names_fmri)

# X needs to be a multi-dimensional array of trials as time points and electrodes, while Y equals the same time 
# values with voxel activations as spatial dimension 

X_npls_amp_a <- array(time_series_a_eeg, dim=c(144, 31))
Y_npls_a <- times_series_a_fmri

fita <- sNPLS(X_npls_amp_a, Y_npls_a, ncomp=2, keepJ = rep(2,2) , keepK = rep(1,2))

X_npls_amp_b <- array(time_series_b_eeg, dim=c(49, 31))
Y_npls_b <- time_series_b_fmri

fitb <- sNPLS(X_npls_amp_b, Y_npls_b, ncomp=2, keepJ = rep(2,2) , keepK = rep(1,2))

# Model using time freuquency results as EEG measure (same MRI voxel time series)

time_series_a_eeg_frequ <- read.table('EEG/time_frequency/txt/Sub1_frequency_A.txt', 
                                header = FALSE, sep = "", na.strings = "NA", dec = ",", strip.white = TRUE)

# Before using the frequency data, the data frame has to be transposed, so that rows equal the same time points as in
# the fMRI data set to ensure maximal covariance between these vectors

k <- seq(0, ncol(time_series_a_eeg_frequ), by = 144)
f <- seq(0, 930, by = 30)
elec <- 31

# As data is imported, the 30 frequencies are listed as rows and columns are trials for each electrode (144 x 31)
# Thus, a new data frame is created with transposed intervals of 144 trials over 30 frequencies from the old data frame
# in each row, so that each electrode's values are entered with each iteration of the loop

for (i in 1:31){
  if (i==1) {timef_eeg <- data.frame(matrix(data = NA, ncol = 930, nrow = 144))}
  timef_eeg[,(f[i]+1):(f[i+1])] <- t(time_series_a_eeg_frequ[,(k[i]+1):(k[i+1])])
}

# Again, the EEG data is included as a multi-dimensional array with trials x frequencies x electrodes
# Before that, the data frame for the three-dimensional array is converted to atomic vectors and then subdivided by
# the provided sizes for its dimensions

X_npls_a_frequ <- array(unlist(timef_eeg), dim=c(144, 30, 31))
Y_npls_a <- time_series_a_fmri

fit_frequ <- sNPLS(X_npls_a_frequ, Y_npls_a, ncomp=3, keepJ = rep(2,3) , keepK = rep(1,3))
