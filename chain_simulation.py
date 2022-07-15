import pyalps
import matplotlib.pyplot as plt
import pyalps.plot
import numpy as np
import os
import glob


#function to delete old parm files (start with given string)
def delete_old(file_name):
    for d in glob.glob(file_name + "*.*"):
        os.remove(d)



#prepare the input parameters
temp_list = list(np.arange(0.1,2.5,0.1))+list(np.arange(2.5,10.5,0.2))

parms = []
for t in temp_list:
    parms.append(
        {
            'LATTICE'        : "chain lattice", 
            'T'              : t, 
            'J'              : 1 ,
            'THERMALIZATION' : 1000,
            'SWEEPS'         : 50000,
            'UPDATE'         : "cluster",
            'MODEL'          : "Ising", 
            'L'              : 30
        }
    )


#run delete old simulation files function before new simulation
delete_old('parm')


#write the input file and run the simulation
input_file = pyalps.writeInputFiles('parm',parms)
pyalps.runApplication('spinmc',input_file, writexml = True)


#get the list of result files 
result_files = pyalps.getResultFiles(prefix = 'parm')
print ("Loading results from the files: ", result_files)


#print the observables stored in those files 
print ("The files contain the folowing measurements: "),
print (pyalps.loadObservableList(result_files))


#load selected measurements
data = pyalps.loadMeasurements(result_files, ['Susceptibility']) 


# collect plotdata as a function of temperature T
plotdata = pyalps.collectXY(data,x='T',y='Susceptibility', foreach=['MODEL', 'LATTICE']) 


#function to make plot with multiple variables (susceptibility, magnetization and specific heat)
def sim_plot(plotdata):
    N=len(plotdata[0].y)
    new_argument_x = np.zeros(N)
    new_argument_y = np.zeros(N)
    new_variance = np.zeros(N)
    for k in range(N):
        new_argument_x[k] = plotdata[0].x[k]
        new_argument_y[k] = plotdata[0].y[k].mean
        new_variance[k] = plotdata[0].y[k].variance
    return new_argument_x, new_argument_y, new_variance

plt.errorbar(new_argument_x, new_argument_y, new_variance, label='Ising')
plt.legend()
plt.show()