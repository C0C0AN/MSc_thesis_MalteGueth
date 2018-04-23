#####
##### Script and examples for first testing EEG and fMRI times series for autocorrelation, then
##### calculating a block bootstrap method (for cases of weak dependence of observations) for resampling eeg and fmri 
##### time series and lastly correlating both fMRI time courses with time varying EEG frequency spectrum and with 
##### time varying amplitudes (separated by conditions) with an examplary subject
##### Finally, the script compares the relation of fMRI and amplitude variation with the one between fMRI and EEG frequency
##### 

library(boot)
library(fpp)
library(ggplot2)

# Load EEG and fMRI times series data (in case of fmri reduced to cortical regions)
setwd('/Volumes/INTENSO/DPX_EEG_fMRI/')
time_series_fmri_mfg1 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_mfg_-36_18_40.txt', 
                                    header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_mfg2 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_mfg_38_18_40.txt', 
                                    header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_ifg1 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_infFGopercularis_-48_14_19.txt', 
                                  header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_ifg2 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_infFGopercularis_49_16_17.txt', 
                               header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_ifg3 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_infFGtriangularis_-46_27_11.txt', 
                                header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_ifg4 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_infFGtriangularis_48_28_9.txt', 
                                header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_postCG <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_postCenG_-0_-28_50.txt', 
                                    header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_supra1 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_postSupG_51_-40_31_roi.txt', 
                                    header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_fmri_supra2 <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_postSupG_-49_-47_31.txt', 
                                      header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)

time_series_fmri_fc <- data.frame(time_series_fmri_mfg1, time_series_fmri_mfg2, time_series_fmri_ifg1,
                               time_series_fmri_ifg2, time_series_fmri_ifg3, time_series_fmri_ifg4)
time_series_fmri_pc <- data.frame(time_series_fmri_postCG, time_series_fmri_supra1, time_series_fmri_supra2)
time_series_fmri_fc <- data.frame(rowMeans(time_series_fmri))
time_series_fmri_pc <- data.frame(rowMeans(time_series_fmri))

times_ab <- read.table('fMRI/output/sub2/sub2_fmri_times.txt', 
                       header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)

acols <- as.data.frame((times_ab[1:150,] >= -0.25 & times_ab[1:150,] <= 1.5))
bcols <- (times_ab[151:197,] >= -0.25 & times_ab[151:197,] <= 1.5)

times_a <- (which(apply(acols, 2, function(x) any(grepl(TRUE, x)))))
times_b <- (which(apply(bcols, 2, function(x) any(grepl(TRUE, x)))))

fmri_a_fc <- data.frame(time_series_fmri[times_a[1:142],])
fmri_b_fc <- data.frame(time_series_fmri[times_b[1:43],])
fmri_a_pc <- data.frame(time_series_fmri[times_a[1:142],])
fmri_b_pc <- data.frame(time_series_fmri[times_b[1:43],])

                        timef_frequ_a <- read.table('EEG/time_frequency/txt/signatures/Sub2_sign_A.txt', 
                                      header = FALSE, sep = "", na.strings = "NA", dec = ",", strip.white = TRUE)
timef_frequ_b <- read.table('EEG/time_frequency/txt/signatures/Sub2_sign_B.txt', 
                                      header = FALSE, sep = "", na.strings = "NA", dec = ",", strip.white = TRUE)

time_series_a_eeg_amp <- read.table("EEG/Rtables/A/sub2_mean_epoch_A.txt", 
                                    header = TRUE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_a_eeg_amp$subject <- NULL
time_series_a_eeg_amp$condition <- NULL
time_series_a_eeg_amp$epoch <- NULL

time_series_b_eeg_amp <- read.table("EEG/Rtables/B/sub2_mean_epoch_B.txt", 
                                    header = TRUE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
time_series_b_eeg_amp$subject <- NULL
time_series_b_eeg_amp$condition <- NULL
time_series_b_eeg_amp$epoch <- NULL


# Test both time series for autocorrelation or, more precisely, their residuals by fitting an autocorrelation model
# If both are tested negative, resampling and perumtation tests for time segments can be performed
arfit_eeg <- ar(timef_eeg[,55], method = "burg", order.max = 25)
arfit_fmri <- ar(fmri_a, method = "burg", order.max = 25)

# ... or use the forecasting package                      
                        
xts <- ts(timef_frequ_a[,55],start=1,frequency=142) #convert to a time series
yts <- ts(fmri_a,start=1,frequency=142) #convert to a time series

mod1 <- auto.arima(xts)
mod2 <- auto.arima(yts)

ccf(mod1$residuals, mod2$residuals)

# To correlate time series, resample both data sets in blocks of points compensating for weak dependence of observations
# In this case, the resampling is not based on a fixed term, but on an empirical data model (i.e., basing
# resampling on data point and data resiudals distribution
# Necessary functions for simulations, statistics to be computed and post-blackening

# Create the function to be applied in the bootstrapping, determining statistics to be returned
# Create the function to be applied in the bootstrapping, determining statistics to be returned
meanN <- function(df, n){
    df %>% group_by(G=(0:(n()-1))%/%n) %>%  summarise(mean=mean(df[,1])) %>% select(-G)
  }

stat <- function(tsb) {
  ar.fit <- ar(tsb, order.max = 25)
  c(ar.fit$order, mean(tsb), tsb)
}

stat2 <- function(tsb) {
  ar.fit <- ar(tsb, order.max = 20)
  mean_block <- meanN(tsb, (ar.fit$order*2+1))
  c(mean_block)
}

sim <- function(res, n.sim, ran.args) {
  rg1 <- function(n, res) sample(res, n, replace = TRUE)
  ts.orig <- ran.args$ts
  ts.mod <- ran.args$model
  mean(ts.orig)+ts(arima.sim(model = ts.mod, n = n.sim,
                             rand.gen = rg1, res = as.vector(res)))
}

black <- function(res, n.sim, ran.args) {
  ts.orig <- ran.args$ts
  ts.mod <- ran.args$model
  mean(ts.orig) + ts(arima.sim(model = ts.mod,n = n.sim,innov = res))
}


#### EEG frequs

logar_eeg_a <- ar(log(as.numeric((unlist(timef_eeg_a)))))
model_eeg_a <- list(order = c(logar_eeg_a$order, 0, 0), ar = logar_eeg_a$ar)
model_eeg_res_a <- logar_eeg_a$resid[!is.na(logar_eeg_a$resid)]
model_eeg_res_a <- model_eeg_res_a - mean(model_eeg_res_a)

# Resampling without post-blackening
boot_block_eeg_a <- tsboot(model_eeg_res_a, stat, R = 99, sim = "model", n.sim = 114,
                   orig.t = FALSE, ran.gen = sim, 
                   ran.args = list(ts = log(as.numeric(unlist(timef_eeg_a))), model = model_eeg_a))


# Resampling with post-blackening
boot_block_eeg_black_a<- tsboot(model_eeg_res_a, stat, R = 99, l = 20, sim = "fixed",
                  n.sim = 114, orig.t = FALSE, ran.gen = black, 
                  ran.args = list(ts = log(as.numeric(unlist(timef_eeg_a))), model = model_eeg_a))

# To compare the two models, check on fit to original data points (superior with post-blackening)
table(boot_block_eeg_a$t[, 1])
table(boot_block_eeg_black_a$t[, 1])

logar_eeg_b <- ar(log(as.numeric((unlist(timef_eeg_b)))))
model_eeg_b <- list(order = c(logar_eeg_b$order, 0, 0), ar = logar_eeg_b$ar)
model_eeg_res_b <- logar_eeg_b$resid[!is.na(logar_eeg_b$resid)]
model_eeg_res_b <- model_eeg_res_b - mean(model_eeg_res_b)

boot_block_eeg_black_b <- tsboot(model_eeg_res_b, stat, R = 99, l = 20, sim = "fixed",
                               n.sim = 114, orig.t = FALSE, ran.gen = black, 
                               ran.args = list(ts = log(as.numeric(unlist(timef_eeg_b))), model = model_eeg_b))         
               
### EEG amps

logar_amp_a <- ar(as.numeric(unlist(time_series_a_eeg_amp[,19], use.names = FALSE)))
model_amp_a <- list(order = c(logar_amp_a$order, 0, 0), ar = logar_amp_a$ar)
model_amp_res_a <- logar_amp_a$resid[!is.na(logar_amp_a$resid)]
model_amp_res_a <- model_amp_res_a - mean(model_amp_res_a)
                        
boot_block_amp_black_a <- tsboot(model_amp_res_a, stat, R = 99, l = 20, sim = "fixed",
                               n.sim = 114, orig.t = FALSE, ran.gen = black, 
                               ran.args = list(ts = as.numeric(unlist(time_series_a_eeg_amp[,19])), model = model_amp_a))

logar_amp_b <- ar(as.numeric(unlist(time_series_b_eeg_amp[,19], use.names = FALSE)))
model_amp_b <- list(order = c(logar_amp_b$order, 0, 0), ar = logar_amp_b$ar)
model_amp_res_b <- logar_amp_b$resid[!is.na(logar_amp_b$resid)]
model_amp_res_b <- model_amp_res_b - mean(model_amp_res_b)

boot_block_amp_black_b <- tsboot(model_amp_res_b, stat, R = 99, l = 20, sim = "fixed",
                                 n.sim = 114, orig.t = FALSE, ran.gen = black, 
                                 ran.args = list(ts = as.numeric(unlist(time_series_b_eeg_amp[,19])), model = model_amp_b))

### fMRI data fc

logar_fmri_a <- ar(log(as.numeric((unlist(fmri_a_fc[,1])))))
model_fmri_a <- list(order = c(logar_fmri_a$order, 0, 0), ar = logar_fmri_a$ar)
model_fmri_res_a <- logar_fmri_a$resid[!is.na(logar_fmri_a$resid)]
model_fmri_res_a <- model_fmri_res_a - mean(model_fmri_res_a)

boot_block_fmri_fc_black_a <- tsboot(model_fmri_res_a, stat, R = 99, l = 5, sim = "fixed",
                               n.sim = 114, orig.t = FALSE, ran.gen = black, 
                               ran.args = list(ts = log(as.numeric(unlist(fmri_a_fc[,1]))), model = model_fmri_a))

logar_fmri_b <- ar(log(as.numeric((unlist(fmri_b_fc[,1])))))
model_fmri_b <- list(order = c(logar_fmri_b$order, 0, 0), ar = logar_fmri_b$ar)
model_fmri_res_b <- logar_fmri_b$resid[!is.na(logar_fmri_b$resid)]
model_fmri_res_b <- model_fmri_res_b - mean(model_fmri_res_b)

boot_block_fmri_fc_black_b <- tsboot(model_fmri_res_b, stat, R = 99, l = 5, sim = "fixed",
                                  n.sim = 114, orig.t = FALSE, ran.gen = black, 
                                  ran.args = list(ts = log(as.numeric(unlist(fmri_b_fc[,1]))), model = model_fmri_b))

### fMRI data pc

logar_fmri_a <- ar(log(as.numeric((unlist(fmri_a_pc[,1])))))
model_fmri_a <- list(order = c(logar_fmri_a$order, 0, 0), ar = logar_fmri_a$ar)
model_fmri_res_a <- logar_fmri_a$resid[!is.na(logar_fmri_a$resid)]
model_fmri_res_a <- model_fmri_res_a - mean(model_fmri_res_a)

boot_block_fmri_pc_black_a <- tsboot(model_fmri_res_a, stat, R = 99, l = 5, sim = "fixed",
                                  n.sim = 114, orig.t = FALSE, ran.gen = black, 
                                  ran.args = list(ts = log(as.numeric(unlist(fmri_a_pc[,1]))), model = model_fmri_a))

logar_fmri_b <- ar(log(as.numeric((unlist(fmri_b_pc[,1])))))
model_fmri_b <- list(order = c(logar_fmri_b$order, 0, 0), ar = logar_fmri_b$ar)
model_fmri_res_b <- logar_fmri_b$resid[!is.na(logar_fmri_b$resid)]
model_fmri_res_b <- model_fmri_res_b - mean(model_fmri_res_b)

boot_block_fmri_pc_black_b <- tsboot(model_fmri_res_b, stat, R = 99, l = 5, sim = "fixed",
                                  n.sim = 114, orig.t = FALSE, ran.gen = black, 
                                  ran.args = list(ts = log(as.numeric(unlist(fmri_b_pc[,1]))), model = model_fmri_b))
                      
# Run perumtation of correlation tests

corperm <- function(x, y, N=1000, plot=FALSE){
  reps <- replicate(N, cor(sample(x), y))
  obs <- cor(x,y)
  p <- mean(reps > obs) # shortcut for sum(reps > obs)/N
  if(plot){
    hist(reps)
    abline(v=obs, col="red")
  }
  p
}

# Pick the newly sampled segments/blocks for correlation tests
frequ_blocks <- boot_block_eeg_black$t
amp_blocks <- boot_block_amp_black$t
fmri_blocks <- boot_block_fmri_black$t

ts_corr <- corperm(amp_blocks, fmri_blocks, plot=FALSE)
                        
# Concatenate data frames for plotting
# ... as raw time points
ts_a <- data.frame(t(rbind(c(as.numeric(as.character(unlist(timef_frequ_a[,55]))), 
                             as.numeric(as.character(unlist(timef_frequ_a[,56]))), 
                             as.numeric(as.character(unlist(timef_frequ_a[,57])))
                           ))))
ts_a$y <- t(rbind(c(fmri_a_fc[,1], fmri_a_fc[,1], fmri_a_fc[,1])))
ts_a$y2 <- t(rbind(c(fmri_a_pc[,1], fmri_a_pc[,1], fmri_a_pc[,1])))
names(ts_a)[1] <- "x"
ts_a$Frequency <- c(rep('Theta',142), rep('Alpha',142), rep('Beta',142))
ts_a$t <- c(seq(1,142), seq(1,142), seq(1,142))
ts_a$xcent <- (ts_a$x - mean(ts_a$x)) / sd(ts_a$x)
ts_a$ycent <- (ts_a$y - mean(ts_a$y)) / sd(ts_a$y)
ts_a$y2cent <- (ts_a$y2 - mean(ts_a$y2)) / sd(ts_a$y2)

ts_b <- data.frame(t(rbind(c(as.numeric(as.character(unlist(timef_frequ_b[,55]))), 
                             as.numeric(as.character(unlist(timef_frequ_b[,56]))), 
                             as.numeric(as.character(unlist(timef_frequ_b[,57])))
))))
ts_b$y <- t(rbind(c(fmri_b_fc[,1], fmri_b_fc[,1], fmri_b_fc[,1])))
ts_b$y2 <- t(rbind(c(fmri_b_pc[,1], fmri_b_pc[,1], fmri_b_pc[,1])))
names(ts_b)[1] <- "x"
ts_b$Frequency <- c(rep('Theta',43), rep('Alpha',43), rep('Beta',43))
ts_b$t <- c(seq(1,43), seq(1,43), seq(1,43))
ts_b$xcent <- ((ts_b$x - mean(ts_b$x)) / sd(ts_b$x))
ts_b$ycent <- (ts_b$y - mean(ts_b$y)) / sd(ts_b$y)
ts_b$y2cent <- (ts_b$y2 - mean(ts_b$y2)) / sd(ts_b$y2)

ggplot(ts_a, aes(xcent, ycent, color=Frequency)) + geom_point() +
  scale_colour_hue(l=50) + geom_smooth(method=lm, se=TRUE) +
  labs(x = "Centered EEG Frequency Power", y = "Centered fMRI TS DLPFC") +
  coord_cartesian(xlim = c(-1, 2), ylim = c(-2, 2)) +
  theme_classic()

ggplot(ts_b, aes(xcent, ycent, color=Frequency)) + geom_point() +
  scale_colour_hue(l=50) + geom_smooth(method=lm, se=TRUE) +
  labs(x = "Centered EEG Frequency Power", y = "Centered fMRI TS DLPFC") +
  coord_cartesian(xlim = c(-1.5, 2), ylim = c(-2, 2)) +
  theme_classic()

# ... amplitudes
ts_amp <- data.frame(t(rbind(c(as.numeric(as.character(unlist(time_series_a_eeg_amp[,19]))), 
                               as.numeric(as.character(unlist(time_series_b_eeg_amp[,19]))) 
))))
ts_amp$y <- t(rbind(c(fmri_a_fc[,1], fmri_b_fc[,1])))
ts_amp$y2 <- t(rbind(c(fmri_a_pc[,1], fmri_b_pc[,1])))
names(ts_amp)[1] <- "x"
ts_amp$Cue <- c(rep('A',142), rep('B',43))
ts_amp$t <- c(seq(1,142), seq(1,43))
ts_amp$xcent <- (ts_amp$x - mean(ts_amp$x)) / sd(ts_amp$x)
ts_amp$ycent <- (ts_amp$y - mean(ts_amp$y)) / sd(ts_amp$y)
ts_amp$y2cent <- (ts_amp$y2 - mean(ts_amp$y2)) / sd(ts_amp$y2)

ggplot(ts_amp, aes(xcent, ycent, color=Cue)) + geom_point() +
  scale_colour_hue(l=50) + geom_smooth(method=lm, se=TRUE) +
  labs(x = "Centered EEG Frequency Power", y = "Centered fMRI TS DLPFC") +
  coord_cartesian(xlim = c(-1, 2), ylim = c(-2, 2)) +
  theme_classic()
                        

# Finally, bring all relevant data columns together in a data frame of a specific condition, compute a cross
# correlation matrix for all time series data (using cff function) and plot correlated times series data
                        
all_ts_b <- data.frame(as.numeric(as.character(unlist(timef_frequ_b[,55]))), 
                     as.numeric(as.character(unlist(timef_frequ_b[,56]))),
                     as.numeric(as.character(unlist(time_series_b_eeg_amp[,19]))),
                     as.numeric(as.character(unlist(fmri_b_mfg[,1]))),
                     as.numeric(as.character(unlist(fmri_b_ifg[,1]))),
                     as.numeric(as.character(unlist(fmri_b_postcc[,1]))),
                     as.numeric(as.character(unlist(fmri_b_prepc[,1])))
)
names(all_ts_b)[1] <- "theta"
names(all_ts_b)[2] <- "alpha"
names(all_ts_b)[3] <- "amplitude"
names(all_ts_b)[4] <- "MFG"
names(all_ts_b)[5] <- "IFG"
names(all_ts_b)[6] <- "CC"
names(all_ts_b)[7] <- "preCG"
                        
all_ts_b$theta <- (all_ts_b$theta - mean(all_ts_b$theta)) / sd(all_ts_b$theta)
all_ts_b$alpha <- (all_ts_b$alpha - mean(all_ts_b$theta)) / sd(all_ts_b$alpha)
all_ts_b$amplitude <- (all_ts_b$amplitude - mean(all_ts_b$amplitude)) / sd(all_ts_b$amplitude)
all_ts_b$MFG <- (all_ts_b$MFG - mean(all_ts_b$MFG)) / sd(all_ts_b$MFG)
all_ts_b$IFG <- (all_ts_b$IFG - mean(all_ts_b$IFG)) / sd(all_ts_b$IFG)
all_ts_b$CC <- (all_ts_b$CC - mean(all_ts_b$CC)) / sd(all_ts_b$CC)
all_ts_b$preCG <- (all_ts_b$preCG - mean(all_ts_b$preCG)) / sd(all_ts_b$preCG)

correlationTable = function(graphs) {
  cross = matrix(nrow = length(graphs), ncol = length(graphs))
  for(graph1Id in 1:length(graphs)){
    graph1 = graphs[[graph1Id]]
    print(graph1Id)
    for(graph2Id in 1:length(graphs)) {
      graph2 = graphs[[graph2Id]]
      if(graph1Id == graph2Id){
        break;
      } else {
        correlation = ccf(graph1, graph2, lag.max = 0)
        cross[graph1Id, graph2Id] = correlation$acf[1]
      }
    }
  }
  cross
}

corr = correlationTable(all_ts_b)

findCorrelated = function(orig, highCorr){
  match = highCorr[highCorr[,1] == orig | highCorr[,2] == orig,]
  match = as.vector(match)
  match[match != orig]
}

highCorr = which(corr > 0.4 | corr < -0.4 , arr.ind = TRUE)
match = findCorrelated(1, highCorr)
match

bound = function(graphs, orign, match) {
  graphOrign = graphs[[orign]]
  graphMatch = graphs[match]
  allValue = c(graphOrign)
  for(m in graphMatch){
    allValue = c(allValue, m)
  }
  c(min(allValue), max(allValue))
}

plotSimilar = function(graphs, orign, match){
  lim = bound(graphs, orign, match)
  
  graphOrign = graphs[[orign]]
  plot(ts(graphOrign), ylim=lim, xlim=c(1,length(graphOrign)), lwd=3)
  title(paste("Similar to", orign, "(black bold)"))
  
  cols = c()
  names = c()
  for(i in 1:length(match)) {
    m = match[[i]]
    matchGraph = graphs[[m]]
    lines(x = 1:length(matchGraph), y=matchGraph, col=i)
    
    cols = c(cols, i)
    names = c(names, paste0(m))
  }
  legend("topright", names, col = cols, lty=c(1,1))
}

plotSimilar(all_ts_b, 4, match)

########### Stats for correlations
df <- length(graphs) - 2
t <- sqrt(df) * 0.9/sqrt(1 - 0.9^2)
p <- 2 * min(pt(t, df), pt(t, df, lower.tail = FALSE))
