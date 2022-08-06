import pyalps
import matplotlib.pyplot as plt
import pyalps.plot
import numpy as np
import os
import glob


#function to delete old parm files (start with given string)
def delete_old(file_name):
    for d in glob.glob(file_name + ".task*.*"):
        os.remove(d)
    for d in glob.glob(file_name + ".in.*"):
        os.remove(d)
    for d in glob.glob(file_name + ".out.*"):
        os.remove(d)


#if statement to simplyfy the simulation (TRUE/FALSE)
if False:
    LATTICE = "my_chain"
    PREFIX = "Chain_spinmc_lattice"
else:
    LATTICE = "my_ladder"
    PREFIX = "Ladder_spinmc_lattice"


#prepare the input parameters with different incrementation (0.5 and 2)
temp_list = list(np.arange(2,10,0.5)) + list(np.arange(10,25,2))

parms = []
for t in temp_list:
    parms.append(
        {
            'LATTICE'        : LATTICE, 
            'LATTICE_LIBRARY': "my_ladder_lattice.xml", 
            'MODEL'          : "Ising", 
            'MODEL_LIBRARY'  : "my_ladder_model.xml", 
            'T'              : t, 
            'J'              : 1 ,
            'THERMALIZATION' : 1000,
            'SWEEPS'         : 50000,
            'UPDATE'         : "cluster",
            'L'              : 30
        }
    )


#run delete old simulation files function before new simulation
delete_old('parm')


#write the input file and run the simulation
input_file = pyalps.writeInputFiles(PREFIX, parms)
results = pyalps.runApplication('spinmc', input_file, Tmin = 5)

assert results[0] == 0, "There is an ERROR in runApplication!"

#evaluate tool results of the spinmc application (+evaluated results are written back intothe files)
pyalps.evaluateSpinMC(pyalps.getResultFiles(prefix = PREFIX))


