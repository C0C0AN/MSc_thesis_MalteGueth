# This section on reading data and creating tables, starting at this point has been written by José Alanis
# for usage in the section of neuropsychology
#############################################

setwd('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/')

paths <- dir('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/rawdata/', full.names = T)
names(paths) <- basename(paths)

rt_data <- plyr::ldply(paths, read.table, header = F, sep =',')

rt_data <- dplyr::rename(rt_data, 
                         ID = .id, 
                         Block = V2, 
                         Trial = V4, 
                         Trial_Type = V6, 
                         RT = V8, 
                         Reaction = V10)

rt_data <- dplyr::select(rt_data, ID, Block, Trial, Trial_Type, Reaction, RT)

rt_data$ID <- as.factor(rt_data$ID)
rt_data <- dplyr::arrange(rt_data, ID)
rt_data$Subject <- rep(1:13, each=208)
rt_data$Subject <- as.factor(rt_data$Subject)

rt_data$Reaction <- plyr::revalue(rt_data$Reaction, c(' hit' = 'correct', ' incorrect'='incorrect', ' miss'='too slow'))
rt_corrects <- dplyr::filter(rt_data, Reaction == 'correct')
rt_corrects$Trial_Type <- as.factor(rt_corrects$Trial_Type)

rt_corrects_average <- plyr::ddply(Corrects, c('Trial_Type'), dplyr::summarise,
                                Sum    = sum(!is.na(RT)),
                                Mean_RT = mean(RT),
                                sd   = sd(RT),
                                se   = sd / sqrt(Sum),
                                ci   = se * qt(.95/2 + .5, Sum-1)
)

#############################################
