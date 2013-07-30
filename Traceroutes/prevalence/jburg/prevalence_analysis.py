# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,sys
import numpy
import matplotlib.pyplot as plt

dfile=open('jburg_traceroute_processed146.txt','r')
proutes=[]
unique={}
tot={}
devices=[]
prevalence={}

class Route:
    def __init__(self,direction=0,nhop=0,hops={},freq=0,intercont=0,prevl=0.0):
        self.direction=direction
        self.nhop=nhop
        self.hops=hops
        self.freq=freq
        self.intercont=intercont
        self.prevl=prevl

def printtofile():
    ofile=open('preval_results.txt','w+')
    prevalence[0]=[]
    prevalence[1]=[]    
    for dev in devices:
        ofile.write('Device: '+dev+'\n')        
        for direc in [0,1]:
            maxprev=0
            if (dev,direc) in unique:
                for r in unique[(dev,direc)]:
                    r.prevl=float(r.freq*100)/tot[dev,direc]
                    if r.prevl>maxprev:
                        maxprev=r.prevl
                    #r.prevl=float(r.freq*100)/tot[dev,direc]
                    ofile.write("direction: "+str(r.direction)+" nhop: "+str(r.nhop)+" intercontinental: "+str(r.intercont)+" freq="+str(r.freq)+" prevalence: "+str(r.prevl)+'\n')
                    for hop in r.hops:
                        (ip,rtt,cntry,asn)=r.hops[hop]
                        ofile.write(""+str(hop)+", "+ip+", "+str(rtt)+", "+cntry+", "+asn+"\n")
                    ofile.write('\n')
            prevalence[direc].append(maxprev)
    prevalence[0].sort()
    prevalence[1].sort()

def printrt(r):
    print "direction: "+str(r.direction)+" freq="+str(r.freq)+" nhop: "+str(r.nhop)
    for hop in r.hops:
        (ip,rtt,cntry,asn)=r.hops[hop]
        print ""+str(hop)+", "+ip+", "+str(rtt)+", "+cntry+", "+asn

def update_unique(r,did,direction):
    if (did,direction) not in unique:
        r.freq=1
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
                    #print "match found, no unique entry"
                    entry.freq+=1
                    break
                    # update the freq here
                else:
                    match=0
        if match==0:
            # unique entry found
            #print "unique entry added"
            r.freq=1
            unique[(did,direction)].append(r)
def main():
    rta=Route()
    flag=0
    direction=0
    devid=''
    for line in dfile.readlines():
        if line.startswith('Device id'):
            d=line.split('\n')[0].split(': ')[1]
            devid=line.split('Device id:')[1].split(',')[0]
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
        elif flag==1  and line!='\n':
            #print line
            temp = line.split('\n')[0].split(',')
            rt.hops[int(temp[0])]=(temp[1],temp[2],temp[3],temp[4])
            if temp[2]!='Kenya' or temp[2]!='South Africa' or temp[2]!='':
                rt.intercont=1
        elif flag==1 and line=='\n':
            flag=0
            rta=rt
            update_unique(rta,devid,direction)
            proutes.append(rta)
            #print "change"
    #for route in proutes:
    #    printrt(route)

    print "Unique entries"
    """for route in unique:
        printrt(route)
    """
    printtofile()
    print prevalence
    num_bins = 20
    counts, bin_edges = numpy.histogram(prevalence[0], bins=num_bins, normed=True)
    cdf = numpy.cumsum(counts)
    plt.plot(bin_edges[1:], cdf)
    print cdf
    print bin_edges[1:]
    #print unique
    #print tot

if __name__=="__main__":
    main()

