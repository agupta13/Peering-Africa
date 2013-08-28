# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,sys
import numpy
#import matplotlib.pyplot as plt

dfile=open('nairobi_symmetry_processedc.txt','r')

tot={}
devices=[]



class Route:
    def __init__(self,direction=0,nhop=0,hops={},freq=0,intercont=0,prevl=0.0,consistency=0,count=0,aslist=[],did=''):
        self.direction=direction
        self.nhop=nhop
        self.hops=hops
        self.freq=freq
        self.intercont=intercont
        self.prevl=prevl
        self.consistency=consistency
        self.count=count
        self.aslist=aslist
        self.did=did

def printrt(r):
    print "devid: "+r.did+" direction: "+str(r.direction)+" freq="+str(r.freq)+" nhop: "+str(r.nhop)
    for asn in r.aslist:
        print asn
    for hop in r.hops:
        (ip,rtt,cntry,asn)=r.hops[hop]
        print ""+str(hop)+", "+ip+", "+str(rtt)+", "+cntry+", "+asn

path_ip_symmetric={}
path_ip_total={}

path_as_symmetric={}
path_as_total={}

def is_ipsymmetric(r1,r2):
    #print "test for symmetry"
    #printrt(r1)
    #printrt(r2)
    devid=r1.did
    #print devid
    if devid in path_ip_total:
        path_ip_total[devid]+=1
    else:
        path_ip_total[devid]=1
    # check if number of hops match
    symmetry=1
    if r1.nhop==r2.nhop:
        l=r1.nhop
        for hop in range(1,l+1):
            rev_hop=l-hop+1
            if hop in r1.hops and rev_hop in r2.hops:
                if r1.hops[hop][0]!=r2.hops[rev_hop][0]:
                    # symmetry=0 Let us be more flexible
                    if r1.hops[hop][3]!=r2.hops[rev_hop][3]:
                        # different IP different AS, no way this dude is a symmetric route
                        symmetry=0
    else:
        #print 'different nhops'
        symmetry=0
    if symmetry==1:
        if devid in path_ip_symmetric:
            path_ip_symmetric[devid]+=1
        else:
            path_ip_symmetric[devid]=1
    else:
        if devid not in path_ip_symmetric:
            path_ip_symmetric[devid]=0

def is_assymmetric(r1,r2):
    #print "test for as-symmetry"
    symmetry=1
    devid=r1.did
    """print r1.aslist
    print r2.aslist"""
    if devid in path_as_total:
        path_as_total[devid]+=1
    else:
        path_as_total[devid]=1
    if len(r1.aslist) == len(r2.aslist):
        for order in range(0,len(r1.aslist)):
            rev_order=len(r1.aslist)-order-1
            if r1.aslist[order]!=r2.aslist[rev_order]:
                symmetry=0
    else:
        symmetry=0
    if symmetry==1:
        if devid in path_as_symmetric:
            path_as_symmetric[devid]+=1
        else:
            path_as_symmetric[devid]=1
    else:
        if devid not in path_as_symmetric:
            path_as_symmetric[devid]=0

ip_symmetry=[]
as_symmetry=[]

def analyse_data():
    for dev in devices:
        ip_symmetry.append(float(path_ip_symmetric[dev])*100/float(path_ip_total[dev]))
        as_symmetry.append(float(path_as_symmetric[dev])*100/float(path_as_total[dev]))
        #print "dev: "+dev+" ip: "+str(float(path_ip_symmetric[dev])*100/float(path_ip_total[dev]))+" as: "+str(float(path_as_symmetric[dev])*100/float(path_as_total[dev]))

    ip_symmetry.sort()
    as_symmetry.sort()
    print ip_symmetry
    #print as_symmetry

def plot_symmetry():
    print "later"

def main():
    rt_cur=Route()
    rt_prev=Route()
    flag=0
    direction=0
    devid=''
    asn_prev=''
    for line in dfile.readlines():
        if line.startswith('Device id'):
            d=line.split('\n')[0].split(': ')[1]
            devid=line.split('Device id:')[1].split(',')[0]
            if devid not in devices:
                devices.append(devid)

        elif line.startswith('hops:'):
            flag=1
            nhop=int(line.split('\n')[0].split('hops: ')[1].split(' direction: ')[0])
            direction=int (line.split('\n')[0].split('hops: ')[1].split(' direction: ')[1])
            rt=Route(direction,nhop,{},0)
            #print devid
            rt.did=devid
            rt.aslist=[]
        elif flag==1  and line!='\n':
            #print line
            temp = line.split('\n')[0].split(',')
            asn=temp[4].split(' ')[0]
            if asn!=asn_prev:
                rt.aslist.append(asn)
                asn_prev=asn
            rt.hops[int(temp[0])]=(temp[1],temp[2],temp[3],temp[4])
            if temp[2]!='Kenya' or temp[2]!='South Africa' or temp[2]!='':
                rt.intercont=1
        elif flag==1 and line=='\n':
            flag=0
            asn_prev=''
            if direction==1:
                rt_prev=rt
            elif direction==0:
                rt_cur=rt
                is_ipsymmetric(rt_prev,rt_cur)
                is_assymmetric(rt_prev,rt_cur)


    print "Symmetry Analysis done"
    #print path_ip_symmetric
    #print path_ip_total
    #print path_as_symmetric
    #print path_as_total

    # Analyse the symmetry data
    analyse_data()
    #plot_symmetry()



if __name__=="__main__":
    main()
