"""
Created on Sun Jan 08 09:27:51 2018

@author: Malte R. Gueth
"""

# Read in data and get some basic descriptive and inferential statistics using pandas data frame, statsmodels,
# seaborn and scipy statistics

import pandas
data = pd.read_csv('/Volumes/INTENSO/DPX_EEG_fMRI/Behavioral_Data/self_report_data.csv', 
                   sep=';', na_values="none")

# Basic descriptives and t-test

data['age'].mean()
data['age'].std()
data[data['gender'] == 'female']['age'].mean()
data[data['gender'] == 'female']['digit_symbol_coding'].mean()
data[data['gender'] == 'male']['digit_symbol_coding'].mean()

groupby_gender = data.groupby('gender')
for gender, value in groupby_gender['digit_symbol_coding']:
    print((gender, value.mean()))

from pandas import plotting
plotting.scatter_matrix(data[['age', 'digit_symbol_coding', 'grade']])   

data = data.replace('male', 2)
data = data.replace('female', 1)

from scipy import stats
female_perf = data[data['gender'] == 'female']['task_performance']
male_perf = data[data['gender'] == 'male']['task_performance']
stats.ttest_ind(female_perf, male_perf)

# Regressional analyses and seaborn plots for self-report data

x = data['gender']
y = data['task_performance']
dataRegression = pandas.DataFrame({'x': x, 'y': y})

from statsmodels.formula.api import ols
model = ols("y ~ x", data).fit()

print(model.summary()) 

# Plot regressional scatter plots using seaborn

import seaborn
seaborn.pairplot(data, vars=['gender', 'grade', 'digit_symbol_coding', 
                             'task_performance', 'alertness'],kind='reg') 

# Calculate ANOVA, effect sizes and create table

import statsmodels.api as sm
from statsmodels.formula.api import ols
 
model = ols('grade ~ digit_symbol_coding',
                data=data).fit()
                
table = sm.stats.anova_lm(model, typ=2)
print table

esq = table['sum_sq'][0]/(table['sum_sq'][0]+table['sum_sq'][1])
print esq
