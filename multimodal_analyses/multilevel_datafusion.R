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
library(arm)
lmm.data <- read.table("/Volumes/INTENSO/DPX_EEG_fMRI/multilevel/multimodal_param.txt", 
                       header = TRUE, sep = ",", na.strings = "NA", dec = ".", strip.white = TRUE)

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

model <- lmer(RT ~ EEG + MRI + trialtype:block + (1 | date), data = lmm.data)

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
