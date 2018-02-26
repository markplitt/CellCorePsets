vm = linspace(-120,40);
celsius = 27;

sh   = 15	;
gbar = 0.010   	;	

tha  =  -30		;%	: v 1/2 for act	
qa   = 7.2		;%	: act slope (4.5)		
Ra   = 0.4	; %		: open (v)		
Rb   = 0.124 ; %		: close (v)		

thi1  = -45	;%(mV)		: v 1/2 for inact 	
thi2  = -45 ;%	(mV)		: v 1/2 for inact 	
qd   = 1.5	;%(mV)	        : inact tau slope
qg   = 1.5   ;%   (mV)
mmin=0.02	;
hmin=0.5	;		
q10=2;
Rg   = 0.01 ;%	(/ms)		: inact recov (v) 	
Rd   = .03 ;%	(/ms)		: inact (v)	

thinf  = -50 ;%	(mV)		: inact inf slope	
qinf  = 4 	;%(mV)		: inact inf slope 



    

trap0 = @(v,th,a,q) a * (v - th) ./ (1 - exp(-(v - th)/q));


qt=q10^((celsius-24)/10);
a = trap0(vm,tha+sh,Ra,qa);
b = trap0(-vm,-tha-sh,Rb,qa);
mtau = 1./(a+b)/qt;  
minf = a./(a+b);

a = trap0(vm,thi1+sh,Rd,qd);
b = trap0(-vm,-thi2-sh,Rg,qg);
htau =  1./(a+b)/qt;
hinf = 1./(1+exp((vm-thinf-sh)/qinf));

subplots(121);
plot(vm,minf); hold on; plot(vm,mtau);

subplots(122);
plot(vm,hinf); hold on; plot(vm,htau);
