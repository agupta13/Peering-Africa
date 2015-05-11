
#Author: Arpit Gupta (glex.qsd@gmail.com)


import os,sys
import IXP_auxInfo as auxinfo
asInterface={}
asName={}

ixps=['jinx','linx','kixp','ams']
#ixps=['jinx']
ixpPair={}

ofile=open('intersections.txt','w+')

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





def main():

    print "get the aux info"
    asInterface,asName=auxinfo.main()
    level2_overlap(asName)
    ofile.close()

if __name__ == "__main__":
        main()
