#Author: Arpit Gupta (glex.qsd@gmail.com)

import os, sys
import itertools
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
from matplotlib.mlab import PCA


asInterface={}
aux_asInterface={}
aux_name={}
#ixps=['jinx','kixp']
ixps=['jinx']
tm={}
log_name='log_rib.20130301.0000.txt'
asPair={}
uniqueAS={}

iclass={}

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


"""
def trafficMatrix():
    print "enter function"
    for ixp in ixps:
        fname='ribs/'+ixp+'/'+log_name
        bgpdump = open(fname,'r')
        lines = bgpdump.readlines()
        for line, next_line in pairwise(lines):
        #for line in lines:
            if line.startswith('ASPATH: '):
                ases=line.split('ASPATH: ')[1].split('\n')[0].split(' ')
                if len(ases)<=1:
                    #print "insufficient info for determining peering"
                    continue
                if (ases[0],ases[1]) not in asPair:
                    asPair[(ases[0],ases[1])]=1
                    if (ixp,ases[1]) in asInterface:
                        #print "the two ASes might peer at IXP itself. Need to confirm that"
                        #print line
                        #print next_line
                        if (ixp,ases[0]) in tm:
                            tm[(ixp,ases[0])].append(ases[1])
                        else:
                            tm[(ixp,ases[0])]=[ases[1]]


                        if next_line.startswith('NEXT_HOP: '):
                            nexthop=next_line.split('NEXT_HOP: ')[1].split('\n')[0]
                            print "nexthop:"+nexthop
                            if nexthop == asInterface[ixp,ases[1]]:
                                print "peering at IXP confirmed"
                                if ases[0] in tm:
                                    tm[ases[0]].append(ases[1])
                                else:
                                    tm[ases[0]]=[ases[1]]
                            else:
                                print "Not able to judge peering at IXP for: "
                                print line
                                print next_line
                        else:
                            print "next_hop not after aspath..."


                else:
                    asPair[(ases[0],ases[1])]+=1

"""


def trafficMatrix_aggr(aux_asInterface):
    print "Creating Peering Matrix from bgpdump"
    for ixp in ixps:
        fname='ribs/'+ixp+'/'+log_name
        bgpdump = open(fname,'r')
        lines = bgpdump.readlines()
        for line, next_line in pairwise(lines):
        #for line in lines:
            if line.startswith('ASPATH: '):
                ases=line.split('ASPATH: ')[1].split('\n')[0].split(' ')
                if len(ases)<=1:
                    #print "insufficient info for determining peering"
                    continue
                ases[1]=int(ases[1])
                ases[0]=int(ases[0])
                for j in [0]:
                    if ases[j] not in uniqueAS[ixp]:
                        uniqueAS[ixp].append(ases[j])
                        iclass[(ixp,ases[j])]='bgpdump'

                if (ases[0],ases[1]) not in asPair:
                    asPair[(ases[0],ases[1])]=1

                    if (ixp,ases[1]) in asInterface or (ixp,ases[1]) in aux_asInterface:
                        if ases[1] not in uniqueAS[ixp]:
                            uniqueAS[ixp].append(ases[1])
                            iclass[(ixp,ases[1])]='bgpdump'
                        if (ixp,ases[0]) in tm:
                            tm[(ixp,ases[0])].append(ases[1])
                        else:
                            tm[(ixp,ases[0])]=[ases[1]]

                else:
                    asPair[(ases[0],ases[1])]+=1

def print_pm(aux_name):
    for ixp in ixps:
        ofile = open('pm_'+ixp+'.txt','w+')
        ofile.write(' : ')
        for k in range(0,len(uniqueAS[ixp])):
            ofile.write('AS'+str(uniqueAS[ixp][k])+' ')
        ofile.write('\n')
        for i in range(0,len(uniqueAS[ixp])):
            as1=uniqueAS[ixp][i]
            if (ixp,as1) in aux_name:
                ofile.write('AS'+str(as1)+' '+aux_name[(ixp,as1)]+': ')
            else:
                ofile.write('AS'+str(as1)+' .. : ')

            for j in range(0,len(uniqueAS[ixp])):

                if (ixp,as1) in tm:
                    #ofile.write(str(as1)+': ')
                    #as1=uniqueAS[ixp][i]
                    as2=uniqueAS[ixp][j]
                    if as2 in tm[(ixp,as1)]:
                        ofile.write("Yes ")
                    else:
                        ofile.write("No ")
                else:
                    if iclass[(ixp,as2)]!=iclass[(ixp,as1)]:
                        ofile.write("NA* ")
                    else:
                        ofile.write("N/A ")
            ofile.write("\n")

        ofile.write("\n")

def process_traceroutePeering():
    pfile = open('ixp_peeringInfo.txt','r')
    flag=0
    for line in pfile.readlines():
        if line.startswith('IXP: ') and flag==0:
            ixp=line.split('\n')[0].split('IXP: ')[1].lower()
            if ixp in ixps:
                print ixp
                flag=1
        elif flag==1:
            if line.startswith('\n'):
                flag=0
            if line.startswith('AS'):
                as1=int(line.split('AS')[1].split(' ')[0])
                as2=int(line.split('AS')[2].split(' ' )[0])
                print as1
                print as2
                if as1 not in uniqueAS[ixp]:
                    uniqueAS[ixp].append(as1)
                    iclass[(ixp,as1)]='tracert'
                if (as1,as2) not in asPair:
                    asPair[(as1,as2)]=1
                    if as2 not in uniqueAS[ixp]:
                        uniqueAS[ixp].append(as2)
                        iclass[(ixp,as2)]='tracert'
                    if (ixp,as1) in tm:
                        tm[(ixp,as1)].append(as2)
                    else:
                        tm[(ixp,as1)]=[as2]


                else:
                    asPair[(as1,as2)]+=1

def peeringMatrices(tm):
    # define a peering matrix
    pm={}
    for ixp in ixps:
        pm[ixp]=[]
        i=0
        for as1 in uniqueAS[ixp]:
            pm[ixp].append([])
            j=0
            for as2 in uniqueAS[ixp]:
                if as1==as2:
                    pm[ixp][i].append(0)
                elif (ixp,as1) in tm:
                    if as2 in tm[(ixp,as1)]:
                        pm[ixp][i].append(1)
                    else:
                        pm[ixp][i].append(-1)

                else:
                    pm[ixp][i].append(0)
                j+=1
            i+=1
    return pm


def main():
    print "parse the file to map the Interfaces for each AS"
    for ixp in ixps:
        uniqueAS[ixp]=[]
        fname='ribs/'+ixp+'/'+log_name
        bgpdump = open(fname,'r')
        for line in bgpdump.readlines():
            if line.startswith('FROM:'):
                info=line.split('\n')[0].split(' ')
                ip = info[1]
                asn=int(info[2].split('AS')[1])
                if (ixp,asn) not in asInterface:
                    asInterface[ixp,asn]=ip
    (aux_asInterface,aux_name) = auxinfo.main()
    #print asInterface
    #print aux_asInterface
    #print ('kixp',25568) in aux_asInterface
    print aux_name
    print "Create the traffic matrix"
    trafficMatrix_aggr(aux_asInterface)
    #print asPair
    #process_traceroutePeering()
    print tm
    pMatrices=peeringMatrices(tm)
    myPCA=PCA(np.array(pMatrices['jinx']))
    print myPCA.Y
    print myPCA.a
    print np.array(pMatrices['jinx'])
    print uniqueAS
    print "print the Traffic Matrix"
    print_pm(aux_name)

if __name__ == "__main__":
    main()
