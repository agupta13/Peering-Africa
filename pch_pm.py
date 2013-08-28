
#Author: Arpit Gupta (glex.qsd@gmail.com)


import os,sys
import IXP_auxInfo as auxinfo
asInterface={}
asName={}

#ixps=['jinx','linx','kixp']
ixps=['ams']

pch_ixps={'jinx':'jnb','kixp':'nbo','linx':'lhr','ams':'ams'}
asPair={}
tm={}
entries={}
uniqueAS={}

def print_pm(aux_name):
    for ixp in ixps:
        ofile = open('pch_pm_'+ixp+'.txt','w+')
        ofile.write(' : ')
        for k in range(0,len(uniqueAS[ixp])):
            ofile.write('AS'+str(uniqueAS[ixp][k])+' ')
        ofile.write('\n')
        for i in range(0,len(uniqueAS[ixp])):
            as1=uniqueAS[ixp][i]
            if (ixp,as1) not in tm:
                continue
            if (ixp,as1) in aux_name:
                ofile.write('AS'+str(as1)+' '+aux_name[(ixp,as1)]+': ')
            else:
                ofile.write('AS'+str(as1)+' .. : ')

            for j in range(0,len(uniqueAS[ixp])):

                if (ixp,as1) in tm:
                    #ofile.write(str(as1)+': ')
                    #as1=uniqueAS[ixp][i]
                    as2=uniqueAS[ixp][j]
                    if as2 in tm[(ixp,as1)]:
                        ofile.write("Yes ")
                    else:

                        ofile.write("No ")
                else:
                    i=1
                    #ofile.write("N/A ")
            ofile.write("\n")

        ofile.write("\n")




def peeringMatrix(asInterface):
    for ixp in ixps:
        print ixp
        uniqueAS[ixp]=[]
        fname='ribs/'+ixp+'/route-collector.'+pch_ixps[ixp]+'.pch.net.2013.08.16'
        print fname
        pfile=open(fname,'r')
        for line in pfile.readlines():
            if line.startswith('*>'):
                if len(line.split(' 0 '))==3:
                    data = line.split('\n')[0].split(' 0 ')[2]
                    if len(data.split(' '))>=3:
                        as1=int(data.split(' ')[0])
                        as2=int(data.split(' ')[1])
                        if as1!=as2:
                            if as1 not in uniqueAS[ixp]:
                                uniqueAS[ixp].append(as1)

                            if (ixp,as1,as2) in asPair:
                                asPair[(ixp,as1,as2)]+=1
                            else:
                                asPair[(ixp,as1,as2)]=1
                                if (ixp,as2) in asInterface:
                                    if as2 not in uniqueAS[ixp]:
                                        uniqueAS[ixp].append(as2)

                                    if (ixp,as1) in tm:
                                        tm[(ixp,as1)].append(as2)
                                    else:
                                        tm[(ixp,as1)]=[as2]
                                        if ixp not in entries:
                                            entries[ixp]=1
                                        else:
                                            entries[ixp]+=1



def main():
    print "Start analysing PCH data"
    asInterface,asName=auxinfo.main()
    peeringMatrix(asInterface)
    #print asPair
    print tm
    print entries
    print_pm(asName)


if __name__ == "__main__":
        main()
