---
## Monte Carlo Simulations
___

Goal of the project is to compare experimental and simulated data results of molecular magnetic complex. The numerical Monte Carlo simulation method is used with the ALPS package. The simulation algorithm was defined by the exchange interactions between atoms and the Ising model of the nearest neighbors (NN) in the respective lattices of one-dimensional chain and two-dimensional ladder, based on temperature-dependant variational approach. 

The motivation to undertake this issue is the study of the magnetization properties, specific heat and magnetic susceptibility for the first spin ladder Co(NCS)2 and the next one from the group of low-temperature magnetics.

You will like this project!

---
###  💻 Technologies
___

* Python libraries: NumPy, Matplotlib 
* ALPS libraries: PyAlps (eg. HDF5), XML, API

---
### 🎬 Launch
___

Monte Carlo simulations are performed with the 'time dependence' of a model in a stochastic manner. It depends on a sequence of random numbers which are generated during the simulation. The simulation will not give identical results due to different sequence of random numbers.  The part of the 'art' of simulation is the appropriate choice of a suitable model. 

#### The ALPS Project 

The ALPS project stands for Algorithms and Libraries for Physics Simulations. It is an open source data formats, libraries and simulation codes for quantum lattice models and can be downloaded codes from website  http://alps.comp-phys.org . Simulation codes of quantum lattice models are possible due to individual codes, model-specific implementations and growing complexity of methods. ALPS is considered to have community codes, simplified code development with generic implementations. Common file formats are possible to be considered, eg. XML for input and output what gives portability and self-explanatory options.

Simulations with ALPS package are possible due to system structure. There are three variables which are inputs for the system: lattice library, model library and parameters library. The system setup make it possible to use Monte Carlo method to finally obtain results.


