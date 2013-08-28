# Author: Arpit Gupta (glex.qsd@gmail.com)


import os, sys

from statistics import *
#import symmetry_analysis
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netaddr import *
from scipy.stats import cumfreq
#import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import statsmodels.api as sm

loc=sys.argv[1]
dfile=open(loc+'_traceroute_processed.txt','r')
proutes=[]
unique={}
unique_as={}
tot_as={}
tot={}
devices=[]
prevalence={}
asprevalence={}
asfreq={}
ipfreq={}

rttDiff={}

ixpinfo={'DE-CIX': '80.81.199.0/24', 'LINX': '195.66.224.0/19', 'AMS-IX': '195.69.144.0/22', 'KIXP': '196.223.21.32/27', 'CINX': '196.223.22.0/24', 'JINX': '196.223.14.0/24'}
private_blocks=['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16']
Cybersmart=['196.6.121.0/24']

def is_private(i):
    ip = IPAddress(i)
    for block in private_blocks:
        if ip in IPNetwork(block):
            return True
    return False

def find_missing_asn(i):
    ip = IPAddress(i)
    if is_private(i) is True:
        return 'private'
    elif ip in IPNetwork(Cybersmart[0]):
        return 'AS36874 Cybersmart (ZA)'
    else:
        for ixp in ixpinfo:
            if ip in IPNetwork(ixpinfo[ixp]):
                return ixp
    return ''

class Route:
    def __init__(self,direction=0,nhop=0,hops={},freq=0,intercont=0,prevl=0.0,consistency=0,count=0,aspath=[],aspathlen=0,asprevl=0.0,asfreq=0,asconsistency=0,ascount=0,hrtt={},rttstats={}):
        self.direction=direction
        self.nhop=nhop
        self.hops=hops
        self.freq=freq
        self.intercont=intercont
        self.prevl=prevl
        self.consistency=consistency
        self.count=count
        self.aspath=aspath
        self.aspathlen=aspathlen
        self.asprevl=asprevl
        self.asfreq=asfreq
        self.asconsistency=asconsistency
        self.ascount=ascount
        self.hrtt=hrtt # per hop rtt values
        self.rttstats=rttstats

def plot_rttdiff():
    for dev in devices:
        for direc in [0,1]:
            for r in unique[(dev,direc)]:
                for hop in range(1,30):
                    if (hop,direc) not in rttDiff:
                        rttDiff[(hop,direc)]=[]

                    else:
                        print "rttstat"
                        print r.rttstats.keys()
                        if hop in r.rttstats:
                            #print "hop: "+str(hop)+" in rttstats"
                            hopp=hop+1

                            if hopp in r.rttstats:

                                rttDiff[(hop,direc)].append(r.rttstats[hopp][2]-r.rttstats[hop][2])
                                print "device: "+dev+" direc: "+str(direc)+" hop: "+str(hop)+" :"+str(r.rttstats[hop][2])+" hop: "+str(hopp)+" :"+str(r.rttstats[hopp][2])+" diff: "+str(r.rttstats[hopp][2]-r.rttstats[hop][2])
    for direc in [0,1]:
        for hop in range(1,30):
            print "direction: "+str(direc)+" hop: "+str(hop)
            print rttDiff[(hop,direc)]

def process_rtt():
    for dev in devices:
        for direc in [0,1]:
            if (dev,direc) in unique:
                for r in unique[(dev,direc)]:
                    #print "device: "+dev+" direc: "+str(direc)
                    dic={}
                    for hop in r.hops:

                        #print "hop "+str(hop)
                        #print r.hrtt[hop][0:7]
                        if hop in r.hrtt:
                            #print "hop: "+str(hop)
                            #print r.hrtt[hop]

                            total0, mean0, median0, stddev0, min0, max0, confidence0 = stats(r.hrtt[hop])
                            a=[total0, mean0, median0, stddev0, min0, max0, confidence0]
                            #print a
                            #print lea)

                            dic[hop]=[]

                            for j in range(0,len(a)):
                                dic[hop].append(a[j])

                    r.rttstats=dic
                    #print "number of keys"
                    #print r.rttstats


def printastofile():
    ofile=open('preval_asresults.txt','w+')
    print "print"
    asprevalence[0]=[]
    asprevalence[1]=[]
    asfreq[0]=[]
    asfreq[1]=[]

    for dev in devices:
        ofile.write('Device: '+dev+'\n')
        for direc in [0,1]:
            maxprevl=0
            maxfreq=0
            if(dev,direc) in unique_as:
                for r in unique_as[(dev,direc)]:
                    r.asprevl=float(r.ascount*100)/tot_as[(dev,direc)]
                    r.asfreq=float(100*r.asfreq)/r.ascount
                    if r.asprevl>maxprevl:
                        maxprevl=r.asprevl
                    #if r.asfreq>maxfreq:
                        maxfreq=r.asfreq
                    ofile.write('direction:'+str(direc)+' AS path len: '+str(r.aspathlen)+
                    ' count: '+str(r.ascount)+' tot: '+str(tot_as[(dev,direc)])+
                    ' prevalence: '+str(r.asprevl)+' freq: '+str(r.asfreq)+'\n')

                    i=1
                    for ashop in r.aspath:
                       ofile.write(str(i)+':'+ashop+'\n')
                       i+=1
                    ofile.write('\n')
                #print "for device: "+dev+" direction: "+str(direc)+" maxprevl: "+str(maxprevl)
                asprevalence[direc].append(maxprevl)
                asfreq[direc].append(maxfreq)
            asprevalence[0].sort()
            asprevalence[1].sort()
            asfreq[0].sort()
            asfreq[1].sort()



def printtofile():
    ofile=open('preval_results.txt','w+')
    prevalence[0]=[]
    prevalence[1]=[]
    ipfreq[0]=[]
    ipfreq[1]=[]
    for dev in devices:
        ofile.write('Device: '+dev+'\n')
        for direc in [0,1]:
            maxprev=0
            maxfreq=0
            if (dev,direc) in unique:
                for r in unique[(dev,direc)]:
                    r.prevl=float(r.count*100)/tot[dev,direc]
                    r.freq=float(r.freq*100)/r.count
                    if r.prevl>maxprev:
                        maxprev=r.prevl
                        maxfreq=r.freq
                    #r.prevl=float(r.freq*100)/tot[dev,direc]
                    ofile.write("direction: "+str(r.direction)+" nhop: "+str(r.nhop)+" intercontinental: "
                    +str(r.intercont)+" count= "+str(r.count)+" prevalence: "
                   +str(r.prevl)+" freq: "+str(r.freq)+'\n')
                    #print "device: "+dev+" direc: "+str(direc)
                    for hop in r.hops:
                        (ip,rtt,cntry,asn)=r.hops[hop]
                        #print "hop: "+str(hop)+" len: "+str((r.hrtt[hop]))
                        ofile.write(""+str(hop)+", "+ip+", ("+str(r.rttstats[hop][2])+";"+str(r.rttstats[hop][6])+"), "+cntry+", "+asn+"\n")
                    ofile.write('\n')
            ipfreq[direc].append(maxfreq)
            prevalence[direc].append(maxprev)
    prevalence[0].sort()
    prevalence[1].sort()
    ipfreq[0].sort()
    ipfreq[1].sort()

def printrt(r):
    print "direction: "+str(r.direction)+" freq="+str(r.freq)+" nhop: "+str(r.nhop)
    for hop in r.hops:
        (ip,rtt,cntry,asn)=r.hops[hop]
        print ""+str(hop)+", "+ip+", "+str(rtt)+", "+cntry+", "+asn

def synch_consistency(did,direc):
    for node in unique[(did,direc)]:
        node.consistency=0

def synch_asconsistency(did,direc):
    for node in unique_as[(did,direc)]:
        node.asconsistency=0

def update_uniqueas(r,did,direction):
    #print did
    if (did,direction) not in unique_as:
        #print "First entry in unique for this pair "+str(direction)+","+did
        r.ascount=1
        r.asfreq=1
        unique_as[(did,direction)]=[]
        unique_as[(did,direction)].append(r)
        tot_as[(did,direction)]=1
    else:
        tot_as[(did,direction)]+=1
        match=0
        for entry in unique_as[(did,direction)]:
            if entry.aspathlen != r.aspathlen:
                continue
            elif entry.direction!=r.direction:
                continue
            else:
                hmatch=1
                i=0
                for ashop in entry.aspath:
                    if ashop !=r.aspath[i]:
                        hmatch=0
                        break
                    i+=1

                if hmatch==1:
                    match=1
                    if entry.asconsistency==0:
                        entry.asfreq+=1
                        synch_asconsistency(did,direction)
                        entry.asconsistency=1
                    entry.ascount+=1
                    break


        if match==0:

            r.ascount=1
            r.asfreq=1
            """#print "No entry found for:"
            #print r.aspath
            #print "Compared agaisnt"
            for entry in unique_as[(did,direction)]:
                print entry.aspath
            """
            unique_as[(did,direction)].append(r)



def update_unique(r,did,direction):
    #print did
    if (did,direction) not in unique:
        r.count=1
        r.freq=1
        """
        a={}
        for hop in r.hops:
            a[hop]=[0]
        r.hrtt=a
        """
        unique[(did,direction)]=[]
        unique[(did,direction)].append(r)
        tot[(did,direction)]=1
    else:
        tot[(did,direction)]+=1
        match=0
        #print "size unique: "+str(len(unique))
        for entry in unique[(did,direction)]:
            if entry.nhop!=r.nhop:
                continue
            elif entry.direction!=r.direction:
                continue
            else:
                #print "same direction and nhop"
                hmatch=1
                for hp in range(1,entry.nhop+1):
                    if hp in entry.hops and hp in r.hops:
                        if entry.hops[hp][0] != r.hops[hp][0]:
                            # ip addresses have not matched, check if they belong to same AS and same country
                            hmatch=0
                            if entry.hops[hp][2]==r.hops[hp][2] and entry.hops[hp][3]==r.hops[hp][3]:
                                hmatch=1
                                break
                    elif hp not in entry.hops and hp not in r.hops:
                        continue
                    """elif hp!=1 and hp!=entry.nhop:
                        hmatch=0
                        break
                    """
                if hmatch==1:
                    match=1
                    if entry.consistency == 0:
                        entry.freq+=1
                        synch_consistency(did,direction)
                        entry.consistency=1
                        for hop in entry.hops:
                            if hop in r.hops:
                                if hop in entry.hrtt:
                                    entry.hrtt[hop].append(float(r.hops[hop][1]))
                                else:
                                    #print "really can this actually happen !!"
                                    entry.hrtt[hop]=[]
                                    entry.hrtt[hop].append(float(r.hops[hop][1]))
                                    entry.rttstats[hop]=[]
                                #print entry.hrtt
                    #print "match found, no unique entry"
                    entry.count+=1
                    break
                    # update the freq here
                else:
                    match=0

        if match==0:
            # unique entry found
            #print "unique entry added"
            r.count=1
            r.freq=1
            unique[(did,direction)].append(r)




def main():
    rta=Route()
    flag=0
    direction=0
    devid=''
    temppath=[]
    asplen=0
    for line in dfile.readlines():
        if line.startswith('Device id'):
            d=line.split('\n')[0].split(': ')[1]
            devid=line.split('Device id:')[1].split(',')[0]
            """if devid=='2CB05D8302A5':
                break
            """
            if devid not in devices:
                devices.append(devid)
            if d=='from Mlab_Nairobi':
                direction=0
            else:
                direction=1

        elif line.startswith('hops:'):
            flag=1
            nhop=int(line.split('\n')[0].split(': ')[1])
            rt=Route(direction,nhop,{},0)
            rt.aspathlen=0
            temppath=[]
            asplen=0
            1000
        elif flag==1  and line!='\n':
            #print line
            temp = line.split('\n')[0].split(',')
            #rt.hops[int(temp[0])]=(temp[1],temp[2],temp[3],temp[4])

            if temp[4]=='':
                temp[4]=find_missing_asn(temp[1])
            if temp[4] not in temppath and temp[4] is not 'private':
                temppath.append(temp[4])
                asplen+=1
            rt.hops[int(temp[0])]=(temp[1],temp[2],temp[3],temp[4])
            """
            hopn=int(temp[0]) # hop number
            # Updating the RTT value
            if hopn in rt.hrtt:
                print len(rt.hrtt)
                rt.hrtt[hopn].append(float(temp[2]))
            else:
                rt.hrtt[hopn]=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,float(temp[2])]


            if temp[2]!='Kenya' or temp[2]!='South Africa' or temp[2]!='':
                rt.intercont=1

            """
        elif flag==1 and line=='\n':
            flag=0
            rta=rt
            #print "temp path"
            #print temppath
            rta.aspath=temppath
            rta.aspathlen=asplen
            update_unique(rta,devid,direction)
            update_uniqueas(rta,devid,direction)
            proutes.append(rta)
            #print "change"
    #for route in proutes:
    #    printrt(route)

    print "Unique entries"
    """for route in unique:
        printrt(route)
    """
    #print unique_as[('2CB05D830287',1)]
    #print prevalence
    process_rtt()
    plot_rttdiff()
    printtofile()
    printastofile()

    print prevalence
    print asprevalence
    print ipfreq
    print asfreq
    print "## Plot the frequency and Prevalence"

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    i=0
    p1=[]
    direction=['downstream','upstream']
    for direc in [0,1]:
        a=prevalence[direc]
        num_bins=10000
        counts, bin_edges = np.histogram(a,bins=num_bins,normed=True)
        cdf=np.cumsum(counts)
        scale = 1.0/cdf[-1]
        cdf=cdf*scale
        p1.append([])
        p1[direc]=pl.plot(bin_edges[1:],cdf,label=direction[direc],color=color_n[direc], linewidth=5.0)

    p=[]
    i=0
    for direc in direction:
        p.append(p1[i][0])
        i+=1
    pl.ylim(0.00,1.00)
    pl.xlim(-1,100)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    pl.legend((p),direction,'upper left',prop={'size':32})
    pl.xlabel('Most Prevalent Routes (%)',fontsize=32)
    pl.ylabel('# Paths ',fontsize=32)
    ax.grid(True)
    plot_name='route_preval_'+loc+'.eps'
    plot_name_png='route_preval_'+loc+'.png'
    pl.savefig(plot_name)
    pl.savefig(plot_name_png)

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    i=0
    p1=[]
    direction=['downstream','upstream']
    for direc in [0,1]:
        a=ipfreq[direc]
        num_bins=10000
        counts, bin_edges = np.histogram(a,bins=num_bins,normed=True)
        cdf=np.cumsum(counts)
        scale = 1.0/cdf[-1]
        cdf=cdf*scale
        p1.append([])
        p1[direc]=pl.plot(bin_edges[1:],cdf,label=direction[direc],color=color_n[direc], linewidth=5.0)

    p=[]
    i=0
    for direc in direction:
        p.append(p1[i][0])
        i+=1
    pl.ylim(0.00,1.00)
    pl.xlim(-1,100)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    pl.legend((p),direction,'lower right',prop={'size':32})
    pl.xlabel('Frequency (%)',fontsize=32)
    pl.ylabel('# Paths ',fontsize=32)
    ax.grid(True)
    plot_name='route_preval_freq_'+loc+'.eps'
    plot_name_png='route_preval_freq_'+loc+'.png'
    pl.savefig(plot_name)
    pl.savefig(plot_name_png)

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    i=0
    p1=[]
    direction=['downstream','upstream']
    for direc in [0,1]:
        a=asprevalence[direc]
        num_bins=10000
        counts, bin_edges = np.histogram(a,bins=num_bins,normed=True)
        cdf=np.cumsum(counts)
        scale = 1.0/cdf[-1]
        cdf=cdf*scale
        p1.append([])
        p1[direc]=pl.plot(bin_edges[1:],cdf,label=direction[direc],color=color_n[direc], linewidth=5.0)

    p=[]
    i=0
    for direc in direction:
        p.append(p1[i][0])
        i+=1
    pl.ylim(0.00,1.00)
    pl.xlim(-1,100)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    pl.legend((p),direction,'upper left',prop={'size':32})
    pl.xlabel('Most Prevalent Routes (%)',fontsize=32)
    pl.ylabel('# Paths ',fontsize=32)
    ax.grid(True)
    plot_name='asroute_preval_'+loc+'.eps'
    plot_name_png='asroute_preval_'+loc+'.png'
    pl.savefig(plot_name)
    pl.savefig(plot_name_png)

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    i=0
    p1=[]
    direction=['downstream','upstream']
    for direc in [0,1]:
        a=asfreq[direc]
        num_bins=10000
        counts, bin_edges = np.histogram(a,bins=num_bins,normed=True)
        cdf=np.cumsum(counts)
        scale = 1.0/cdf[-1]
        cdf=cdf*scale
        p1.append([])
        p1[direc]=pl.plot(bin_edges[1:],cdf,label=direction[direc],color=color_n[direc], linewidth=5.0)

    p=[]
    i=0
    for direc in direction:
        p.append(p1[i][0])
        i+=1
    pl.ylim(0.00,1.00)
    pl.xlim(-1,100)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    pl.legend((p),direction,'lower right',prop={'size':32})
    pl.xlabel('Frequency (%)',fontsize=32)
    pl.ylabel('# Paths ',fontsize=32)
    ax.grid(True)
    plot_name='asroute_preval_freq_'+loc+'.eps'
    plot_name_png='asroute_preval_freq_'+loc+'.png'
    pl.savefig(plot_name)
    pl.savefig(plot_name_png)



    """fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    color_n=['g','m','c','r','b','k','w']
    p1=[]
    direction=['downstream','upstream']
    for direc in [0,1]:
        a="""

    os.system('cp *.eps *png ../scripts/')

if __name__=="__main__":
    main()
