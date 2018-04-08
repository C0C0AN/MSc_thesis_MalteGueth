#####
##### Code snippets for linear mixed effects regression as reported in the thesis paper
##### 

# Read in tables for RT, PSI and error data as processed in 'behavioral_descriptives_inferential.R'

require(lme4)
require(dplyr)
require(plyr)

# Read in RT data and arrange it
setwd('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/Rtables/')
rt_data <- read.table('rt_corrects_single_trial.txt', header=T)
rt_data <- select(rt_data, Subject, Block, trialtype, RT)
rt_data$trialtype <- as.factor(rt_data$trialtype)
rt_data$Block <- as.factor(rt_data$Block)

# Recode data so that block and trialtype have the range 0 to 3 for coding trialtypes for contrasts
rt_data$trialtype <- plyr::revalue(rt_data$trialtype, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))
rt_data$Block <- plyr::revalue(rt_data$Block, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))

# Read in error data and arrange it
errors_data <- read.table('incorrects_average.txt', header=T)
errors_data <- dplyr::select(errors_data, Subject, Block, trialtype, Errors)
errors_data$trialtype <- as.factor(errors_data$trialtype)
errors_data$Block <- as.factor(errors_data$Block)

# Recode data so that block and trialtype have the range 0 to 3 for coding trialtypes for contrasts
errors_data$trialtype <- plyr::revalue(errors_data$trialtype, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))
errors_data$Block <- plyr::revalue(errors_data$Block, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))

# Read in ER data and arrange it
er_data <- read.table('incorrects_average.txt', header=T)
er_data <- dplyr::select(er_data, Subject, Block, trialtype, ER)
er_data$trialtype <- as.factor(er_data$trialtype)
er_data$Block <- as.factor(er_data$Block)

# Recode data so that block and trialtype have the range 0 to 3 for coding trialtypes for contrasts
er_data$trialtype <- plyr::revalue(er_data$trialtype, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))
er_data$Block <- plyr::revalue(er_data$Block, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))

# Read in PSI for RT data and arrange it
psi_rt_data <- read.table('PSI_RT_blocks.txt', header=T)
psi_rt_data <- dplyr::select(psi_data, Subject, Block, PSI)
psi_rt_data$Block <- as.factor(psi_data$Block)

# Recode data so that block has the range 0 to 3 for coding trialtypes for contrasts
psi_rt_data$Block <- plyr::revalue(psi_rt_data$Block, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))

# Read in PSI for errors and arrange it
psi_errors_data <- read.table('PSI_Errors_blocks_subs.txt', header=T)
psi_errors_data <- dplyr::select(psi_errors_data, Subject, Block, PSI)
psi_errors_data$Block <- as.factor(psi_errors_data$Block)

# Recode data so that block has the range 0 to 3 for coding trialtypes for contrasts
psi_errors_data$Block <- plyr::revalue(psi_errors_data$Block, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))

# Read in PSI for ER data and arrange it
psi_er_data <- read.table('PSI_ER_blocks_subs.txt', header=T)
psi_er_data <- select(psi_er_data, Subject, Block, PSI)
psi_er_data$Block <- as.factor(psi_er_data$Block)

# Recode data so that block has the range 0 to 3 for coding trialtypes for contrasts
psi_er_data$Block <- revalue(psi_er_data$Block, c('1' = 0, '2' = 1, '3' = 2, '4' = 3))

# Set up regression equation with random slopes for trialtypes and intercepts for each block, 
# nested within each participant for each dependent variable

RT_lmm <- lmer(RT ~ trialtype + Block + (1 | Subject/Block), data = rt_data, REML = TRUE)
summary(RT_lmm)
Anova(RT_lmm)

Errors_lmm <- lmer(Errors ~ trialtype + Block + (1 | Subject/Block), data = errors_data, REML = TRUE)
summary(Errors_lmm)
Anova(Errors_lmm)

PSI_RT_lmm <- lmer(PSI ~ Block + (1 | Subject), data = psi_rt_data, REML = TRUE)
summary(PSI_RT_lmm)
Anova(PSI_RT_lmm)

PSI_Errors_lmm <- lmer(PSI ~ Block + (1 | Subject), data = psi_errors_data, REML = TRUE)
summary(PSI_Errors_lmm)
Anova(PSI_Errors_lmm)

PSI_ER_lmm <- lmer(PSI ~ Block + (1 | Subject), data = psi_er_data, REML = TRUE)
summary(PSI_ER_lmm)
Anova(PSI_ER_lmm)
