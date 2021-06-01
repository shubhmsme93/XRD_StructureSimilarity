import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from collections import OrderedDict


##gaussian function: x = list of discretized max(E-Emin) of the group, x0 = E-Emin of a structure, sigma = FWHM (3 or 4 * least count of x
def gauss(x,x0,sigma):
     return np.exp(-np.power(x-x0,2)/(2*np.power(sigma,2)))/(sigma*np.sqrt(2*np.pi))


df = pd.read_parquet('groups.parquet')
df = df.sort_values('max_parent_sg').reset_index(drop=True)

df['X'] = ''
df['gaussians'] = ''

nrg = pd.read_csv('data_relaxed.csv')
x = np.linspace(-0.05,2*nrg['E-Emin'].max()+0.05,20000)

##calculate gaussian for each structure in each group and sum them up
for i in range(len(df)):
     y = np.zeros(len(x))
     for j in df.E_Emin_fu[i]:
         y += gauss(x,j,200*(x[1]-x[0]))
     df['X'].values[i] = x
     df['gaussians'].values[i] = y


# plot all gaussians
# load colors
colors = np.load('colors.npy')

for i in range(len(df)):
     plt.plot(df.X[i],df.gaussians[i],color=colors[df.max_parent_sg[i]],lw=0.1)
     plt.fill_between(df.X[i],df.gaussians[i],color=colors[df.max_parent_sg[i]],alpha=0.9,label='s.g. #'+str(df.max_parent_sg[i]))


# show unique labels in the legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(),framealpha=1, frameon=True)
plt.xlabel(r'E-$\rmE_{GS}$ (eV/f.u.)', fontsize=16)
plt.ylabel("Space group resolved TDOS (arb. units)", fontsize=16)



