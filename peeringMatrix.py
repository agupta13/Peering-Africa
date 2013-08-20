#Author: Arpit Gupta (glex.qsd@gmail.com)

import os, sys
import itertools
import IXP_auxInfo as auxinfo

asInterface={}
aux_asInterface={}
aux_name={}
ixps=['jinx','kixp']
#ixps=['jinx']
tm={}
log_name='log_rib.20130301.0000.txt'
asPair={}




def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


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

                        """
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
                        """

                else:
                    asPair[(ases[0],ases[1])]+=1

def main():
    print "parse the file to map the Interfaces for each AS"
    for ixp in ixps:
        fname='ribs/'+ixp+'/'+log_name
        bgpdump = open(fname,'r')
        for line in bgpdump.readlines():
            if line.startswith('FROM:'):
                info=line.split('\n')[0].split(' ')
                ip = info[1]
                asn=info[2].split('AS')[1]
                if (ixp,asn) not in asInterface:
                    asInterface[ixp,asn]=ip
    (aux_asInterface,aux_name) = auxinfo.main()
    print asInterface
    print aux_asInterface
    print aux_name
    print "try to create the traffic matrix"
    trafficMatrix()
    #print asPair
    print tm

if __name__ == "__main__":
    main()

