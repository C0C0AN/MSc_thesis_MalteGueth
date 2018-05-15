#####
##### Script snippets for multilevel modeling and model sequence
##### 

# EEG, MRI and multimodal parameters are meant to be entered (see multimodal_param.txt), with EEG either.
# spectral or ERP derivates and MRI for instance as voxel intensity from contrasts.
# Attempt to predict variance in behavioral data (RT, ER or PSI) with different neuronal (unimodal and multimodal)
# parameters.

# Data has to be arranged in the long data format with each trial of a subject nested within a type, nested within
# one of four blocks. In addition, to behavioral data (reaction time, error rate, proactive shift index)
# electrophysiological and neuroimaging can be added as parametric regressors on a single-trial level nested within
# the aforementioned grouping variables.

library(lme4)
library(car)
library(plyr)
library(r2glmm)

# Load behavioral data with block and cuetype numbers

RT <- read.table('Behavioral_Data/Rtables/rt_corrects_single_trial_multilevel.txt', 
                 header = TRUE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)

# Load fMRI data

ts_fmri_mfg <- read.table('fMRI/output/ts/single_trial_fmri_mfg.txt', 
                              header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
ts_fmri_ifg <- read.table('fMRI/output/ts/single_trial_fmri_infFGtriangularis.txt', 
                              header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)

ts_fmri_dlpfc <- data.frame(rowMeans(ts_fmri_mfg[1:1087,]), rowMeans(ts_fmri_ifg[1:1087,]))

times_ab <- read.table('fMRI/output/times/all_fmri_times.txt', 
                       header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)

acols <- as.data.frame((times_ab[1:1924,] >= 0 & times_ab[1:1924,] <= 1.5))
bcols <- (times_ab[1925:2535,] >= 0 & times_ab[1925:2535,] <= 1.5)

times_a <- (which(apply(acols, 2, function(x) any(grepl(TRUE, x)))))
times_b <- (which(apply(bcols, 2, function(x) any(grepl(TRUE, x)))))
                        
ts_fmri_a_dlpfc <- data.frame(ts_fmri_dlpfc[times_a[1:1924],])
ts_fmri_b_dlpfc <- data.frame(ts_fmri_dlpfc[times_b[1925:2535],])

names(ts_fmri_a_dlpfc)[1] <- "V1"
names(ts_fmri_b_dlpfc)[1] <- "V1"
ts_fmri_dlpfc <- rbind(ts_fmri_a_dlpfc, ts_fmri_b_dlpfc)
                        
# Load EEG data
                        
pathsa <- dir('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/time_frequency/txt/signatures/A/', full.names = T)
names(pathsa) <- basename(pathsa)
timef_eeg_a <- plyr::ldply(pathsa, read.table, header = F, sep ='')

pathsb <- dir('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/time_frequency/txt/signatures/B/', full.names = T)
names(pathsb) <- basename(pathsb)
timef_eeg_b <- plyr::ldply(pathsb, read.table, header = F, sep ='')

ts_eeg <- data.frame(c(timef_eeg_a, timef_eeg_b))
                        
# Combine all
                        
lmm.data <- data.frame(as.numeric(as.character(unlist(ts_eeg))),
                       as.numeric(as.character(unlist(ts_fmri_preCG))),
                       as.numeric(as.character(RT))
)

lmm.data$block <- as.factor(c(rep(c(rep(0,35), rep(1,35), rep(2,35), rep(3,37)),13), 
                    rep(c(rep(0,10), rep(1,10), rep(2,10), rep(3,13)),13)))

lmm.data$type <- as.factor(c(rep(0,1846), rep(1,559)))

names(lmm.data)[1] <- "alpha"
names(lmm.data)[2] <- "preCG"
names(lmm.data)[3] <- "RT"
lmm.data$type <- RT$type
lmm.data$block <- RT$block

# Different Non-multilevel model specifications

OLSexamp <- lm(RT ~ EEG + MRI + trialtype, data = lmm.data) # OLS model
MLnoIntercept <- glm(RT ~ EEG + MRI + trialtype, data = lmm.data) # ML model

# For a first elaboration step, let intercepts vary as fixed effect for blocks or runs  
# Get difference in model deviance from the first to the second ML model or its AIC

MLplusIntercept <- glm(RT ~ EEG + MRI + trialtype + block, data = lmm.data)
anova(MLnoIntercept, MLplusIntercept, test = "F")
AIC(MLplusIntercept)

# For next elaboration specify an interaction of block and trial type

MLwithInt <- glm(RT ~ EEG + MRI + trialtype:block, data = lmm.data)

# Now you could already test a sequence of models for incremental improvements to deviance, AIC or RMSE

ML1 <- glm(RT ~ EEG + trialtype:block, data = lmm.data)
ML2 <- glm(RT ~ EEG + MRI + trialtype:block, data = lmm.data)
ML3 <- glm(RT ~ EEG + MRI + jICA + trialtype:block, data = lmm.data)
anova(ML1, ML2, ML3, test = "F")

# Now for random effects, model random slopes with plyr with dlply ...

require(plyr)
model <- dlply(lmm.data, .(time, date), function(x) glm(RT ~ EEG + MRI + trialtype:block, data = x))

# ... or use lmer with (1|group effect) 

model1 <- lmer(as.numeric(RT) ~ (1 | block/type), data = lme_data, REML=FALSE)
model2 <- lmer(as.numeric(RT) ~ alpha + (1 | block/type), data = lme_data, REML=FALSE)
model3 <- lmer(as.numeric(RT) ~ alpha + preCG + (1 | block/type), data = lme_data, REML=FALSE)
sum <- anova(model1, model2, model3, test = 'F')

mod1r <- r2beta(model1, method = 'nsj')
mod2r <- r2beta(model2, method = 'nsj')
mod3r <- r2beta(model3, method = 'nsj')

r2diff <- r2dt(x=mod3r, y = mod2r, cor = TRUE)
               
# To modify random effects (varying intercepts for grouping variables) include grouping terms 
# (1|date/time) fits a varying intercept model for dates and test times nested 
# within dates

model <- lmer(RT ~ EEG + MRI + trialtype:block + (1 | date), data = lmm.data)

# Fit multiple group effects with multiple group effect terms for experiment date and time

model <- lmer(RT ~ EEG + MRI + trialtype:block + (1 | date) + (1 | time), 
                  data = lmm.data)

# Fit nested group effect terms through (1|level 1 group variable/level 2 group variable) 
# (1|date/time) means we want to fit a mixed effect term for varying intercepts 1| by dates, 
# and for times that are nested within dates

model <- lmer(RT ~ EEG + MRI + trialtype:block + (1 | date/time), data = lmm.data)

# For varying slope model modify random effect term to include variables before the grouping terms
# (1 + trialtype|date/time) tells R to fit a varying slope and varying intercept model for dates and test times 
# nested within dates, and to allow the slope of trialtypes to vary by date

model <- lmer(RT ~ EEG + MRI + trialtype:block + (1 + trialtype | date/time), 
                  data = lmm.data)

# Alternatively, to make a little more sense of nesting, here, each subject has four blocks and four trialtypes
# nested within these blocks of a subject

model <- lmer(RT ~ ID + EEG + MRI + trialtype:block + (1 + ID | block/trialtype), 
              data = lmm.data)
