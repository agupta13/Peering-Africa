#Author: Arpit Gupta (****.qsd@gmail.com)

import os, sys
import itertools
import IXP_auxInfo as auxinfo

asInterface={}
aux_asInterface={}
aux_name={}
ixps=['jinx','kixp']
#ixps=['kixp']
tm={}
log_name='log_rib.20130301.0000.txt'
asPair={}
uniqueAS={}



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
                ases[1]=int(ases[1])
                ases[0]=int(ases[0])
                for j in [0]:
                    if ases[j] not in uniqueAS[ixp]:
                        uniqueAS[ixp].append(ases[j])


                if (ases[0],ases[1]) not in asPair:
                    asPair[(ases[0],ases[1])]=1
                    #print (ixp,ases[1])
                    #if ases[1]==25568:
                    #    print aux_asInterface
                    #if (ixp,ases[1]) in aux_asInterface:
                    #    print "match in aux db"
                    #    print ases[1]
                    if (ixp,ases[1]) in asInterface or (ixp,ases[1]) in aux_asInterface:
                        #print "the two ASes might peer at IXP itself. Need to confirm that"
                        #print line
                        #print next_line
                        if ases[1] not in uniqueAS[ixp]:
                            uniqueAS[ixp].append(ases[1])
                        if (ixp,ases[0]) in tm:
                            tm[(ixp,ases[0])].append(ases[1])
                        else:
                            tm[(ixp,ases[0])]=[ases[1]]                       

                else:
                    asPair[(ases[0],ases[1])]+=1

def print_pm():
    for ixp in ixps:
        ofile = open('pm_'+ixp+'.txt','w+')
        ofile.write('\t')
        for k in range(0,len(uniqueAS[ixp])):
            ofile.write(str(uniqueAS[ixp][k])+' ')
        ofile.write('\n')
        for i in range(0,len(uniqueAS[ixp])):
            as1=uniqueAS[ixp][i]
            ofile.write(str(as1)+' '+aux_name[as1]+': ')
            for j in range(0,len(uniqueAS[ixp])):
 
                if (ixp,as1) in tm:
                    #ofile.write(str(as1)+': ')
                    #as1=uniqueAS[ixp][i]
                    as2=uniqueAS[ixp][j]
                    if as2 in tm[(ixp,as1)]:
                        ofile.write("True ")
                    else: 
                        ofile.write("False ")
                else:
                    ofile.write("NA ")
            ofile.write("\n")
            
        ofile.write("\n")

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
    #print aux_name
    print "Create the traffic matrix"
    trafficMatrix_aggr(aux_asInterface)
    #print asPair
    print tm
    print uniqueAS
    print "print the Traffic Matrix"
    print_pm()

if __name__ == "__main__":
    main()

