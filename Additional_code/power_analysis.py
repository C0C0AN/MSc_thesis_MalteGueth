"""
Created on Fri Nov 10 06:25:12 2017
@author: Malte
"""

# Two ways of calculating the necessary sample size for a given effect, (group) variances,
# and a desired power in a simple t-test

# The first script is recreating the existing approach implemented in an R function power.prop.test 
# Original post Matt Alcock on stackoverflow: https://i.stack.imgur.com/8q6Cb.gif

from scipy.stats import norm, zscore

def sample_power_probtest(p1, p2, power=0.8, sig=0.05):
    z = norm.isf([sig/2]) #two-sided t test
    zp = -1 * norm.isf([power]) 
    d = (p1-p2)
    s =2*((p1+p2) /2)*(1-((p1+p2) /2))
    n = s * ((zp + z)**2) / (d**2)
    return int(round(n[0]))

def sample_power_difftest(d, s, power=0.8, sig=0.05):
    z = norm.isf([sig/2]) 
    zp = -1 * norm.isf([power])
    n = (2*(s**2)) * ((zp + z)**2) / (d**2)
    return int(round(n[0]))

if __name__ == '__main__':

    n = sample_power_probtest(0.35, 0.5, power=0.9, sig=0.05)
    print n 

    n = sample_power_difftest(0.25, 0.6, power=0.9, sig=0.05)
    print n 
    

# The second script is an iterative approach using scipy.stats.
# This script gives out the achieved power with an increasing n per group until
# the desired power level is reached.
# Original post: http://www.djmannion.net/psych_programming/data/power/power.html

import numpy as np

import scipy.stats

# start at 70 participants
n_per_group = 70

# effect size = 0.25
group_means = [0.25, 0.5]
group_sigmas = [0.65, 0.65]

n_groups = len(group_means)

# number of simulations
n_sims = 10000

# power level that we would like to reach
desired_power = 0.9

# initialise the power for the current sample size to a small value
current_power = 0.0

# keep iterating until desired power is obtained
while current_power < desired_power:

    data = np.empty([n_sims, n_per_group, n_groups])
    data.fill(np.nan)

    for i_group in range(n_groups):

        data[:, :, i_group] = np.random.normal(
            loc=group_means[i_group],
            scale=group_sigmas[i_group],
            size=[n_sims, n_per_group]
        )

    result = scipy.stats.ttest_ind(
        data[:, :, 0],
        data[:, :, 1],
        axis=1
    )

    sim_p = result[1]

    # number of simulations where the null was rejected
    n_rej = np.sum(sim_p < 0.05)

    prop_rej = n_rej / float(n_sims)

    current_power = prop_rej

    print "With {n:d} samples per group, power = {p:.3f}".format(
        n=n_per_group,
        p=current_power
    )

    # increase the number of samples by one for the next iteration of the loop
    n_per_group += 1
