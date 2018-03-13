"""
Created on Mon Jan 22 16:06:13 2018

@author: Malte R. Gueth
"""

# Read in reaction times and reaction types by block, trial and trialtype ('rawdata.txt')
# Get some basic descriptive and inferential statistics using pandas data frame, statsmodels,
# seaborn and scipy statistics

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Create pandas dataframe with column names

columns = ['Block1', 'block', 'Trial1', 'trial', 'Type', 'trialtype', 
           'cuetype', 'mask', 'RZ', 'rt', 'Rtype', 'reactiontype']
data = pd.DataFrame(columns=columns)

# Start subject loop with rawdata files and append all files in the dataframe

for x in range(1, 14):
    path = '/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/rawdata/%drawdata.txt' % (x)
    f = pd.read_csv(path, sep=',', names=columns)
    data = data.append(f, ignore_index=True)

# Rearrange and tidy up the dataframe
   
ID = (['1']*208 + ['2']*208 + ['3']*208 + ['4']*208 + ['5']*208 + ['6']*208 + ['7']*208
      + ['8']*208 + ['9']*208 + ['10']*208 + ['11']*208 + ['12']*208 + ['13']*208)
rt_data = data[['block', 'trial', 'trialtype', 'rt', 'reactiontype']]
rt_data['ID'] = ID
cols = rt_data.columns.tolist()
cols = cols[-1:] + cols[:-1]
rt_data = rt_data[cols]
rt_data['rt'] = pd.to_numeric(rt_data['rt'])

# For later calculation of error rates, get some descriptive data on valid and invalid responses
# Then, filter the dataframe with all RT data for invalid, too quick or too slow respones

descriptives_reaction = rt_data['rt'].groupby([rt_data['block'], 
                                              rt_data['trialtype'], rt_data['reactiontype']]).describe()

rt_corrects = rt_data.loc[(rt_data['reactiontype'] == ' hit') & (rt_data['rt'] > 100)
                         & (rt_data['rt'] < 800)]

# Adjust the basic descriptive statistics given by describe with a new function

def get_stats(group):
    return {'min': group.min(), 'max': group.max(), 'count': group.count(),
            'mean': group.mean(), 'sd': group.std()}
stats = rt_corrects['rt'].groupby([rt_data['block'], rt_data['trialtype']]).apply(get_stats).unstack()

rt_corrects_means = rt_corrects[['block', 'trialtype', 'rt']]
rt_corrects_means = rt_corrects_means.groupby([rt_corrects_means['block'], 
                                               rt_corrects_means['trialtype']]).mean().add_prefix('mean_')

# Create some distributional other descriptive plots

sns.set(style="white")
sns.set_context("notebook")    

f, ax = plt.subplots()
  
sns.boxplot(x="block", y="rt", hue='trialtype', data=rt_corrects, palette="PRGn")
sns.despine(offset=10, trim=True)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[4:], labels[4:], title=None,
          handletextpad=0, columnspacing=2,
          loc="best", ncol=1, frameon=True)

# First, let's look at all RT disregarding trialtypes and blocks to get an overview of the distribution
# by creating a 2x2 figures showing four panels with kernel and histogram estimates

sns.set(palette="muted", color_codes=True)

f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
sns.despine(left=True)

sns.distplot(rt_corrects['rt'], kde=False, color="b", ax=axes[0, 0])

sns.distplot(rt_corrects['rt'], hist=False, rug=True, color="r", ax=axes[0, 1])

sns.distplot(rt_corrects['rt'], hist=False, color="g", kde_kws={"shade": True}, ax=axes[1, 0])

sns.distplot(rt_corrects['rt'], color="m", ax=axes[1, 1])

plt.setp(axes, yticks=[])
plt.tight_layout()

# Now, have a look at the distirbutions grouped by trialtype

f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
sns.despine(left=True)

ax = rt_corrects.loc[(rt_corrects['trialtype'] == 1)]
sns.distplot(ax['rt'], color="b", ax=axes[0, 0])

bx = rt_corrects.loc[(rt_corrects['trialtype'] == 2)]
sns.distplot(bx['rt'], color="r", ax=axes[0, 1])

ay = rt_corrects.loc[(rt_corrects['trialtype'] == 3)]
sns.distplot(ay['rt'], color="g", ax=axes[1, 0])

by = rt_corrects.loc[(rt_corrects['trialtype'] == 4)]
sns.distplot(by['rt'], color="m", ax=axes[1, 1])

plt.setp(axes, yticks=[])
plt.tight_layout()

# Or...

f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
sns.despine(left=True)

sns.distplot(ax['rt'], hist=False, rug=True, color="b", ax=axes[0, 0])

sns.distplot(bx['rt'], hist=False, rug=True, color="r", ax=axes[0, 1])

sns.distplot(ay['rt'], hist=False, rug=True, color="g", ax=axes[1, 0])

sns.distplot(by['rt'], hist=False, rug=True, color="m", ax=axes[1, 1])

plt.setp(axes, yticks=[])
plt.tight_layout()

# Test a basic multiple regression model and ANOVA 
# to check that the different trialtypes have a significant effect

model = ols('rt ~ trialtype + block', rt_corrects).fit()
print(model.summary())
                
table = sm.stats.anova_lm(model, typ=3)
print table
