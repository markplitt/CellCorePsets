from neuron import h
import numpy as np

# define branched cable class
class branched_cable(object):
    def __init__(self,):
        '''initialize dictionaries for storing information about cell'''
        self.segments = {}
        self.stims = {}
        self.record_vecs = {}

    def make_cable(self,L,diam,segname='cable',cm = 1, Ra = 150,Rm = 2800, Vrest = -65.,nseg=None):
        '''make a cable with specified distributed properties (approximate a sphere by setting diam=L= x)'''
        cable = h.Section(name=segname,cell=self)
        cable.L = L #micro-m
        cable.diam = diam # micro-m
        cable.cm = cm  # picofarads/cm^2
        cable.Ra = Ra # megaOhms/cm^2

        if nseg is None: # use d_lambda rule to get good guess of best number of segments
            cable.nseg = int(L) #50*(int((L/(0.1*h.lambda_f(100))+.999)/2.)*2 + 1)
        else:
            cable.nseg = nseg

        cable.insert('pas')
        cable.g_pas = 1/Rm # picoSiemens/cm^2
        cable.e_pas = Vrest # milliVolts
        self.segments[segname] = cable



    def add_branch(self,seg,pos,L,diam,segname='branch',cm = 1, Ra = 150,Rm = 2800, Vrest = -65.):
        '''add a branch to seg at pos with specified distributed properites'''
        self.make_cable(L,diam,segname=segname,cm = cm, Ra = Ra,Rm = Rm, Vrest = Vrest)
        self.segments[segname].connect(self.segments[seg](pos))
        #self.segments[segname]

    def add_IClamp(self,seg,pos,amp,dur,delay = 50,stimname = 'iclamp'):
        '''insert current clamp on cell compartment seg at position pos (0 to 1: percent down the process)
        amp: amplitude (milliamps)
        dur: duration (milliseconds)
        delay: delay before stimulus (milliseconds)'''
        iclamp = h.IClamp(self.segments[seg](pos))
        iclamp.amp = amp
        iclamp.dur= dur
        iclamp.delay = delay
        self.stims[stimname]=iclamp

    def add_stim(self,seg,pos):
        '''add a synapse on cell compartment seg at position pos (0 to 1: percent down the process)

        Not fully functional yet'''
        stim = h.NetStim() # Make a new stimulator

        # Attach it to a synapse in the middle of the dendrite
        # of the first cell in the network. (Named 'syn_' to avoid
        # being overwritten with the 'syn' var assigned later.)
        syn_ = h.ExpSyn(self.segments[seg](pos), name='syn_')

        stim.number = 1
        stim.start = 9
        ncstim = h.NetCon(stim, syn_)
        ncstim.delay = 1
        ncstim.weight[0] = 0.04 # NetCon weight is a vector.

    def recording_vecs(self,locations):
        ''' add NEURON vectors to record desired parameters specified by list of lists locations

        each entry in locations is a list with 3 entries: segment name, location on segment (0-1), and the variable
        name you wish to record (e.g. v for membrane potential)'''
        # locations is list of lists with segname, location, variable
        currKeys = self.record_vecs.keys()
        if 'time' not in currKeys:
            t_vec = h.Vector()
            t_vec.record(h._ref_t)
            self.record_vecs['time']= t_vec

        for v in locations:
            try:
                keyname = "%s:%.2f:%s" % (v[0],v[1],v[2])
            except:
                raise("invalid specification of recording locations")


            if keyname in currKeys:
                print(keyname+"is a already a recording vec")

            else:
                self.record_vecs[keyname] = h.Vector()
                eval("self.record_vecs[keyname].record(self.segments[v[0]](v[1])._ref_" + v[2]+")")


def run_current_clamp(cell,stimname,stimVals,tstop = 130):

    results = {}
    for i, amp in enumerate(stimVals):
        cell.stims[stimname].amp = amp
        h.tstop=tstop
        h.run()

        if i == 0:
            t = cell.record_vecs['time'].as_numpy()
            for key in cell.record_vecs.keys():
                results[key] = np.zeros([t.shape[0],len(stimVals)])

        for key in cell.record_vecs.keys():
            results[key][:,i] = cell.record_vecs[key].as_numpy()

    return t, results
