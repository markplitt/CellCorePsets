TITLE nap
: Na current for axon. No slow inact.
: M.Migliore Jul. 1997
: added sh to account for higher threshold M.Migliore, Apr.2002

NEURON {
	SUFFIX nap
	USEION na READ ena WRITE ina
	RANGE  gbar, tha, thi1, thi2, qa, qd, qg, a0m, a0h
	GLOBAL minf, hinf, mtau, htau,thinf, qinf
}

PARAMETER {
	sh   = 15	(mV)
	gbar = 0.010   	(mho/cm2)

	tha  =  -30	(mV)		: v 1/2 for act
	qa   = 7.2	(mV)		: act slope (4.5)
	Ra   = 0.4	(/ms)		: open (v)
	Rb   = 0.124 	(/ms)		: close (v)

	thi1  = -45	(mV)		: v 1/2 for inact
	thi2  = -45 	(mV)		: v 1/2 for inact
	qd   = 1.5	(mV)	        : inact tau slope
	qg   = 1.5      (mV)
	mmin=0.02
	hmin=0.5
	q10=2
	Rg   = 0.01 	(/ms)		: inact recov (v)
	Rd   = .03 	(/ms)		: inact (v)

	thinf  = -50 	(mV)		: inact inf slope
	qinf  = 4 	(mV)		: inact inf slope

	ena		(mV)            : must be explicitly def. in hoc
	celsius
	v 		(mV)
}


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(pS) = (picosiemens)
	(um) = (micron)
}

ASSIGNED {
	ina 		(mA/cm2)
	thegna		(mho/cm2)
	minf 		hinf
	mtau (ms)	htau (ms)
}


STATE { m h}

BREAKPOINT {
        SOLVE states METHOD cnexp
        thegna = gbar*m*m*m
	ina = thegna * (v - ena)
}

INITIAL {
	trates(v)
	m=minf
	h=hinf
}

DERIVATIVE states {
        trates(v)
        m' = (minf-m)/mtau

}

PROCEDURE trates(vm) {
        LOCAL  a, b, qt
        qt=q10^((celsius-24)/10)
	a = trap0(vm,tha+sh,Ra,qa)
	b = trap0(-vm,-tha-sh,Rb,qa)
	mtau = 1/(a+b)/qt
        if (mtau<mmin) {mtau=mmin}
	minf = a/(a+b)

}

FUNCTION trap0(v,th,a,q) {
	if (fabs(v-th) > 1e-6) {
	        trap0 = a * (v - th) / (1 - exp(-(v - th)/q))
	} else {
	        trap0 = a * q
 	}
}
