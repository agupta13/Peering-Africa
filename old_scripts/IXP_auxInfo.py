# Author: Aprit Gupta (glex.qsd@gmail.com)

import os,sys
#ixps=['jinx','kixp','linx','ams','cinx']
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
            asInterface[(ixp,asn)]=''
        if ixp=='linx' and len(data.split(', '))==3:
            asna = (data.split(', ')[1])
            name = data.split(', ')[0]
            ip = data.split(', ')[2]

            for i in range(0,len(asna.split(','))):
                asn = int(asna.split(',')[i])
                asInterface[(ixp,asn)]=ip
                asName[(ixp,asn)]=name
        if ixp=='ams' and len(data.split(', '))==14:
            temp=data.split(', ')
            asn=int(temp[3])
            name=temp[0]
            ip=''
            asInterface[(ixp,asn)]=ip
            asName[(ixp,asn)]=name
        if ixp=='cinx' and len(data.split(','))==3:
            asn = int(data.split(',')[1])
            name=data.split(',')[0]
            asName[(ixp,asn)]=name
            asInterface[(ixp,asn)]=''

    #print len(asInterface.keys())
    #print asName

def main():
    print "start the auxInfo processing"
    #print ixps1
    #ixps=ixps1
    for ixp in ixps:
        parse_auxInfo(ixp)
    #print asName
    return (asInterface,asName)

if __name__ == "__main__":
    main()
