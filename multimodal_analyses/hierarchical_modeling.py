"""
Created on Sun Nov 19 16:35:26 2017

@author: Malte
"""

# Notes on a hierachical regression model (see http://twiecki.github.io/blog/2014/03/17/bayesian-glms-3/)
# for prediction of behavioral, cognitive and self-report data

import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm 
import pandas as pd

data = pd.read_csv('all_data.csv')

with pm.Model() as hierarchical_model:

    mu_a = pm.Normal('mu_alpha', mu=0., sd=1)
    sigma_a = pm.HalfCauchy('sigma_alpha', beta=1)
    mu_b = pm.Normal('mu_beta', mu=0., sd=1)
    sigma_b = pm.HalfCauchy('sigma_beta', beta=1)
    
    # Intercept for each modality with parameterised EEG predictor, distributed around group mean mu_a
    a = pm.Normal('alpha', mu=mu_a, sd=sigma_a, shape=len(data.eeg.unique()))
    # Intercept for each modality with parameterised MRI predictor, distributed around group mean mu_a
    b = pm.Normal('beta', mu=mu_b, sd=sigma_b, shape=len(data.mri.unique()))
    
    # Model error
    eps = pm.HalfCauchy('eps', beta=1)
    
    # Expected value from EEG and MRI predictor
    rt_est = a[eeg_idx] + b[mri_idx]
    
    # Data likelihood
    y_like = pm.Normal('y_like', mu=rt_est, sd=eps, observed=data.rt)
    
with hierarchical_model:
    hierarchical_trace = pm.sample(njobs=4)
