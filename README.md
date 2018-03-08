# CellCorePsets
Interactive NEURON simulations for Stanford Cellular Neurophysiology Core Course


## Install Instructions

I recommend installing Ananconda if you have not already done so. 

In addition, install NEURON (https://www.neuron.yale.edu/neuron/download)

NEURON will try not to see your Anaconda installation if your system has another python available, so we will have to edit some paths.

If you are on a mac or linux system, check your bash_profile and check to make sure you have the following lines

export PATH="/anaconda3/bin:$PATH"

export PATH="/Applications/NEURON-7.5/nrn/x86_64/bin:/anaconda3/bin:$PATH"

export PYTHONPATH="${PYTHONPATH}:/Applications/NEURON-7.5/nrn/lib/python/"



Lastly, install Bokeh (some dope plotting tools) using conda:

conda install Bokeh



You may also need to install ipywidgets 

