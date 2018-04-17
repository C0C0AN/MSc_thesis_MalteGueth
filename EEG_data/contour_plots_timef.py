"""
Created on Sun Apr 15 08:44:43 2018

@author: maltegueth
"""

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

os.chdir('/Volumes/INTENSO/DPX_EEG_fMRI/EEG/time_frequency/txt/')
os.chdir('/Users/maltegueth/Downloads/')

dataA = 'Allsub_average_timef_A.txt'
dataB = 'Allsub_average_timef_B.txt'
times = 'eegtimes_average.txt'
timefA = pd.read_csv(dataA, sep=None, header=None)
timefB = pd.read_csv(dataB, sep=None, header=None)
points = pd.read_csv(times, sep=None, header=None)

induced_power1b_pz = pd.read_csv('Allsub_induced_power_B_5.txt', sep=None, header=None)
induced_power2b_pz = pd.read_csv('Allsub_induced_power_B_10.txt', sep=None, header=None)

induced_power1b_pz = ip1.iloc[:,719:759]
induced_power1b_pz = ip2.iloc[:,719:759]

X, Y = np.meshgrid(points.iloc[:,450:1100], range(1,31))

contours_ip_b_pz = plt.contourf(X, Y, ip2.iloc[:,450:1100], 80, cmap='RdBu_r')
#plt.clim(-5,25)
plt.gca()
plt.colorbar(shrink=0.8, extend='both');
plt.plot([0, 0], [1, 30], '--k')

plt.contour(X, Y, timefA.iloc[:,450:1100], 40, cmap='RdGy');

contours_ep_b_pz = plt.contourf(X, Y, timefB.iloc[:,450:1100], 20, cmap='RdBu')
plt.clim(-2,2)
plt.gca()
plt.colorbar(shrink=0.8, extend='both');
plt.plot([0, 0], [1, 30], '--k')
plt.title('event-related spectral perturbation (cue B) with colorbar')

contours_ep_a_pz = plt.contourf(X, Y, (timefA.iloc[:,450:1100] -0.25), 20, cmap='RdBu')
plt.clim(-2,2)
plt.gca()
plt.colorbar(contours_ep_b_pz, shrink=0.8, extend='both');
plt.plot([0, 0], [1, 30], '--k')
plt.title('event-related spectral perturbation (cue A) with colorbar')


contours = plt.contour(X, Y, timefA.iloc[:,450:1100], 3, colors='black')
plt.clabel(contours, inline=True, fontsize=8)

plt.imshow(timefB.iloc[:,450:1100], extent=None, origin='lower',
           cmap='RdGy')
plt.colorbar()
plt.axis(aspect='image');
