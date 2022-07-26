from sys import prefix
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
if True:
    LATTICE = "my_chain"
    PREFIX = "Chain_spinmc_lattice"
else:
    LATTICE = "my_ladder"
    PREFIX = "Ladder_spinmc_lattice"


#prepare the input parameters
temp_list = list(np.arange(0.1,2.5,0.1))+list(np.arange(2.5,10.5,0.2))

parms = []
for t in temp_list:
    parms.append(
        {
            'LATTICE'        : LATTICE, 
            'LATTICE_LIBRARY': "my_chain_lattice.xml", 
            'MODEL'          : "Ising", 
            'MODEL_LIBRARY'  : "my_chain_model.xml", 
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
results = pyalps.runApplication('spinmc',input_file, writexml = True)
assert results[0]==0, "There is an ERROR in runApplication!"

pyalps.evaluateSpinMC(pyalps.getResultFiles(prefix = PREFIX))


#parameter variable what to draw on the plot
argument = 'Susceptibility'


#get the list of result files 
result_files = pyalps.getResultFiles(prefix = 'parm')
print ("Loading results from the files: ", result_files)


#print the observables stored in those files 
print ("The files contain the folowing measurements: "),
print (pyalps.loadObservableList(result_files))


#load selected measurements
data = pyalps.loadMeasurements(result_files, [argument]) 


# collect plotdata as a function of temperature T
plotdata = pyalps.collectXY(data, x = 'T', y = argument', foreach = ['MODEL', 'LATTICE']) 


#function to make plot with multiple variables (susceptibility, magnetization and specific heat)
def sim_plot(plotdata):
    N = len(plotdata[0].y)
    new_argument_x = np.zeros(N)
    new_argument_y = np.zeros(N)
    new_variance = np.zeros(N)
    for k in range(N):
        new_argument_x[k] = plotdata[0].x[k]
        new_argument_y[k] = plotdata[0].y[k].mean
        new_variance[k] = plotdata[0].y[k].variance
    chi_t = new_argument_x * new_argument_y
    chi_t_variance = new_variance * new_argument_x
    return new_argument_x, new_argument_y, new_variance, chi_t, chi_t_variance

plt.errorbar(new_argument_x, new_argument_y, new_variance, chi_t, chi_t_variance, label='Ising')
plt.legend()
plt.title(PREFIX)
plt.show()



#convert simulated data into txt format 
print ("Results in txt format are saved: ")
f  = open ('chain_lattice.txt', 'w')
f.write(pyalps.plot.ConvertToText(plotdata))
f.colse()


