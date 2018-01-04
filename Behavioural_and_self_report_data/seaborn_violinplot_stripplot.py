"""
Created on Fri Sep 29 13:44:55 2017

@author: Malte
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Descriptive plots in seaborn package to portray sample characteristics, such as personality or cognitive scores
# Data has to be imported in the wide form with each scale represented in a column and each subject in a single row
# Below is an example with psychopathy scores from my bachelor thesis

dataIN = np.array([39, 39, 29, 37, 28, 30, 42, 34, 37, 31, 29,
                    65, 54, 66, 80, 52, 80, 69, 66, 65, 62, 78])
dataBE = np.array([40, 41, 46, 42, 38, 64, 47, 37, 42, 37, 41,
                      60, 54, 57, 61, 37, 48, 51, 49, 65, 66, 58])
dataME = np.array([46, 48, 29, 38, 38, 62, 34, 41, 43, 44, 33,
                     53, 48, 59, 42, 47, 54, 55, 50, 66, 50, 52])
dataCN = np.array([42, 44, 61, 55, 42, 35, 36, 48, 68, 51, 38, 37,
                   34, 57, 66, 34, 27, 49, 49, 55, 71, 61])
dataSI = np.array([30, 58, 39, 47, 51, 31, 47, 41, 39, 42, 48,
                        42, 72, 40, 45, 63, 72, 64, 69, 56, 46, 47])
dataSP = np.array([22, 33, 22, 25, 34, 24, 40, 20, 44, 21, 27, 26,
                   68, 55, 55, 76, 70, 68, 61, 51, 41, 62])
dataF = np.array([56, 30, 38, 68, 55, 33, 57, 48, 65, 57, 44, 32,
                  59, 56, 59, 67, 69, 63, 67, 47, 52, 53])
dataC = np.array([48, 46, 28, 45, 41, 28, 46, 39, 27, 33, 28,
                  48, 66, 72, 50, 69, 62, 53, 50, 60, 53, 32])
dataTotal = np.array([26, 33, 20, 36, 27, 24, 36, 21, 20, 27, 22,
                      62, 65, 67, 70, 61, 76, 72, 67, 69, 62, 66])

Group2 = ['High Psychopathy']*11
Group1 = ['Low Psychopathy']*11
Group = Group1 + Group2

df1 = pd.DataFrame({'Impulsive-Nonconformity': dataIN,
                   'Blame Externalization': dataBE,
                   'Machiavellian Egocentricity': dataME,
                   'Carefree Nonplanfulness': dataCN,
                   'Stress Immunity': dataSI,
                   'Social Potency': dataSP,
                   'Fearlessness': dataF,
                   'Coldheartedness': dataC,
                   'Total': dataTotal,
                   'Psychopathy': Group})

df2 = pd.melt(df1, "Psychopathy", var_name="Scales", value_name="T-Value")

sns.set(style="white")

f, ax = plt.subplots()
sns.despine(bottom=True, left=True)

sns.stripplot(x="T-Value", y="Scales", hue="Psychopathy",
              data=df2, jitter=True,
              alpha=.25, zorder=1)

sns.pointplot(x="T-Value", y="Scales", hue="Psychopathy",
              data=df2, join=False, palette="dark",
              markers="d", scale=1, ci=None)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[2:], labels[2:], title="Psychopathy Group",
          handletextpad=0, columnspacing=2,
          loc="best", ncol=1, frameon=True)


f, ax = plt.subplots()
sns.set(font_scale = 1.5)

sns.violinplot(x="Scales", y="T-Value", hue="Psychopathy", 
               saturation=0.7, data=df2, split=True,
               inner="quart", palette={"High Psychopathy": "b", "Low Psychopathy": "c"}, bbox_inches="tight")
sns.despine(left=True)
plt.xticks(rotation=70)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[2:], labels[2:], title=None,
          handletextpad=0, columnspacing=2,
          loc="best", ncol=1, frameon=True)
