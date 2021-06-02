
import spglib
from pylada.crystal import read, write
from glob import iglob
from xrd_calculator.format_spglib import *
import os
import sys
from multiprocessing import Pool
from pylada.vasp import Extract
#from mpi4py import MPI
#######################

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

