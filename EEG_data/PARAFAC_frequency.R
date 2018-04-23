#####
##### Script and examples for PARAFAC factor analysis for multiway component models via alternating least squares 
##### algorithms with optional constraints (i.e., orgothonal component extraction depending on array dimension)
##### 

setwd('/Volumes/INTENSO/DPX_EEG_fMRI/')
time_series_a_eeg_frequ <- read.table('EEG/time_frequency/txt/Sub2_frequency_A.txt', 
                                      header = FALSE, sep = "", na.strings = "NA", dec = ",", strip.white = TRUE)
time_series_b_eeg_frequ <- read.table('EEG/time_frequency/txt/Sub2_frequency_B.txt', 
                                      header = FALSE, sep = "", na.strings = "NA", dec = ",", strip.white = TRUE)

# Build PARAFAC model and test the model fit for different component numbers

timef_eeg_a <- time_series_a_eeg_frequ[1:142,]
timef_eeg_b <- time_series_b_eeg_frequ[1:43,]

Xa = array(as.numeric(unlist(timef_eeg_a)), dim=c(142, 30, 31))
Xb = array(as.numeric(unlist(timef_eeg_b)), dim=c(43, 30, 31))

pfac_a2 <- parafac(Xa,nfac=2,nstart=1, const = c(0,1,1))
pfac_b2 <- parafac(Xb,nfac=2,nstart=1, const = c(0,1,1))

pfac_a3 <- parafac(Xa,nfac=3,nstart=1, const = c(0,1,1))
pfac_b3 <- parafac(Xb,nfac=3,nstart=1, const = c(0,1,1))

# Check solution
Xhat_a2 <- fitted(pfac_a2)
Xhat_b2 <- fitted(pfac_b2)

Xhat_a3 <- fitted(pfac_a2)
Xhat_b3 <- fitted(pfac_b2)

# Calculate the Corcodndia cirterium fit, Bro's and Kiers’s core consistency diagnostic
corcondia(Xa, pfac_a2, divisor=c("nfac","core"))
corcondia(Xa, pfac_a3, divisor=c("nfac","core"))

corcondia(Xb, pfac_b2, divisor=c("nfac","core"))
corcondia(Xb, pfac_b3, divisor=c("nfac","core"))

# Plot the distibution of a component's power over EEG spectrum (1-30 Hz)

power_spec = range(-2.5, 2.5)
frequencies = range(1, 30)
xlab = 'Frequency [Hz]'
ylab = 'Power'

plot(pfac_a2$B, type = "n", ylim = power_spec, xlim = frequencies,
     xlab = xlab, ylab = ylab, lwd = 5)
lines(pfac_a2$B[, 1], col='darkred')
lines(pfac_a2$B[, 2], col='deepskyblue4')
rect(3,-4,5,4,col = rgb(0.5,0.5,0.5,1/4))
rect(10,-4,12,4,col = rgb(0.5,0.5,0.5,1/4))
legend(list(x = 2,y = 2.5), legend = c("Component 1", "Component 2"), pch = 15, bty = "o", 
       col = c('darkred', 'deepskyblue4'))

plot(pfac_b2$B, type = "n", ylim = power_spec, xlim = frequencies,
     xlab = xlab, ylab = ylab, lwd = 5)
lines(pfac_b2$B[, 1], col='darkred')
lines(pfac_b2$B[, 2], col='deepskyblue4')
rect(6,-4,8,4,col = rgb(0.5,0.5,0.5,1/4))
rect(3,-4,5,4,col = rgb(0.5,0.5,0.5,1/4))
legend(list(x = 2,y = -1.5), legend = c("Component 1", "Component 2"), pch = 15, bty = "o", 
       col = c('deepskyblue4', 'darkred'))
