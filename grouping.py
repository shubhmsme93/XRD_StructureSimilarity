import pandas as pd
import numpy as np

### load dataframe 'xrd_scaled.py' ###
xrd = pd.read_csv('xrd_scaled.csv')

# user defined minimized xrd cutoff = x
xrd = xrd[xrd['minimized_diff'] <= 0.4]
xrd = xrd.reset_index(drop=True)

# exchange 'str_fixed' and 'str_scaled'
xrd_new = pd.DataFrame()
xrd_new['str_fixed'] = xrd['str_scaled']
xrd_new['str_scaled'] = xrd['str_fixed']
xrd_new['minimized_diff']  = xrd['minimized_diff']
del xrd['scaling_factor']

# append original xrd_scaled with new xrd_scaled
xrd = xrd.append(xrd_new).reset_index(drop=True)

### define a function taking two structures as arguments and returning 'True' if they satisfy xrd cutoff <= 0.4 ###
def xrd_group(key1,key2):
           df_key1 = xrd[xrd.str_fixed == key1]
           if key2 in df_key1.str_scaled.unique():
               return True


### load dataframe 'data_relaxed.csv' to make a list of all structure IDs ###
nrg = pd.read_csv('data_relaxed.csv')  
nrg = nrg.sort_values('energy').reset_index(drop=True)
nrg['E_Emin_fu'] = 2*nrg['E-Emin']

# make a list of 'structure IDs' from 'nrg'
ordered_en = nrg['str_id'].to_list()


############################ Grouping Step 1 ###############################################

### for loop to make groups based on xrd ###
equals = []

for name in ordered_en:

     print(name)

     if len(equals)==0:
         equals.append([name])

     else:
         is_in=False
         for ii in range(len(equals)):
             if xrd_group(name,equals[ii][0]):
                 equals[ii].append(name)
                 is_in=True
                 break

         if not is_in:
             equals.append([name])


# store groups (equals list) in a datframe
df = pd.DataFrame()
df['groups'] = equals


####################################### Grouping Step 2 #######################################

# for loops to re-group structures 
for ii in range(10):   # 10 is an arbitrary number, usually this wouldn't take more than 3 iterations

    index1 = []    #initialzie empty lists to store group numbers of the two groups to be checked for similarity
    index2 = []  

    for i in range(len(df)-1):    #loop over all groups in pairs to check for similar structures

         for j in range(len(df.groups[i])):
             xrd_key = xrd[xrd.str_fixed == df.groups[i][j]]
             for k in range(i+1,len(df)):
                 for kk in range(len(df.groups[k])):
                     if df.groups[k][kk] in xrd_key.str_scaled.unique():
                         print("similar groups found with indices {} and {}".format(i,j))
                         index1.append(i)
                         index2.append(k)

    if len(index1) == 0: 
        break

    #store indices in a dataframe
    df_index = pd.DataFrame()  
    df_index['indx1'] = index1
    df_index['indx2'] = index2

    # keep only unique 'indx1' and 'indx2' pairs
    df_index = df_index.drop_duplicates().reset_index(drop=True)
    df_index = df_index.sort_values('indx1',ascending=False).reset_index(drop=True)

    # merge groups of indices 'indx2' with groups of indices 'indx1' in 'df'
    # only keep unique structures after merging  
    for s in range(len(df_index)):
         df.groups[df_index.indx1[s]] = np.unique(np.append(df.groups[df_index.indx1[s]],df.groups[df_index.indx2[s]]))

    # drop groups in 'df' of indices 'indx2' using df_index
    df = df.drop(df.index[df_index['indx2'].unique().tolist()]).reset_index(drop=True)

print("Grouping complete")

# save df containing groups 
df.to_parquet('groups.parquet',index=False)
