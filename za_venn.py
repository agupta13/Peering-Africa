
#Author: Arpit Gupta (glex.qsd@gmail.com)


import os,sys
import geoIP_ans as asInfo
import IXP_auxInfo as auxinfo
import itertools

asInterface={}
asName={}

#ixps=['jinx','linx','kixp','ams','cinx']
#countries=['za','ke']
#ixps=['linx','kixp','ams']
#countries=['ke']
ixps=['jinx','linx','ams','cinx']
countries=['za']

#ixps=['jinx']
ixpPair={}

ofile=open('intersections.txt','w+')
listSet={}

def level2_overlap(asName):
    intersection=[]
    for ixp1 in ixps:
        #ofile.write(''+ixp1)
        for ixp2 in ixps:
            if ixp1!=ixp2:
                if ((ixp1,ixp2) in ixpPair or (ixp2,ixp1) in ixpPair) is False:
                    ixpPair[ixp1,ixp2]=1
                    ofile.write(ixp1.upper()+' AND '+ixp2.upper()+'\n')
                    l1=[]
                    l2=[]
                    for (ex,asn) in asName:
                        #print ex
                        if ex==ixp1:
                            l1.append(asn)
                        elif ex==ixp2:
                            l2.append(asn)
                    print "for "+ixp1+" and "+ixp2
                    #print l1
                    #print l2
                    intersection = list(set(l1) & set(l2))
                    print intersection
                    for asn in intersection:
                        ofile.write('AS'+str(asn)+' '+asName[(ixp1,asn)]+'\n')
                    ofile.write('\n')



def getList(asdict,asName):
    l={}
    for ixp in ixps:
        l[ixp]=[]
        for (ex,asn) in asName:
            if ex==ixp:
                l[ixp].append(asn)
    for cntry in countries:
        l[cntry]=asdict[cntry].keys()

    return l

def getoverlaps(listSet):
    height=len(listSet.keys())
    name=listSet.keys()
    nameset = {}
    count=0
    l={}
    while height>1:
        nameset[height]=set(itertools.combinations(name, height))
        print len(list(nameset[height]))
        print "height: "+str(height)

        for item in list(nameset[height]):
            count+=1
            sl=[]
            for memb in item:
                sl.append(set(listSet[memb]))
            #print sl
            u = set.intersection(*sl)
            print '## intersection set for: '
            print item
            print u
            l[item]=list(u)
        height-=1
    print nameset
    print count
    return l

#def process_zaData():


def main():

    print "get the aux info"
    asInterface,asName=auxinfo.main()
    asdict=asInfo.main()
    print asdict
    listSet=getList(asdict,asName)
    print "## Final list set"
    overlaps = getoverlaps(listSet)
    print overlaps


    #print listSet.keys()

    #for key in overlaps.keys():
    #    print key[0]
    #level2_overlap(asName)
    ofile.close()

if __name__ == "__main__":
        main()
