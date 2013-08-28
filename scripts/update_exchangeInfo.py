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
#locations=['nairobi']
results={}
ixpinfo={}
private_blocks=['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16']

def is_private(i):
    ip = IPAddress(i)
    for block in private_blocks:
        if ip in IPNetwork(block):
            return True
    return False

def find_exchange(i):
    ip=IPAddress(i)
    if is_private(i) is True:
        return 'private'
    else:
        for ixp in ixpinfo:
            prefix=ixpinfo[ixp]
            network=IPNetwork(prefix)
            if ip in network:
                #print "Match for "+ixp+" found"
                return ixp
    if ip in IPNetwork('196.6.121.0/24') is False:
        print "## Weired: No match found for ip: "+i
    return ''

def main():
    print "read the exchange info"
    ixpfile=open('exchange_prefixes.txt','r')
    for line in ixpfile.readlines():
        #print line
        prefix=line.split(':')[0]
        ixp=line.split(':')[1].split('\n')[0]
        ixpinfo[ixp]=prefix

    print ixpinfo
    # Now use this info to see through the preval_result files
    for loc in locations:
        print "Processing "+loc+" data"
        fname='../'+loc+'/preval_results.txt'
        pfile=open(fname,'r')
        ofname='../'+loc+'/preval_ixpinfo.txt'
        ofile=open(ofname,'w+')
        for line in pfile.readlines():
            if line.startswith('Device') or line.startswith('direction') or line.startswith('\n'):
                ofile.write(line)
            else:
                #print line
                asn=line.split(',')[4]
                if asn.startswith(' AS') is False:
                    #print 'asn:'+asn
                    ip=line.split(', ')[1]
                    ixp=find_exchange(ip)
                    newline=line.split('\n')[0]+''+ixp+'\n'
                    ofile.write(newline)
                else:
                    ofile.write(line)



if __name__=="__main__":
    main()
