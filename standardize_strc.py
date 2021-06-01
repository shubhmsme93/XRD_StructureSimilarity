
import spglib
from pylada.crystal import read, write
from glob import iglob
from vladan.format_spglib import *
import os
import sys
from multiprocessing import Pool
from pylada.vasp import Extract
#from mpi4py import MPI
#######################
'''
# Initial calls
comm = MPI.COMM_WORLD
master = 0
n_proc = comm.Get_size()
rank = comm.Get_rank()

##
def load_balance(n_tasks):
# Defines the interval each cores needs to compute
    
    n_jobs = n_tasks//n_proc
    balance = n_tasks%n_proc

    if (rank < balance): 
        i_init = rank*(n_jobs+1)+1
        i_fin = (rank+1)*(n_jobs+1)
    else:
        i_init = balance*(n_jobs+1) + (rank-balance)*(n_jobs)+1
        i_fin = balance*(n_jobs+1) + (rank-balance+1)*(n_jobs)

    return range(i_init-1, i_fin)
'''

########## A function that standardizes structures
def stdz_strc(name):

    if os.path.exists(name+'POSCAR_st'):
        print (name,": Already DONE")

    elif not os.path.exists(name+'CONTCAR'):
        print (name,": No CONTCAR in")

    else:
        try:
            s = read.poscar(name+'CONTCAR')
            news = from_spglib( spglib.standardize_cell( to_spglib(s) , to_primitive=True))
            write.poscar(news,name+'POSCAR_st',vasp5=True)
            print (name,": OK")
        except:
            print (name,": Error in the CONTCAR ")
            pass
    return
#######################################

'''
names=list(iglob('POSCAR_24_atoms_24_*/'))

n_tasks=len(names)
local_tasks=load_balance(n_tasks)

for ii in local_tasks: #Parallelized loop
    stdz_strc(names[ii])


if (rank == master):
    print ("DONE !!!")
'''

# Selecting only those folders with successful VASP
names=[name for name in iglob('POSCAR_24_atoms_24_*/') if Extract(name).success]

#####################################
# Simple parallel execution with python.mulpiprocessing.Pool

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
    pool.map(stdz_strc, names)

# finalizing things
finally:
    n_cores = int(os.environ.get('SLURM_NTASKS'))
    pool = Pool(n_cores)
    pool.close()
    pool.join()
    print("DONE !!!")
    sys.stdout.flush()

