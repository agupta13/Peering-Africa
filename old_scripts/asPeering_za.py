# Author: Arpit Gupta

import os,sys
import geoIP_ans as asInfo
import IXP_auxInfo as auxInfo
import itertools


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

countries=['za','ke']
ixps=['jinx','cinx','linx','ams']
#ixps=['jinx']
pch_ixps={'cinx':'cpt','jinx':'jnb','kixp':'nbo','linx':'lhr','ams':'ams'}

asPair={}
ixpIntf={}
ixpName={}

def neighbors( list ):
    i = 0
    while i + 1 < len( list ):
        yield ( list[ i ], list[ i + 1 ] )
        i += 1


def getpchData(asdict,ixpIntf,ixpName):
    for ixp in ixps:
        fname='ribs/'+ixp+'/route-collector.'+pch_ixps[ixp]+'.pch.net.2013.08.16'
        ifile=open(fname,'r')
        for line in ifile.readlines():
            if line.startswith('*>'):
                temp = line.split('\n')[0].split(' 0 ')
                if len(temp)==3:
                    aslist=temp[2].split(' ')
                    aslist=aslist[0:len(aslist)-1]
                    #print aslist
                    for x,y in pairwise(aslist):
                        x=int(x)
                        y=int(y)
                        """
                        if x!=y and (x,y) not in asPair:
                            asPair[(x,y)]=1
                            if y not in asdict['za']:
                                print 'y: outside South Africa'
                                print y
                            if x not in asdict['za']:
                                print 'x: outside South Africa'
                                print x
                            if (ixp,x) in ixpIntf:
                                print 'x: inside IXP'
                                print ixpName[(ixp,x)]
                            if (ixp,y) in ixpIntf:
                                print 'y: inside IXP'
                                print ixpName[(ixp,y)]
                            else:
                                print 'y: not inside IXP'
                                if y in asdict['za']:
                                    print asdict['za'][y]
                        """

def createLists(asdict,ixpIntf,ixpName):
    S1=set([])
    l={}
    for ixp in ixps:
        print ixp
        l[ixp]=[]
    for (ixp,asn) in ixpName:
        if ixp in ixps:
            l[ixp].append(asn)
    for cntry in countries:
        l[cntry]=asdict[cntry].keys()
    for item in l:
        if item =='jinx' or item=='cinx'or item=='za':
            S1=S1.union(set(l[item]))
    return l,S1

def extractASpair(S1):
    asPair={}
    for ixp in ixps:
        fname='ribs/'+ixp+'/route-collector.'+pch_ixps[ixp]+'.pch.net.2013.08.16'
        ifile=open(fname,'r')
        for line in ifile.readlines():
            if line.startswith('*>'):
                temp = line.split('\n')[0].split(' 0 ')
                if len(temp)==3:
                    aslist=temp[2].split(' ')
                    aslist=aslist[0:len(aslist)-1]
                    #print aslist
                    for x,y in pairwise(aslist):
                        if len(x.split(','))==1 and len(y.split(','))==1 and  len(x.split('{'))==1 and len(y.split('{'))==1:
                            x=int(x)
                            y=int(y)
                            if x!=y and (x,y) not in asPair:
                                if x in S1 and y in S1:
                                    asPair[x,y]='pch'
    return asPair

def classifyASpair(listSet,asPair):
    localExchange=[]
    #setLocal=set(listSet['jinx']).union(set(listSet['cinx']))
    internationalExchange=[]
    #setInternational = set(listSet['linx']).union(set(listSet['ams']))
    exchange=[]
    #setExchange=setLocal.union(setInternational)
    direct=[]
    for (as1,as2) in asPair.keys():
        flag=0
        if as1 in listSet['jinx'] and as2 in listSet['jinx']:
            localExchange.append((as1,as2))
            exchange.append((as1,as2))

        elif as1 in listSet['cinx'] and as2 in listSet['cinx']:
            localExchange.append((as1,as2))
            exchange.append((as1,as2))

        elif as1 in listSet['linx'] and as2 in listSet['linx']:
            print 'linx'
            print as1
            print as2
            internationalExchange.append((as1,as2))
            exchange.append((as1,as2))

        elif as1 in listSet['ams'] and as2 in listSet['ams']:
            internationalExchange.append((as1,as2))
            exchange.append((as1,as2))

        else:
            direct.append((as1,as2))

    return localExchange, internationalExchange, exchange, direct

def main():
    print "start AS peering"
    asdict=asInfo.main()
    ixpIntf,ixpName=auxInfo.main()
    listSet, S1 = createLists(asdict,ixpIntf,ixpName)
    asPair = extractASpair(S1)
    localExchange, internationalExchange, exchange, direct = classifyASpair(listSet,asPair)
    print 'the final sets'
    print ''+str(len(localExchange))+','+str(len(internationalExchange))+','+str(len(exchange))+','+str(len(direct))
    #print len(exchange)
    #print len(direct)
    #print len(asPair.keys())
    print 'S1:'
    #print S1
    #print asdict['za'].keys()

    #getpchData(asdict,ixpIntf,ixpName)
    #print asPair



if __name__ == "__main__":
    main()
