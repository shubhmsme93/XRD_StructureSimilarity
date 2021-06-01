from pylada.crystal import read
from glob import iglob
from xrd_calculator.xrdcalculator import XRDCalculator
from xrd_calculator.rdf import g_r
from multiprocessing import Pool
import sys
import os


############# Function writing RDF and XRD
def write_xrd_rdf(name):

    strc=read.poscar(name+'POSCAR_st')

    if os.path.exists(name+"/xrd.dat"):
        print(name, ": Already DONE")

    else:
    ###### RDF ######

        rdf=g_r(strc)
        
        #writting the rdf
        for key in rdf.keys():
            rdf_file = open(name+'/rdf_%s.dat' %(key),'w')
    
            for x in rdf[key]:
                rdf_file.write(' % 4.8f    % 4.8f\n' %(x[0],x[1]))
                
            rdf_file.close()


    ###### XRD ######

        xrd=XRDCalculator(wavelength="CuKa", symprec=0, debye_waller_factors=None)
        xrd_data=xrd.broadened(strc,sigma=0.3)
    
        # writting the xrd
        xrd_file = open(name+'/xrd.dat','w')
    
        for x in xrd_data:
            xrd_file.write(' % 4.8f    % 4.8f\n' %(x[0],x[1]))

        xrd_file.close()
        ##
    
        print (name, ": Finished")
    return
#######################

                           
names=[x for x in iglob('POSCAR_24_atoms_24_*/')]
names=[name for name in names if os.path.exists(name+'POSCAR_st')]


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
    pool.map(write_xrd_rdf, names)

# finalizing things
finally:
    n_cores = int(os.environ.get('SLURM_NTASKS'))
    pool = Pool(n_cores)
    pool.close()
    pool.join()
    print("DONE !!!")
    sys.stdout.flush()

