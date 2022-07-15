import pyalps
import matplotlib.pyplot as plt
import pyalps.plot
import numpy as np


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


#write the input file and run the simulation
input_file = pyalps.writeInputFiles('parm',parms)
pyalps.runApplication('spinmc',input_file,Tmin=5)


#load the susceptibility
data = pyalps.loadMeasurements(pyalps.getResultFiles(prefix='parm'), 'Susceptibility') 

#flatten the hierarchical structure
data = pyalps.flatten(data)

# collect susceptibility as a function of temperature T
susceptibility = pyalps.collectXY(data,x='T',y='Susceptibility') 

#asign labels to the data depending on the properties
for s in susceptibility:
    if s.props['LATTICE'] == 'chain lattice':
        s.props['label'] == "chain"
    elif s.props['LATTICE'] == 'ladder':
        s.props['label'] == "ladder"
    if s.props['MODEL'] == 'spin':
        s.props['label'] == "quantum" + s.props['label']
    elif s.props['LATTICE'] == 'Ising':
        s.props['label'] == "classical" + s.props['label']

#make plot
plt.figure()
pyalps.plot.plot(susceptibility)
plt.xlabel('Temperature $T/J$')
plt.ylabel('Susceptibility $\chi J$')
plt.ylim(0,0.22) 
plt.title('Classical Heisenberg chain')
plt.show()
