import raw_xrd_equal as xrd
import pandas as pd
import os
import sys
import time
from multiprocessing import Pool


#read in the dataframe with list of all relaxed structure IDs
#and create an empty dataframe to save the results
df1 = pd.read_csv('../data_relaxed.csv')
df2 = pd.DataFrame()


#initialize empty lists to save structure IDs, scaling factors, and minimized CRD differences
str_i = []
str_j = []
scales = []
diffs = []


#initialize indices of structure pairs
inputs = [[i,j] for i in range(len(df1)-1) for j in range(i+1, len(df1))]


#initialize a function to apply 'minimize_xrd_diff' function over all structure pairs
def xrd_scale(x):
   scale, diff = xrd.minimize_xrd_diff(df1.str_id[x[0]], df1.str_id[x[1]])
   print (df1.str_id[x[0]], df1.str_id[x[1]], ": Finished")
   return df1.str_id[x[0]], df1.str_id[x[1]], scale[0], diff
   

#####################################
# Simple parallel execution with python.mulpiprocessing.Pool

start = time.time()

# try might not be needed, just in case
try:

    # getting the number of cores
    # this is a more autmated way that gets the number of cores from the system
    n_cores = int(os.environ.get('SLURM_NTASKS'))
    print("Running on ", n_cores," cores")
    sys.stdout.flush()

    # creating the Pool object
    pool = Pool(n_cores)

    # running the job in parallel
    out = pool.map(xrd_scale, inputs)

# finalizing things
finally:
    #n_cores = int(os.environ.get('SLURM_NTASKS'))
    #pool = Pool(n_cores)             
    pool.close()
    pool.join()
    print("DONE !!!")
    sys.stdout.flush()

for i in out:
    str_i.append(i[0])
    str_j.append(i[1])
    scales.append(i[2])
    diffs.append(i[3])

end = time.time()

df2['str_fixed'] = str_i
df2['str_scaled'] = str_j
df2['scaling_factor'] = scales
df2['minimized_diff'] = diffs

df2.to_csv('xrd_scaled.csv', index=False)


##TIME##
f_time = open('time_scale.txt', 'w')
print("elaspsed_time:", end-start, file=f_time)
f_time.close()
