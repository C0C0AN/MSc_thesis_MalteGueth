#####
##### Code snippets for processing behavioral data
##### 

# Read in reaction times and reaction types by block, trial and trialtype ('rawdata.txt')
# Get some basic descriptive and inferential statistics

# This section on reading data and creating tables, starting at this point has been written by José Alanis
# for usage in the section of neuropsychology (https://github.com/JoseAlanis)
#############################################

setwd('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/')

paths <- dir('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/rawdata/', full.names = T)
names(paths) <- basename(paths)

rt_data <- plyr::ldply(paths, read.table, header = F, sep =',')

rt_data <- dplyr::rename(rt_data, 
                         ID = .id, 
                         Block = V2, 
                         Trial = V4, 
                         trialtype = V6, 
                         RT = V10, 
                         Reaction = V12)

rt_data <- dplyr::select(rt_data, ID, Block, Trial, trialtype, Reaction, RT)

rt_data$ID <- as.factor(rt_data$ID)
rt_data <- dplyr::arrange(rt_data, ID)
rt_data$Subject <- rep(1:13, each=208)
rt_data$Subject <- as.factor(rt_data$Subject)

rt_data$Reaction <- plyr::revalue(rt_data$Reaction, c(' hit' = 'correct', ' incorrect'='incorrect', ' miss'='too slow'))
rt_corrects <- dplyr::filter(rt_data, Reaction == 'correct')
rt_corrects$trialtype <- as.factor(rt_corrects$trialtype)

rt_corrects_average1 <- plyr::ddply(rt_corrects, c('trialtype'), dplyr::summarise,
                                   Sum    = sum(!is.na(RT)),
                                   Mean_RT = mean(RT),
                                   sd   = sd(RT),
                                   se   = sd / sqrt(Sum),
                                   ci   = se * qt(.95/2 + .5, Sum-1)
)

rt_corrects_average2 <- plyr::ddply(rt_corrects, c('trialtype', 'Block'), dplyr::summarise,
                                    Sum    = sum(!is.na(RT)),
                                    Mean_RT = mean(RT),
                                    sd   = sd(RT),
                                    se   = sd / sqrt(Sum),
                                    ci   = se * qt(.95/2 + .5, Sum-1)
)

#############################################

# Test multiple models to check that the different trialtypes or blocks have a significant effect
# and create bar chart with standard error

MLnoIntercept <- glm(RT ~ Block + trialtype, data = rt_corrects) # ML model
print(MLnoIntercept)
anova(MLnoIntercept, test = "F")

ML <- glm(RT ~ Block + trialtype:Block, data = rt_corrects)
anova(ML, test = "F")

require(ggplot2)
require(viridis)
ggplot(rt_corrects_average2, aes(x = Block, y = Mean_RT, fill = trialtype),
       condition = trialtype) + 
  geom_bar(position = position_dodge(), stat = 'identity') +
  geom_errorbar(aes(ymin=Mean_RT - se, ymax=Mean_RT+se), width=.2, position = position_dodge(.9)) +
  scale_fill_viridis(option = 'B', discrete = T, begin = 0.15, end = .85) +
  coord_cartesian(ylim = c(300, 550))
