import pyalps
import matplotlib.pyplot as plt
import pyalps.plot


#prepare the input parameters
parms = []
for t in [0., 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]:
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


#load the susceptibility and collect it as a function of temperature T
data = pyalps.loadMeasurements(pyalps.getResultFiles(prefix='parm'), 'Susceptibility') 
susceptibility = pyalps.collectXY(data,x='T',y='Susceptibility') 


#make plot
plt.figure()
pyalps.plot.plot(susceptibility)
plt.xlabel('Temperature $T/J$')
plt.ylabel('Susceptibility $\chi J$')
plt.ylim(0,0.22) 
plt.title('Classical Heisenberg chain')
plt.show()
