import pyalps
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pyalps.plot
import numpy as np


#list connected to calculation file with outputs
PREFIX_LIST = ['spinmc_chain_high_density']
pre_list = []
for p in PREFIX_LIST:
    pre_list = pre_list + pyalps.getResultFiles(prefix = p)


#parameter variable what to draw on the plot
load_argument = 'Susceptibility', '|Magnetization|', 'Specific Heat', 'Energy'


#load selected measurements
data = pyalps.loadMeasurements(pre_list, [load_argument]) 


#parameter variable what to draw plots
S = 'Susceptibility'
M = '|Magnetization|'
SH = 'Specific Heat'
E = 'Energy'



#ChiT
obschoose = lambda d, o: np.array(d)[np.nonzero([xx.props['observable'] == o for xx in d])]

chit =[]
for dd in data:
    susc = obschoose(dd, S)[0]

    res = pyalps.DataSet() #ChiT
    res.props = pyalps.dict_intersect([d.props for d in dd])
    res.x = np.array([susc.props['T']])
    res.y = np.array(susc.y[0] * res.x)
    res.props['observable'] = 'ChiT'
    chit.append(res)



divide = ['MODEL', 'LATTICE', 'J1']

# collect plotdata as a function of temperature T
plotdata = pyalps.collectXY(data, x = 'T', y = 'ChiT', foreach = divide) 

#flatten hierarchical structure
plotdata = pyalps.flatten(plotdata)
data = pyalps.flatten(data)

#collect physical properies data as a function of temperature - into different data sets depending on the value of the LATTICE and MODEL parameters
Sus = pyalps.collectXY(data, x = 'T', y = S, foreach = divide) 
Mag = pyalps.collectXY(data, x = 'T', y = M, foreach = divide) 
SpeH = pyalps.collectXY(data, x = 'T', y = SH, foreach = divide) 
Ene= pyalps.collectXY(data, x = 'T', y = E, foreach = divide) 



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


