# Author: Arpit Gupta

import os,sys
import pygeoip
#import statistics as stats
from statistics import *
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



gi4 = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIP.dat', pygeoip.MEMORY_CACHE)
giasn = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIPASNum.dat', pygeoip.MEMORY_CACHE)

gicity= pygeoip.GeoIP('/data/arpit/pygeoip/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)


kenya_servers={}
latency_matrix={}
devices=[]
new_rtt = 10.0
def getKenya():
    ifile=open('googleCache_processed.txt','r')
    for line in ifile.readlines():
        if len(line.split(','))==4:
            if line.split(',')[2]=='Kenya':
                kenya_servers[line.split(',')[0]]=int(line.split(',')[3].split('AS')[1].split(' ')[0])


def process_traceroute():
    for srv in kenya_servers.keys():
        fname='africa_traceroute_data/'+srv+'_traceroute_data.txt'
        foname ='africa_traceroute_data/'+srv+'_traceroute_processed.txt'
        ifile = open(fname,'r')
        ofile = open(foname,'w+')
        for line in ifile.readlines():
            if line.startswith('\n') or line.startswith('Device') or line.startswith('hops'):
                ofile.write(line)
            else:
                temp=line.split(',')
                if len(temp)==3 and temp[1]!='*':
                    ip = temp[1]
                    rtt=temp[2]
                    #print ip
                    c = gi4.country_name_by_addr(ip)
                    #print ip
                    if c==None:
                        c=''
                    asn = giasn.org_by_addr(ip)
                    if asn == None:
                        asn = ''
                    ofile.write(line.split('\n')[0]+','+c+','+asn+'\n')

def get_latencyMatrix():
    for srv in kenya_servers.keys():
        perDest={}
        fname = 'africa_traceroute_data/'+srv+'_traceroute_processed.txt'
        ofile=open(fname,'r')
        dev=''
        lat=0.0
        flag=0
        maxhop=0
        hop=0
        #devices=[]
        for line in ofile.readlines():
            if line.startswith('Device'):
                dev = line.split('\n')[0].split('id:')[1]
                perDest[dev]=[]
                flag=1
                if dev not in devices:
                    devices.append(dev)

            elif len(line.split(','))==5:
                lat=(line.split(',')[2])

                hop=int(line.split(',')[0])
            elif line.startswith('hops'):
                if flag==1:
                    flag=0
                    maxhop=int(line.split(':')[1].split('\n')[0])
                else:
                    if maxhop-hop<4:
                        #print line
                        #print lat
                        if lat!='':
                            perDest[dev].append(float(lat))
        perdev={}
        for dev in devices:
            total, average, median, standard_deviation, minimum, maximum, confidence = stats(perDest[dev])
            perdev[dev]=median
        latency_matrix[srv]=perdev

def getLatencyMetric(pair,lm):
    latm=0.0

    for dev in devices:
        #print dev
        latp=[]
        for srv in pair:
            latp.append(lm[srv][dev])
        latm+=min(latp)
    latm=latm/len(devices)
    #print latm
    return latm

def getSimulData(lm):
    #for srv in kenya_servers.keys():
    name = kenya_servers.keys()
    pairs={}
    ltm={}
    for height in range(1,len(kenya_servers.keys())+1):
        sets =  set(itertools.combinations(name,height))
        lath = []
        for pair in sets:
            #print pair
            latMetric = getLatencyMetric(pair,lm)
            lath.append(latMetric)
        ltm[height]=min(lath)
    print ltm
    return ltm

def coalsec(asName):
    nw = {}
    for key in asName.keys():
        ixp,asn=key
        nw[asn]=asName[ixp,asn]
    #print nw[36914]
    return nw

def get_SlatencyMatrix(nw):
    mlat={}
    for srv in kenya_servers.keys():
        mlat[srv]={}
        fname = 'africa_traceroute_data/'+srv+'_traceroute_processed.txt'
        ofile = open(fname,'r')
        flag=1
        dev=''
        latp={}
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

        for line in ofile.readlines():
            if line.startswith('Device'):
                dev = line.split('\n')[0].split('id:')[1]
                latp[dev]=[]
            elif line.startswith('hops'):
                mhop=int(line.split(':')[1].split('\n')[0])
                flag=1
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
                line_start=''
                line_stop=''


            elif line.startswith('\n') and flag==1:
                if mhop-hop<4:
                    if stop==0.0:
                        rtt_adj = start+new_rtt
                    else:
                        rtt_adj = rtt-diff +new_rtt
                    """
                    print "rtt: "+str(rtt)+" adj: "+str(rtt_adj)+", diff: "+str(diff)
                    print line_prev
                    print line_prev2
                    print "start/stop"
                    print line_start
                    print line_stop
                    #rtt_simul.append(rtt_adj)
                    #rtt_orig.append(rtt)
                    """
                    latp[dev].append(rtt_adj)

            elif flag==1:
                temp = line.split('AS')

                if len(temp)>=2:
                    asn=int(temp[1].split(' ')[0])
                    rtt=(temp[0].split(',')[2])
                    if rtt !='':
                        rtt = float(rtt)
                    else:
                        rtt = 0.0
                    cntry=temp[0].split(',')[3]
                    hop=int(temp[0].split(',')[0])


                    if asn not in nw.keys() and flag1==0:
                        flag1=1
                        start = rtt_prev2
                        line_start=line_prev2
                    elif flag1==1 and asn in nw.keys():
                        stop = rtt
                        diff = float(stop)-float(start)

                        flag1==2
                        line_stop = line
                    rtt_prev2=rtt_prev
                    line_prev2=line_prev
                    rtt_prev=rtt
                    line_prev=line
        #print srv
        #print devices
        for dev in devices:
            #print dev
            #print latp[dev]
            total, average, median, standard_deviation, minimum, maximum, confidence = stats(latp[dev])
            #print median
            mlat[srv][dev]=median

    print mlat
    return mlat

def getPlot(lt):
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    #style1 = ['D--','o--','^--','*--']
    style1 = ['p--','*--','o--','^--']

    p1=[]
    lat={}
    i=0
    for ht in lt:
        print i
        print ht
        lat[i]=[]
        for dev in ht.keys():
            lat[i].append(ht[dev])
        i+=1
    print 'lat'
    print lat
    i=0
    for temp in lat.keys():
        p1.append([])
        print temp
        p1[i]=pl.plot(range(1,len(lat[temp])+1), lat[temp], style1[i], color='k', markersize=15.0, linewidth=5.0)
        i+=1
    p=[]
    i=0


    for temp in lat:
        p.append(p1[i][0])
        i+=1
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    pl.legend((p),['Existing Links','Additional Links'],'upper right',prop={'size':16})
    pl.xticks(range(1,len(lat[0])+1))
    pl.ylim(0.1,400)
    pl.xlim(0.9,5.1)
    pl.xlabel('# Cache Servers',fontsize=20)
    pl.ylabel('Average Latency (ms) ',fontsize=20)
    ax.grid(True)
    plot_name='cacheSimul.eps'
    plot_name_png='cacheSimul.png'
    pl.savefig(plot_name)
    pl.savefig(plot_name_png)
    os.system('scp cacheSimul.eps arpit@newton.noise.gatech.edu:~/Writings/glex/PAM14/results/')

def main():
    print "Starting the simulation"
    getKenya()
    print kenya_servers
    #process_traceroute()
    get_latencyMatrix()
    print latency_matrix
    lt_existing = getSimulData(latency_matrix)
    # Now simulate for scenario where KIXP and JINX participants peer with each other.
    asInterface,asName = auxinfo.main()
    print asName
    newworld = coalsec(asName)
    lms = get_SlatencyMatrix(newworld)
    lt_simulated = getSimulData(lms)
    getPlot([lt_existing,lt_simulated])


if __name__ == "__main__":
    main()
