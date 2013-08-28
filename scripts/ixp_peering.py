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
ixp_peering={}
for loc in locations:
    print "Processing location: "+loc
    print "processing the location: "+loc
    fname='../'+loc+'/preval_ixpinfo.txt'
    ifile=open(fname,'r')
    did=''
    direc=0
    asnlist={}
    for line in ifile.readlines():
        if line.startswith('Device'):
            did=line.split('\n')[0].split(' ')[1]
            if did not in devices:
                devices.append(did)
        elif line.startswith('direction'):
            for ind in asnlist:
                if asnlist[ind] in ixpinfo:
                    #print asn
                    if (ind-1 in asnlist and ind+1 in asnlist) and (asnlist[ind-1]!='' and asnlist[ind+1]!=''):
                        """if asnlist[ind-1]=='':
                            print 'empty asname'
                            print asnlist
                        """
                        if asnlist[ind] not in ixp_peering:
                            ixp_peering[asnlist[ind]]={}
                        if (asnlist[ind-1],asnlist[ind+1]) in ixp_peering[asnlist[ind]]:
                            ixp_peering[asnlist[ind]][(asnlist[ind-1],asnlist[ind+1])]+=1
                        else:
                            ixp_peering[asnlist[ind]][(asnlist[ind-1],asnlist[ind+1])]=1

            asnlist={}
        elif line.startswith('\n') is False:
            asn=line.split(', ')[4].split('\n')[0]
            ind=int(line.split(',')[0])
            asnlist[ind]=asn


print ixp_peering
# print in more presentable form:
ofile=open('ixp_peeringInfo.txt','w+')
ofile.write('## Peering information inferred from Bismark Tracroutes for various IXPs\n\n')
for ixp in ixpinfo:
    ofile.write('\nIXP: '+ixp+'\n')
    if ixp in ixp_peering:
        pinfo=ixp_peering[ixp]
        #ofile.write('\nIXP: '+ixp+'\n')
        for (p1,p2) in pinfo:
            if p1 != 'private' and p2 != 'private':
                if p1=='':
                    print 'null'
                ofile.write(''+p1+'-->'+p2+', '+str(pinfo[(p1,p2)]))
                ofile.write('\n')

            else:
                print pinfo[p1,p2]


