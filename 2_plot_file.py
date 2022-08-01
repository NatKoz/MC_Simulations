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

#scale_data = 'J'
scale_data = 'exp' #stands for experimental data


#parameter variable what to draw on the plot
load_argument = 'Susceptibility', '|Magnetization|', 'Specific Heat', 'Energy'


#load selected measurements
data = pyalps.loadMeasurements(pre_list, [load_argument]) 


#parameter variable what to draw plots
S = 'Susceptibility'
M = '|Magnetization|'
SH = 'Specific Heat'
E = 'Energy'


#enter experimental data from external file
def enter_data(file_name):
    all_exp_data = np.loadtxt(file_name, delimiter = '\t', dtype = str) #.transpose()
    all_exp_data = np.delete(all_exp_data, [0,1,2], axis = 0)
    return np.char.replace(all_exp_data, ',', '.').astype(float64)


#enter experimental txt file
exp_chain_chit = enter_data('exp_chit_chain_h1000.txt')
exp_chain_s = enter_data('exp_sus_chain_h1000.txt')
exp_chain_m = enter_data('exp_m_chain-1_8K-2.txt')
exp_chain_sh = enter_data('exp_sh_chain.txt')

"""#ChiT
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
    """



divide = ['MODEL', 'LATTICE', 'J1']

# collect plotdata as a function of temperature T


#flatten hierarchical structure
plotdata = pyalps.flatten(plotdata)
data = pyalps.flatten(data)


#constant physical quantities
sus_const = (0.375 * 0.5 * (8**2)/4)
m_const = 8/2
sh_const = 8.314


#collect physical properies data as a function of temperature - into different data sets depending on the value of the LATTICE and MODEL parameters
Sus = pyalps.collectXY(data, x = 'T', y = S, foreach = divide) 
for su in Sus:
    if su.props["LATTICE"] == 'my_chain':
        su.y = su.y / 2
    if scale_data == 'J':
        su.x = su.x / su.props['J']
        su.props['xlabel'] = 'T/J'
        su.props['ylabel'] = '$\chi$'
    elif scale_data == 'exp':
        su.y = su.y * sus_const / 3
        su.props['xlabel'] = 'T (K)'
        su.props['ylabel'] = '$\chi_{avg}$ (cm$^3$/mol)'
    elif scale_data = 'none':
        su.props['xlabel'] = 'T'
        su.props['ylabel'] = '$\chi$'



Chi_T = pyalps.collectXY(data, x = 'T', y = S, foreach = divide)
for ch in Chi_T:
    ch.y = ch.y * ch.x
    ch.props['ylabel'] = '$\chi T$'
    if ch.props["LATTICE"] == 'my_chain':
        ch.y = ch.y / 2
    if scale_data == 'J':
        ch.x = ch.x / ch.props['J']
        ch.props['xlabel'] = 'T/J'
        ch.props['ylabel'] = '$\chi T$'
    elif scale_data == 'exp':
        ch.y = ch.y * sus_const / 3
        ch.props['xlabel'] = 'T (K)'
        ch.props['ylabel'] = '$\chi_{avg} T$ (cm$^3$K/mol)'
    elif scale_data = 'none':
        ch.props['xlabel'] = 'T'
        ch.props['ylabel'] = '$\chi T$'



log_Chi_T = pyalps.collectXY(data, x = 'T', y = S, foreach = divide) 
Mag = pyalps.collectXY(data, x = 'T', y = M, foreach = divide) 

Spe_H = pyalps.collectXY(data, x = 'T', y = SH, foreach = divide) 
for sh in Spe_H:
    sh.y = sh.y / sh.x
    if sh.props["LATTICE"] == 'my_chain':
        sh.y = sh.y / 2
    if scale_data == 'J':
        sh.x = sh.x / sh.props['J']
        sh.y = sh.y * sh.props['J']
        sh.props['xlabel'] = 'T/J'
        sh.props['ylabel'] = 'CJ/T'
    elif scale_data == 'exp':
        sh.y = sh.y * sh_const
        sh.props['xlabel'] = 'T (K)'
        sh.props['ylabel'] = 'C/T (J/molK$^2$)'
    elif scale_data = 'none':
        sh.props['xlabel'] = 'T'
        sh.props['ylabel'] = 'C/T'




"""""
#function to rescaling lattice real-valued data
def normalized(sims):
    for sim in sims:
        if sim.props["LATTICE"] == 'my_chain':
            for osy in sim.y:
                osy = osy/2

normalized(Chi_T)
normalized(Sus)
normalized(Mag)
normalized(Spe_H)
normalized(Ene)
"""




#plots for collected physical properies data 
plt.figure()

plt.sobplot(221)
pyalps.plot.plot(Chi_T)
plt.xlabel('Temperature $T$')
plt.ylabel('$\chi$T')

plt.sobplot(222)
pyalps.plot.plot(Sus)
plt.xlabel('Temperature $T$')
plt.ylabel('Susceptibility $\chi J$')
plt.ylim(0,1)

fontP = FontProperties()
fontP.set_size('smaller')
plt.legend(loc = 'upper right', bbox_to_anchor = (1,1), prop = fontP)


plt.sobplot(223)
pyalps.plot.plot(Spe_H)
plt.xlabel('Temperature $T$')
plt.ylabel('Specific Heat $c_v$')

plt.sobplot(224)
pyalps.plot.plot(Mag)
plt.xlabel('Temperature $T$')
plt.ylabel('Magnetization $m$')


plt.show()




