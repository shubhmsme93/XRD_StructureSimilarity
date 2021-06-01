from pylada.crystal import read
from glob import iglob
from xrd_calculator.xrdcalculator import XRDCalculator
import os
import sys
from multiprocessing import Pool
import pickle
from pylada.vasp import Extract
#################################

############# INPUTS ############

# Selecting only those folders with successful VASP
names=[name for name in iglob('POSCAR_24_atoms_24_*/') if Extract(name).success]


############# Function writing raw XRD
def write_raw_xrd(name):

    if os.path.exists(name+"/raw_xrd.p"):
        print(name, ": Already DONE")

    else:
    ###### XRD ######

        strc=Extract(name).structure

        xrd=XRDCalculator(wavelength="CuKa", symprec=0, debye_waller_factors=None)
        xrd_data=xrd.get_xrd_data(strc,two_theta_range=(0, 180))
    
        # writting the xrd
        pickle.dump(xrd_data,open(name+'/raw_xrd.p','wb'))
        ##
        print (name, ": Finished")
    return
#######################
                           

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
    pool.map(write_raw_xrd, names)

# finalizing things 
finally:
    n_cores = int(os.environ.get('SLURM_NTASKS'))
    pool = Pool(n_cores)
    pool.close()
    pool.join()
    print("DONE !!!")
    sys.stdout.flush()
