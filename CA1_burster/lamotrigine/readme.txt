NEURON mod files from the paper:
N. Poolos, M. Migliore, and D. Johnston
Pharmacological upregulation of h-channels selectively reduces
the excitability of pyramidal neuron dendrites
Nature Neuroscience 5, 767-774 (2002).

The paper shows that the anticonvulsant drug lamotrigine
shifts the I-h activation curve, and results in reduction of EPSPs summation
on distal dendrites while minimally influencing summation of proximal ones.
Rather than reproduce the main modeling figure of the paper (Fig.6)
with rather long simulations, the main effect is demonstrated here
with simpler and shorter simulations, where a single synapse
is randomly (poisson) activated at an average frequency of 20Hz.
With the lamotrigine.hoc file two simulations can be run:
- distal, where the synapse is at 200um from soma
- proximal, where the synapse is close to the soma.
In each case two traces will be superimposed, corresponding to
simulations with or without a +10mV shift  
in the Ih activation curve, modeling lamotrigine application.

Under unix systems:
to compile the mod files use the command 
nrnivmodl 
and run the simulation hoc file with the command 
nrngui lamotrigine.hoc

Under Windows systems:
to compile the mod files use the "mknrndll" command.
A double click on the simulation file
lamotrigine.hoc 
will open the simulation window.

Questions on how to use this model
should be directed to michele.migliore@pa.ibf.cnr.it

Bugs and fixes:
03 July 2003  -  M. Migliore
A bug in the vhalfl variable declaration in h.mod
required a change of ghd in lamotrigine.hoc (from 0.0003 to 0.0006) 
to obtain the same results. 

