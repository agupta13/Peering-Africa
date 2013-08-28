# Author: Aprit Gupta (****.qsd@gmail.com)

import os,sys
ixps=['jinx','kixp']
asInterface={}
asName={}

def parse_auxInfo(ixp):
    fname ='peeringInfo_'+ixp+'.txt'
    auxfile=open(fname,'r')
    for line in auxfile.readlines():
        data=line.split('\n')[0]
        if ixp=='kixp' and len(data.split(','))==4:
            asn=int(data.split(', ')[1])
            name=data.split(', ')[0]
            ip = data.split(', ')[2]

            asInterface[(ixp,asn)]=ip
            asName[(ixp,asn)]=name
        if ixp=='jinx' and len(data.split(','))==3:
            #print data
            asn = int(data.split(', ')[1])
            name=data.split(', ')[0]
            asName[(ixp,asn)]=name
    #print asInterface
    #print asName

def main():
    print "start the auxInfo processing"
    for ixp in ixps:
        parse_auxInfo(ixp)

    return (asInterface,asName)

if __name__ == "__main__":
    main()
