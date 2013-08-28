import os, sys
import symmetry_analysis
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netaddr import *
from scipy.stats import cumfreq
#import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import statsmodels.api as sm

locations=['tunisia', 'jburg','nairobi']

ixpinfo={'DE-CIX': '80.81.199.0/24', 'LINX': '195.66.224.0/19', 'AS1200 Amsterdam Internet Exchange B.V.': '195.69.144.0/22', 'KIXP': '196.223.21.32/27', 'CINX': '196.223.22.0/24', 'JINX': '196.223.14.0/24'}
devices=[]

ixp_preval={}


for loc in locations:
    print "processing the location: "+loc
    fname='../'+loc+'/preval_ixpinfo.txt'
    ifile=open(fname,'r')
    did=''
    prevl=0.0
    direc=0
    for line in ifile.readlines():
        if line.startswith('Device'):
            did=line.split('\n')[0].split(' ')[1]
            if did not in devices:
                devices.append(did)
            #print did
        elif line.startswith('direction'):
            prevl=line.split(':')[4].split(' ')[1]
            direc=line.split('direction: ')[1].split('nhop')[0]
            print direc
            #print prevl
        elif line.startswith('\n') is False:
            asn=line.split(', ')[4].split('\n')[0]
            if asn in ixpinfo:
                #print asn
                if (loc,asn,did) in ixp_preval:
                    ixp_preval[(loc,asn,did)]+=float(prevl)/2

                else:
                    ixp_preval[(loc,asn,did)]=float(prevl)/2
    print ixp_preval

    print "plot for location: "+loc
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    i=0
    p1=[]
    select_ixp=[]
    for ixp in ixpinfo:
        a=[]
        print ixp
        for did in devices:
            if (loc,ixp,did) in ixp_preval:
                a.append(ixp_preval[(loc,ixp,did)])
            else:
                a.append(0.0)
        print a

        if sum(a) != 0.0:
            num_bins=10000
            counts, bin_edges = np.histogram(a,bins=num_bins,normed=True)
            cdf=np.cumsum(counts)
            scale = 1.0/cdf[-1]
            cdf=cdf*scale
            p1.append([])
            p1[i]=pl.plot(bin_edges[1:],cdf,label=loc,color=color_n[i], linewidth=5.0)
            if ixp =='AS1200 Amsterdam Internet Exchange B.V.':
                select_ixp.append('AMS-IX')
            else:
                select_ixp.append(ixp)
            i+=1
    p=[]
    i=0
    for ixp in select_ixp:
        p.append(p1[i][0])
        i+=1
    pl.ylim(0.00,1.00)
    pl.xlim(-1,100)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    pl.legend((p),select_ixp,'lower right',prop={'size':32})
    pl.xlabel('IXP Prevalence (%)',fontsize=32)
    pl.ylabel('# Paths ',fontsize=32)
    ax.grid(True)
    plot_name='ixp_preval_'+loc+'.eps'
    plot_name_png='ixp_preval_'+loc+'.png'
    pl.savefig(plot_name)
    pl.savefig(plot_name_png)

os.system('scp *.eps *png arpit@newton.noise.gatech.edu:~/Bismark_bgp/Traceroutes/prevalence/results/')



