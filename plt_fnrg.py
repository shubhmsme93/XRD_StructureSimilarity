import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict


## calculate partial partition functions for each group ##

df = pd.read_parquet('groups.parquet')
df = df.sort_values('max_parent_sg').reset_index(drop=True)

df['temp'] = ''
df['Pk'] = ''
df['free_nrg'] = ''

temp = np.arange(50,2100,150)
kb = 8.617333262145 * 1e-05

# loop over all groups to calculate ensemble probabilities

for i in range(len(df)):
     P = []
     for t in temp:
         pk = 0
         for j in range(len(df.groups[i])):
             pk += np.exp(-(df.E_Emin_fu[i][j])/(kb*t))
         P.append(pk)
     df['Pk'].values[i] = P
     df['temp'].values[i] = temp


# loop over all groups to calculate free energies

for i in range(len(df)):
     F = []
     for j in range(len(df.Pk[i])):
         F.append(-kb*df.temp[i][j]*np.log(df.Pk[i][j]))
     df['free_nrg'].values[i] = F


## plot free energies ##

# load colors
colors = np.load('colors.npy')

plt.figure(figsize=(5,5))

for i in range(len(df)):
      plt.plot(df.temp[i],df.free_nrg[i],color=colors[df.max_parent_sg[i]], label=str(df.max_parent_sg[i]))


# show unique labels in the legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))


plt.ylabel('Configurational free energy (eV/f.u.)', fontsize=16)
plt.xlabel('Temperature (K)', fontsize=16)
plt.xticks(np.arange(0, 2500, step=500),fontsize=13)
plt.yticks(np.arange(-1, 2, step=0.5),fontsize=13)
plt.xlim(-1,2050)
plt.title(r'Ta$\rmC_{0.916}N_{0.084}$',fontsize=16)
plt.tight_layout()



