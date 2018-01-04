# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 06:25:12 2017

@author: Malte
"""


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
    
    

from statsmodels.stats.power import tt_ind_solve_power

mean_diff, sd_diff = 0.25, 0.55
std_effect_size = mean_diff / sd_diff

n = tt_ind_solve_power(effect_size=std_effect_size, alpha=0.05, power=0.9, ratio=1, alternative='two-sided')
print('Number in *each* group: {:.5f}'.format(n))




import numpy as np

import scipy.stats

# start at 20 participants
n_per_group = 70

# effect size = 0.8
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

# this is a bit tricky
# what we want to save is an array with 2 columns, but we have 2 different 1D
# arrays. here, we use the 'np.newaxis' property to add a column each of the
# two 1D arrays, and then 'stack' them horizontally
array_to_save = np.hstack(
    [
        ns_per_group[:, np.newaxis],
        power[:, np.newaxis]
    ]
)

power_path = "prog_data_vis_power_sim_data.tsv"

np.savetxt(
    power_path,
    array_to_save,
    delimiter="\t",
    header="Simulated power as a function of samples per group"
)


import numpy as np

power_path = "prog_data_vis_power_sim_data.tsv"

power = np.loadtxt(power_path, delimiter="\t")

# number of n's is the number of rows
n_ns = power.shape[0]

ns_per_group = power[:, 0]
power_per_ns = power[:, 1]





import numpy as np

import veusz.embed

power_path = "prog_data_vis_power_sim_data.tsv"

power = np.loadtxt(power_path, delimiter="\t")

# number of n's is the number of rows
n_ns = power.shape[0]

ns_per_group = power[:, 0]
power_per_ns = power[:, 1]

embed = veusz.embed.Embedded("veusz")

page = embed.Root.Add("page")
page.width.val = "8.4cm"
page.height.val = "8cm"

graph = page.Add("graph", autoadd=False)

x_axis = graph.Add("axis")
y_axis = graph.Add("axis")


# do the typical manipulations to the axis apperances
graph.Border.hide.val = True

typeface = "Arial"

for curr_axis in [x_axis, y_axis]:

    curr_axis.Label.font.val = typeface
    curr_axis.TickLabels.font.val = typeface

    curr_axis.autoMirror.val = False
    curr_axis.outerticks.val = True

embed.WaitForClose()




import numpy as np

import veusz.embed

power_path = "prog_data_vis_power_sim_data.tsv"

power = np.loadtxt(power_path, delimiter="\t")

# number of n's is the number of rows
n_ns = power.shape[0]

ns_per_group = power[:, 0]
power_per_ns = power[:, 1]

embed = veusz.embed.Embedded("veusz")

page = embed.Root.Add("page")
page.width.val = "8.4cm"
page.height.val = "8cm"

graph = page.Add("graph", autoadd=False)

x_axis = graph.Add("axis")
y_axis = graph.Add("axis")

# let veusz know about the data
embed.SetData("ns_per_group", ns_per_group)
embed.SetData("power_per_ns", power_per_ns)

xy = graph.Add("xy")

xy.xData.val = "ns_per_group"
xy.yData.val = "power_per_ns"

# set the x ticks to be at every 2nd location we sampled
x_axis.MajorTicks.manualTicks.val = ns_per_group[::2].tolist()
x_axis.MinorTicks.hide.val = True
x_axis.label.val = "Sample size per group"
x_axis.min.val = float(np.min(ns_per_group) - 5)
x_axis.max.val = float(np.max(ns_per_group) + 5)

# sensible to include the whole range here
y_axis.min.val = 0.0
y_axis.max.val = 1.0
y_axis.label.val = "Power (for d = 0.8)"

# do the typical manipulations to the axis apperances
graph.Border.hide.val = True

typeface = "Arial"

for curr_axis in [x_axis, y_axis]:

    curr_axis.Label.font.val = typeface
    curr_axis.TickLabels.font.val = typeface

    curr_axis.autoMirror.val = False
    curr_axis.outerticks.val = True

embed.WaitForClose()