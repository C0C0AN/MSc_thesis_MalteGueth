#####
##### Script and examples for multiway partial least squares in R as recently implemented in the sNPLS package
##### by David Hervas (https://github.com/David-Hervas) in NPLS Regression with L1 Penalization
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
