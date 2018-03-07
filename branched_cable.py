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
        elif nseg is "d_lambda":
            cable.nseg=int((L/(0.1*h.lambda_f(100))+.999)/2.)*2 + 1
        else:
            cable.nseg = nseg

        cable.insert('pas')
        cable.g_pas = 1/Rm # picoSiemens/cm^2
        cable.e_pas = Vrest # milliVolts
        self.segments[segname] = cable



    def add_branch(self,seg,pos,L,diam,segname='branch',cm = 1, Ra = 150,Rm = 2800,
        Vrest = -65.,nseg=None):
        '''add a branch to seg at pos with specified distributed properites'''
        self.make_cable(L,diam,segname=segname,cm = cm, Ra = Ra,Rm = Rm, Vrest = Vrest,
            nseg=nseg)
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

    def add_stim(self,seg,pos,weight=1,tau = .1,delay=80,stimname='alpha_syn'):
        '''add a synapse on cell compartment seg at position pos (0 to 1: percent down the process)

        Not fully functional yet'''
        stim = h.NetStim() # Make a new stimulator
        syn_ = h.ExpSyn(self.segments[seg](pos))
        syn_.e = 0
        syn_.tau = 1
        stim.number = 10
        stim.interval=.1
        stim.start = 80
        ncstim = h.NetCon(stim, syn_)
        ncstim.delay = 1
        ncstim.weight[0] = .04 # NetCon weight is a vector.
        #cell.stims['expsyn']=ncstimn weight is a vector.
        self.stims[stimname]=ncstim

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



    def channel_control(self,secname, # default values taken from CA1 simulation
        kdr = False, gkdrbar=.003, vhalfn_kdr = 13, a0n_kdr=.02,zetan_kdr=-3,
        kin = False, gkinbar = .008, vhalfn_kin = 11, vhalfl_kin = -56,
        zetan_kin = -1.5, zetal_kin = 3, a0n_kin =.05,a0l_kin=.05,
        h = False, ghbar = .0001, vhalfl_h = -90, vhalft_h=-75, zetal_h = 4,
        zetat_h=2.2,a0t_h =.011,
        na = False, gnabar = .01,vhalfm_na = -30, vhalfh_na = -45, zetam_na = 7.2,
        zetah_na = 1.5, a0m_na=1,a0h_na=1,
        nap=False,gnapbar=.001):
        '''insert distributed channels and control conductances, voltage dependence,
        and dynamics'''



        # K delayed rectifier
        if kdr:
            self.segments[secname].insert('kdr')
            self.segments[secname].gkdrbar_kdr = gkdrbar #.003
            # voltage dependence
            self.segments[secname].vhalfn_kdr = vhalfn_kdr # half activation (Default 13)
            # kinetics
            self.segments[secname].a0n_kdr = a0n_kdr # gain on kinetics (default .02)
            self.segments[secname].zetan_kdr = zetan_kdr # slope of voltage dependence (default -3)


        # K inactivating
        #I don't have  a good mod file for this at the moment
        if kin:
            self.segments[secname].insert('kap')
            # conductance
            self.segments[secname].gkabar_kap = gkinbar
            # voltage depenedence

            # activation
            self.segments[secname].vhalfn_kap = vhalfn_kin # activation gate
            self.segments[secname].vhalfl_kap = vhalfl_kin # inactivation gate
            self.segments[secname].zetan_kap = zetan_kin # slope for activation gate
            self.segments[secname].zetal_kap = zetal_kin # slope for inactivation gate

            # kinetics
            self.segments[secname].a0n_kap = a0n_kin # tau activation gain
            self.segments[secname].a0l_kap = a0l_kin # tau inactivation gain



        # Ih
        if h:
            self.segments[secname].insert('hd')
            # conductance
            self.segments[secname].ghdbar_hd = ghbar
            # voltage dependence
            #
            self.segments[secname].vhalfl_hd = vhalfl_h # v-half activation gate
            self.segments[secname].vhalft_hd = vhalft_h # v-half kinetics
            self.segments[secname].a0t_hd = a0t_h # scale tau
            self.segments[secname].zetal_hd = zetal_h # slope of activation gate voltage dependence
            self.segments[secname].zetat_hd = zetat_h # slope of tau voltage dependence
            #kinetics

        # Na
        if na:
            self.segments[secname].insert('nax')

            self.segments[secname].gbar_nax = gnabar
            # voltage dependence
            self.segments[secname].tha_nax = vhalfm_na # activation gate voltage dependence
            self.segments[secname].thi1_nax = vhalfh_na # inactivation gate voltage dependence
            self.segments[secname].thi2_nax = vhalfh_na

            # slopes
            self.segments[secname].qa_nax = zetam_na # activation gate slopes
            self.segments[secname].qd_nax = zetah_na # inactivation slope
            self.segments[secname].qg_nax = zetah_na

            # gain on kinetics
            self.segments[secname].a0m_nax = a0m_na # global gain on activation kinetics
            self.segments[secname].a0h_nax = a0h_na # global gain on inactivation kinetics

        if nap: # persistant sodium
            self.segments[secname].insert('nap')
            self.segments[secname].gbar_nap = gnapbar
            # volatage dependence


    def noise_source(self,seg,pos, E_e=0, E_i=-75, g_e0=0.0121,
        g_i0=0.0573,std_e=0.0030, std_i=0.0066,
        tau_e=2.728,tau_i=10.49,stimname = 'noise'):


        syn_noise = h.Gfluct2(self.segments[seg](pos))
        syn_noise.E_e=E_e
        syn_noise.E_i =E_i
        syn_noise.g_e0 =g_e0
        syn_noise.g_i0 =g_i0
        syn_noise.std_e =std_e
        syn_noise.std_i =std_i
        syn_noise.tau_e =tau_e

        self.stims[stimname]=syn_noise
        # noise = h.IClampNoise(self.segments[seg](pos))
        # noise.f0=1
        # noise.std=1


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

def run_sim(cell,tstop=130):
    results = {}

    h.tstop=tstop
    h.run()


    t = cell.record_vecs['time'].as_numpy()
    for key in cell.record_vecs.keys():
        results[key] = np.zeros([t.shape[0],])

    for key in cell.record_vecs.keys():
        results[key][:] = cell.record_vecs[key].as_numpy()

    return t, results
