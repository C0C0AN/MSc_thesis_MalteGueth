#####
##### Code snippets for processing behavioral data
##### 

# Read in reaction times and reaction types by block, trial and trialtype ('rawdata.txt')
# Get some basic descriptive and inferential statistics

# This section on reading data and creating tables, starting at this point has been written by Jose Alanis
# for usage in the section of neuropsychology (https://github.com/JoseAlanis)
#############################################

require(plyr)
require(dplyr)

setwd('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/')

paths <- dir('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/rawdata/', full.names = T)
names(paths) <- basename(paths)

rt_data <- ldply(paths, read.table, header = F, sep =',')

rt_data <- rename(rt_data, 
                   ID = .id, 
                   Block = V2, 
                   Trial = V4, 
                   trialtype = V6, 
                   RT = V10, 
                   Reaction = V12)

rt_data <- select(rt_data, ID, Block, Trial, trialtype, Reaction, RT)

rt_data$ID <- as.factor(rt_data$ID)
rt_data <- arrange(rt_data, ID)
rt_data$Subject <- rep(1:13, each=208)
rt_data$Subject <- as.factor(rt_data$Subject)

rt_data$Reaction <- revalue(rt_data$Reaction, c(' hit' = 'correct', ' incorrect'='incorrect', ' miss'='too slow'))
rt_corrects <- filter(rt_data, Reaction == 'correct')
rt_corrects$trialtype <- as.factor(rt_corrects$trialtype)

rt_corrects_average <- ddply(rt_corrects, c('trialtype'), summarise,
                             Sum    = sum(!is.na(RT)),
                             Mean_RT = mean(RT),
                             sd   = sd(RT),
                             se   = sd / sqrt(Sum),
                             ci   = se * qt(.95/2 + .5, Sum-1))

rt_corrects_average_subs <- ddply(rt_corrects, c('Subject', 'Block', 'trialtype'), summarise,
                                  Sum    = sum(!is.na(RT)),
                                  Mean_RT = mean(RT),
                                  sd   = sd(RT),
                                  se   = sd / sqrt(Sum),
                                  ci   = se * qt(.95/2 + .5, Sum-1))

rt_corrects_average_blocks <- ddply(rt_corrects, c('Block', 'trialtype'), summarise,
                                    Sum    = sum(!is.na(RT)),
                                    Mean_RT = mean(RT),
                                    sd   = sd(RT),
                                    se   = sd / sqrt(Sum),
                                    ci   = se * qt(.95/2 + .5, Sum-1))

#############################################

# Build new variable in averaged data frame for the proactive behavioral shift index (PSI)

require(tidyr)

PSI_RT <- filter(rt_corrects, trialtype %in% c(2, 3))
PSI_RT <- select(PSI_RT, Subject, Block, trialtype, RT)
PSI_RT <- spread(PSI_RT, trialtype, RT, drop = TRUE)

PSI_RT_blocks_subs <- filter(rt_corrects_average_subs, trialtype %in% c(2, 3))
PSI_RT_blocks_subs <- select(PSI_RT_blocks_subs, Subject, Block, trialtype, Mean_RT)
PSI_RT_blocks_subs <- spread(PSI_RT_blocks_subs, trialtype, Mean_RT, drop = TRUE)
PSI_RT_blocks_subs <- rename(PSI_RT_blocks_subs, RT_BX = '2', RT_AY = '3')

PSI_RT_blocks_subs$PSI <- (PSI_RT_blocks_subs$RT_AY - PSI_RT_blocks_subs$RT_BX)/
                                 (PSI_RT_blocks_subs$RT_AY + PSI_RT_blocks_subs$RT_BX)

PSI_RT_blocks <- ddply(PSI_blocks_subs, c('Block'), summarise,
                       Subs    = sum(!is.na(PSI)),
                       Mean_PSI = mean(PSI),
                       sd   = sd(PSI),
                       se   = sd / sqrt(Subs),
                       ci   = se * qt(.95/2 + .5, Subs-1))

# Build new data frame for errors and error rates by block and trialtype
# Each ER is calculated by dividing the error count by its respective frequency per block (AX = 34; BX, AY, BY = 6)

incorrects <- select(rt_data, Subject, Block, trialtype, Reaction)
incorrects$Reaction <- revalue(rt_data$Reaction, c('correct' = 0, 'incorrect'= 1, 'too slow'= 0))

incorrects_average <- ddply(incorrects, c('Subject', 'Block', 'trialtype'), summarise,
                            Errors    = sum(Reaction == 1))

# Implement the correction formula put forth by Braver et al. (2009) for errors per trialtype and block 
# equaling zero to ease further calculations (so there is no need to work with zero values)

corrAX <- (0.5)/(34 + 1)
corrBXAYBY <- (0.5)/(6 + 1)

incorrects_average$Errors <- ifelse(incorrects_average$trialtype == 1 & incorrects_average$Errors == 0, corrAX,
                                    ifelse(incorrects_average$trialtype >= 2 & incorrects_average$Errors == 0, 
                                           corrBXAYBY, incorrects_average$Errors))

incorrects_average$ER <- ifelse(incorrects_average$trialtype == 1, (incorrects_average$Errors/34),
                                ifelse(incorrects_average$trialtype >= 2, (incorrects_average$Errors/6),
                                       incorrects_average$Errors))

incorrects_average_blocks_errors <- ddply(incorrects_average, c('Block', 'trialtype'), summarise,
                                          Subs    = sum(!is.na(Errors)),
                                          Mean_Errors = mean(Errors),
                                          sd   = sd(Errors),
                                          se   = sd / sqrt(Subs),
                                          ci   = se * qt(.95/2 + .5, Subs-1))

incorrects_average_blocks <- ddply(incorrects_average, c('Block', 'trialtype'), summarise,
                                   Subs    = sum(!is.na(ER)),
                                   Mean_ER = mean(ER),
                                   sd   = sd(ER),
                                   se   = sd / sqrt(Subs),
                                   ci   = se * qt(.95/2 + .5, Subs-1))

incorrects_average_blocks_errors$trialtype <- as.factor(incorrects_average_blocks_errors$trialtype)
incorrects_average_blocks$trialtype <- as.factor(incorrects_average_blocks$trialtype)

# Now for the PSI based on the total error count instead of RT

PSI_Errors_blocks_subs <- dplyr::select(incorrects_average, Subject, Block, trialtype, Errors)
PSI_Errors_blocks_subs <- dplyr::filter(PSI_Errors_blocks_subs, trialtype %in% c(2, 3))
PSI_Errors_blocks_subs <- spread(PSI_Errors_blocks_subs, trialtype, Errors, drop = TRUE)
PSI_Errors_blocks_subs <- dplyr::rename(PSI_Errors_blocks_subs, Errors_BX = '2', Errors_AY = '3')

PSI_Errors_blocks_subs$PSI <- (PSI_Errors_blocks_subs$Errors_AY - PSI_Errors_blocks_subs$Errors_BX)/
  (PSI_Errors_blocks_subs$Errors_AY + PSI_Errors_blocks_subs$Errors_BX)

PSI_Errors_blocks <- ddply(PSI_Errors_blocks_subs, c('Block'), summarise,
                           Subs    = sum(!is.na(PSI)),
                           Mean_PSI = mean(PSI),
                           sd   = sd(PSI),
                           se   = sd / sqrt(Subs),
                           ci   = se * qt(.95/2 + .5, Subs-1))

# Lastly, also calculate the PSI but based on ER

PSI_ER_blocks_subs <- select(incorrects_average, Subject, Block, trialtype, ER)
PSI_ER_blocks_subs <- filter(PSI_ER_blocks_subs, trialtype %in% c(2, 3))
PSI_ER_blocks_subs <- spread(PSI_ER_blocks_subs, trialtype, ER, drop = TRUE)
PSI_ER_blocks_subs <- rename(PSI_ER_blocks_subs, ER_BX = '2', ER_AY = '3')

PSI_ER_blocks_subs$PSI <- (PSI_ER_blocks_subs$ER_AY - PSI_ER_blocks_subs$ER_BX)/
  (PSI_ER_blocks_subs$ER_AY + PSI_ER_blocks_subs$ER_BX)

PSI_ER_blocks <- ddply(PSI_ER_blocks_subs, c('Block'), summarise,
                       Subs    = sum(!is.na(PSI)),
                       Mean_PSI = mean(PSI),
                       sd   = sd(PSI),
                       se   = sd / sqrt(Subs),
                       ci   = se * qt(.95/2 + .5, Subs-1))

# Formulate statistcial model equations and perform inferential tests with a general linear model
# Factors are either trialtype and/or block, depending on if PSI, RT, error counts and ER are dependent variables
# For that purpose, enter data frames with single subject values for the dependent variable

# Reaction times

MLRT <- glm(RT ~ Block + trialtype + trialtype:Block, data = rt_corrects) # ML model with main effects and interaction term
anova(MLRT, test = "F")

MLPSI <- glm(PSI ~ Block, data = PSI_RT_blocks_subs) # ML model for PSI based on RT with main effect for block
anova(MLPSI, test = "F")

# Error rates and total error counts

MLErrors <- glm(Errors ~ Block + trialtype + trialtype:Block, data = incorrects_average) # ML model for ER with main effects and interaction terms
anova(MLErrors, test = "F")

MLER <- glm(ER ~ Block + trialtype + trialtype:Block, data = incorrects_average) # ML model for ER with main effects and interaction terms
anova(MLER, test = "F")

MLErrorsPSI <- glm(PSI ~ Block, data = PSI_Errors_blocks_subs) # ML model for ER with main effects and interaction terms
anova(MLErrorsPSI, test = "F")

MLERPSI <- glm(PSI ~ Block, data = PSI_ER_blocks_subs) # ML model for ER with main effects and interaction terms
anova(MLERPSI, test = "F")

# Create bar plots with ggplot2 for RT, PSI and ER models

# RT and PSI for RT

require(ggplot2)
require(viridis)
ggplot(rt_corrects_average_blocks, aes(x = Block, y = Mean_RT, fill = trialtype),
       condition = trialtype) + 
  geom_bar(position = position_dodge(), stat = 'identity') +
  geom_errorbar(aes(ymin=Mean_RT-se, ymax=Mean_RT+se), width=.2, position = position_dodge(.9)) +
  scale_fill_viridis(option = 'B', discrete = T, begin = 0.15, end = .85, 
                     labels=c("AX", "BX", "AY","BY")) +
  coord_cartesian(ylim = c(300, 550)) +
  labs(x = "block", y = "reaction times [ms]") +
  theme_classic()

ggsave('./Rplots/rt_bar_graph.pdf', plot=last_plot(), width=7.85, height=5.83) 

ggplot(PSI_RT_blocks, aes(x = Block, y = Mean_PSI)) + 
  geom_bar(position = position_dodge(), stat = 'identity', fill="steelblue") +
  geom_errorbar(aes(ymin=Mean_PSI-se, ymax=Mean_PSI+se), width=.2, position = position_dodge(.9)) +
  coord_cartesian(ylim = c(0.1, 0.25)) +
  labs(x = "block", y = "proactive behavioral shift index (PSI) for reaction times") +
  theme_classic()

ggsave('./Rplots/psi_rt_bar_graph.pdf', plot=last_plot(), width=7.85, height=5.83) 

# Errors and PSI for errors

ggplot(incorrects_average_blocks_errors, aes(x = Block, y = Mean_Errors, fill = trialtype),
       condition = trialtype) + 
  geom_bar(position = position_dodge(), stat = 'identity') +
  geom_errorbar(aes(ymin=Mean_Errors-se, ymax=Mean_Errors+se), width=.2, position = position_dodge(.9)) +
  scale_fill_viridis(option = 'B', discrete = T, begin = 0.15, end = .85, 
                     labels=c("AX", "BX", "AY","BY")) +
  coord_cartesian(ylim = c(0.1, 2.5)) +
  labs(x = "block", y = "error counts (average amount of errors per block)") +
  theme_classic()

ggsave('./Rplots/errors_bar_graph.pdf', plot=last_plot(), width=7.85, height=5.83) 

ggplot(PSI_Errors_blocks, aes(x = Block, y = Mean_PSI)) + 
  geom_bar(position = position_dodge(), stat = 'identity', fill="steelblue") +
  geom_errorbar(aes(ymin=Mean_PSI-se, ymax=Mean_PSI+se), width=.2, position = position_dodge(.9)) +
  coord_cartesian(ylim = c(0.01, 0.7)) +
  labs(x = "block", y = "proactive behavioral shift index (PSI) for errors") +
  theme_classic()

ggsave('./Rplots/psi_errors_bar_graph.pdf', plot=last_plot(), width=7.85, height=5.83) 

# ER and PSI for ER

ggplot(incorrects_average_blocks, aes(x = Block, y = Mean_ER, fill = trialtype),
       condition = trialtype) + 
  geom_bar(position = position_dodge(), stat = 'identity') +
  geom_errorbar(aes(ymin=Mean_ER-se, ymax=Mean_ER+se), width=.2, position = position_dodge(.9)) +
  scale_fill_viridis(option = 'B', discrete = T, begin = 0.15, end = .85, 
                     labels=c("AX", "BX", "AY","BY")) +
  coord_cartesian(ylim = c(0.005, 0.25)) +
  labs(x = "block", y = "error rates (average amount of errors per block)") +
  theme_classic()

ggsave('./Rplots/er_bar_graph.pdf', plot=last_plot(), width=7.85, height=5.83) 

ggplot(PSI_ER_blocks, aes(x = Block, y = Mean_PSI)) + 
  geom_bar(position = position_dodge(), stat = 'identity', fill="steelblue") +
  geom_errorbar(aes(ymin=Mean_PSI-se, ymax=Mean_PSI+se), width=.2, position = position_dodge(.9)) +
  coord_cartesian(ylim = c(0.01, 0.7)) +
  labs(x = "block", y = "proactive behavioral shift index (PSI) for error rates") +
  theme_classic()

ggsave('./Rplots/psi_er_bar_graph.pdf', plot=last_plot(), width=7.85, height=5.83) 

# Write and save tables for later analyses

# RT
write.table(rt_corrects, './Rtables/rt_corrects_single_trial.txt', row.names = F, sep = '\t')
write.table(rt_corrects_average, './Rtables/rt_corrects_average.txt', row.names = F, sep = '\t')
write.table(rt_corrects_average_subs, './Rtables/rt_corrects_average_subs.txt', row.names = F, sep = '\t')
write.table(rt_corrects_average_blocks, './Rtables/rt_corrects_average_blocks.txt', row.names = F, sep = '\t')
write.table(PSI_RT_blocks, './Rtables/PSI_RT_blocks.txt', row.names = F, sep = '\t')
write.table(PSI_RT_blocks_subs, './Rtables/PSI_RT_blocks.txt', row.names = F, sep = '\t')

# Errors and ER
write.table(incorrects_average, './Rtables/incorrects_average.txt', row.names = F, sep = '\t')
write.table(incorrects_average_blocks, './Rtables/incorrects_average_blocks.txt', row.names = F, sep = '\t')
write.table(PSI_ER_blocks, './Rtables/PSI_ER_blocks.txt', row.names = F, sep = '\t')
write.table(PSI_ER_blocks_subs, './Rtables/PSI_ER_blocks_subs.txt', row.names = F, sep = '\t')

write.table(incorrects_average_blocks_errors, './Rtables/incorrects_average_blocks_errors.txt', row.names = F, sep = '\t')
write.table(PSI_Errors_blocks, './Rtables/PSI_Errors_blocks.txt', row.names = F, sep = '\t')
write.table(PSI_Errors_blocks_subs, './Rtables/PSI_Errors_blocks_subs.txt', row.names = F, sep = '\t')
