#####
##### Script and examples for first testing EEG and fMRI times series for autocorrelation, then
##### calculating a block bootstrap method (for cases of weak dependence of observations) for resampling eeg and fmri 
##### time series and lastly correlating both fMRI time courses with time varying EEG frequency spectrum and with 
##### time varying amplitudes (separated by conditions) with an examplary subject
##### Finally, the script compares the relation of fMRI and amplitude variation with the one between fMRI and EEG frequency
##### 

library(boot)

# Load EEG and fMRI times series data (in case of fmri reduced to cortical regions)
setwd('/Volumes/INTENSO/DPX_EEG_fMRI/')
time_series_fmri <- read.table('fMRI/output/sub2/sub2_single_trial_fmri_cortex.txt', 
                                  header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)
times_ab <- read.table('fMRI/output/sub2/sub2_fmri_times.txt', 
                       header = FALSE, sep = "", na.strings = "NA", dec = ".", strip.white = TRUE)

acols <- as.data.frame((times_ab[1:150,] >= -0.25 & times_ab[1:150,] <= 1.5))
bcols <- (times_ab[151:197,] >= -0.25 & times_ab[151:197,] <= 1.5)

times_a <- (which(apply(acols, 2, function(x) any(grepl(TRUE, x)))))
times_b <- (which(apply(bcols, 2, function(x) any(grepl(TRUE, x)))))

fmri_a <- time_series_fmri[times_a,]
fmri_b <- time_series_fmri[times_b,]

timef_eeg_a <- read.table('EEG/time_frequency/txt/Sub2_frequency_A.txt', 
                                      header = FALSE, sep = "", na.strings = "NA", dec = ",", strip.white = TRUE)
timef_eeg_b <- read.table('EEG/time_frequency/txt/Sub2_frequency_B.txt', 
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


# Test both time series for autocorrelation
# If both are tested negative, resampling and perumtation tests for time segments can be performed
arfit_eeg <- ar(timef_eeg, method = "burg", order.max = 25)
arfit_fmri <- ar(fmri_a, method = "burg", order.max = 25)

# To correlate time series, resample both data sets in blocks of points compensating for weak dependence of observations
# In this case, the resampling is not based on a fixed term, but on an empirical data model (i.e., basing
# resampling on data point and data resiudals distribution
# Necessary functions for simulations, statistics to be computed and post-blackening

# Create the function to be applied in the bootstrapping, determining statistics to be returned
stat <- function(tsb) {
  ar.fit <- ar(tsb, order.max = 50)
  c(ar.fit$order, mean(tsb), tsb)
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

logar_eeg <- ar(log(as.numeric((unlist(timef_eeg_a)))))
model_eeg <- list(order = c(logar_eeg$order, 0, 0), ar = logar_eeg$ar)
model_eeg_res <- logar_eeg$resid[!is.na(logar_eeg$resid)]
model_eeg_res <- model_eeg_res - mean(model_eeg_res)

# Resampling without post-blackening
boot_block_eeg <- tsboot(model_eeg_res, stat, R = 99, sim = "model", n.sim = 114,
                   orig.t = FALSE, ran.gen = sim, 
                   ran.args = list(ts = log(as.numeric(unlist(timef_eeg_a))), model = model_eeg))

# Resampling with post-blackening
boot_block_eeg_black <- tsboot(model_eeg_res, stat, R = 99, l = 20, sim = "fixed",
                  n.sim = 114, orig.t = FALSE, ran.gen = black, 
                  ran.args = list(ts = log(as.numeric(unlist(timef_eeg_a))), model = model_eeg))

# To compare the two models, check on fit to original data points (superior with post-blackening)
table(boot_block_eeg$t[, 1])
table(boot_block_eeg_black$t[, 1])

### EEG amps

logar_amp <- ar(as.numeric(unlist(time_series_a_eeg_amp, use.names = FALSE)))
model_amp <- list(order = c(logar_amp$order, 0, 0), ar = logar_amp$ar)
model_amp_res <- logar_amp$resid[!is.na(logar_amp$resid)]
model_amp_res <- model_amp_res - mean(model_amp_res)

boot_block_amp_black <- tsboot(model_amp_res, stat, R = 99, l = 20, sim = "fixed",
                               n.sim = 114, orig.t = FALSE, ran.gen = black, 
                               ran.args = list(ts = as.numeric(unlist(time_series_a_eeg_amp)), model = model_amp))

### fMRI data

logar_fmri <- ar(log(as.numeric((unlist(fmri_a[1:143,])))))
model_fmri <- list(order = c(logar_fmri$order, 0, 0), ar = logar_fmri$ar)
model_fmri_res <- logar_fmri$resid[!is.na(logar_fmri$resid)]
model_fmri_res <- model_fmri_res - mean(model_fmri_res)

boot_block_fmri <- tsboot(model_fmri_res, stat, R = 99, sim = "model", n.sim = 114,
                         orig.t = FALSE, ran.gen = sim, 
                         ran.args = list(ts = log(as.numeric(unlist(fmri_a[1:142,]))), model = model_fmri))

boot_block_fmri_black <- tsboot(model_fmri_res, stat, R = 99, l = 20, sim = "fixed",
                               n.sim = 114, orig.t = FALSE, ran.gen = black, 
                               ran.args = list(ts = log(as.numeric(unlist(fmri_a[1:142,]))), model = model_fmri))

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
frequ_blocks <- boot_block_eeg_black$seed
amp_blocks <- boot_block_amp_black$seed
fmri_blocks <- boot_block_fmri_black$seed

ts_corr <- corperm(amp_blocks, fmri_blocks, plot=FALSE)
