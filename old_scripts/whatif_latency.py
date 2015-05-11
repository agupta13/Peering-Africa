# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,sys
import IXP_auxInfo as auxinfo
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netaddr import *
from scipy.stats import cumfreq
#import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import statsmodels.api as sm

# attempt to improve your figures
from matplotlib.ticker import MaxNLocator
my_locator = MaxNLocator(6)

from matplotlib import rc
rc('/data/arpit/matplotlib_config.rc')


asInterface={}
asName={}

rtt_simul=[]
rtt_orig=[]

africa=['Kenya','South Africa']
newworld={}
kenet={36914,'Kenya Education Network'}
kasn=36914
new_rtt=10.0

def plot_cdf(r1,r2):
    print "Plot the original and simulated RTT"
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    rtts=[r1,r2]
    rlabel=['Existing','Better Peering']
    p1=[]
    i=0
    for r in rtts:
        a=r
        num_bins=1000
        counts, bin_edges = np.histogram(a,bins=num_bins,normed=True)
        cdf=np.cumsum(counts)
        scale = 1.0/cdf[-1]
        cdf=cdf*scale
        p1.append([])
        p1[i]=pl.plot(bin_edges[1:],cdf*100,label=rlabel[i],color=color_n[i], linewidth=5.0)
        i+=1
    p=[]
    i=0
    for r in rtts:
        p.append(p1[i][0])
        i+=1
    pl.ylim(0.01,100)
    #pl.xlim(0,550)
    """
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    """
    pl.legend((p),rlabel,'lower right')
    pl.xlabel('RTT (ms)')
    pl.ylabel('% Routes ')
    ax.grid(True)
    plot_name='latency_simul.eps'
    plot_name_png='latency_simul.png'
    pl.savefig(plot_name)
    pl.savefig(plot_name_png)
    os.system('scp *.eps *png arpit@newton.noise.gatech.edu:~/Writings/glex/PAM14/results/')


def main():
    print "Start the what if analysis"
    asInterface,asName=auxinfo.main()
    jinx_asn=[]
    for key in asName.keys():
        ixp,asn=key
        jinx_asn.append(asn)
    #print jinx_asn
    newworld[kasn]=jinx_asn
    for asn in jinx_asn:
        newworld[asn]=kasn
    print len(newworld.keys())
    fopen=open('nairobi_traceroute_processed.txt','r')
    flag=0
    rtt=0.0
    stop=0.0
    start=0.0
    diff=0.0
    flag1=0
    rtt_prev=0.0
    line_prev=''
    rtt_prev2=0.0
    line_prev2=''
    hop=0
    mhop=0
    line_start=''
    line_stop=''
    for line in fopen.readlines():

        if line.startswith('hops'):
            mhop=int(line.split('\n')[0].split(': ')[1])
            #print mhop
            flag=1
            flag1=0
            line_prev=''
            line_prev2=''
            line_start=''
            line_stop=''
            diff=0.0
            rtt_prev=0.0
            rtt_prev2=0.0

        elif line.startswith('\n') and flag==1:
            flag=0
            #
            if hop==mhop:
                rtt_adj=rtt-diff+new_rtt
                #if diff<=new_rtt or rtt<=diff or rtt>500:

                if rtt<600 and start<=50 and rtt>rtt_adj and rtt>diff:
                    print "rtt: "+str(rtt)+" adj: "+str(rtt_adj)+", diff: "+str(diff)
                    #print "rtt: "+str(rtt)+" adj: "+str(rtt_adj)+", diff: "+str(diff)
                    rtt_simul.append(rtt_adj)
                    rtt_orig.append(rtt)

                """
                if diff<100 or start>50:
                    print line_prev
                    print line_prev2
                    print "start/stop"
                    print line_start
                    print line_stop
                """

            else:
                a=1
                #print "hop: "+str(hop)+' mhop: '+str(mhop)
                #print "hop mismatch"
        elif flag==1:
            temp=line.split('AS')
            #print "flag==1"
            #print newworld.keys()
            if len(temp) >=2:
                asn=int(temp[1].split(' ')[0])
                rtt=float(temp[0].split(',')[2])
                cntry=temp[0].split(',')[3]
                hop=int(temp[0].split(',')[0])
                #print hop
                #print asn
                if asn not in newworld.keys() and flag1==0:
                    flag1=1
                    start=rtt_prev2
                    line_start=line_prev2
                    #print 'start: '+str(start)
                elif flag1==1 and asn in newworld.keys():
                    stop=rtt
                    diff=float(stop)-float(start)
                    #print 'diff: '+str(diff)
                    flag1=2
                    line_stop=line
                rtt_prev2=rtt_prev
                line_prev2=line_prev
                rtt_prev=rtt
                line_prev=line
    rtt_orig.sort()
    rtt_simul.sort()
    print rtt_orig
    print rtt_simul
    plot_cdf(rtt_orig,rtt_simul)


if __name__=="__main__":
    main()
