# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,re,string, sys
import logging as log
import bgp_rib

dir = "/Users/arpit/Bismark_bgp/logs/ribs/"

prefix_list=[]
possible_prefix=[]

def adjust(a,net):
    n=int(a)
    b = bin(n)
    out=fin=''
    for j in range(1,len(b)-1):
        out = b[len(b)-j]+out
    for j in range(0,8-len(out)):
        out='0'+out

    for j in range(0,8):       
        if(j>=net):
            fin=fin+'0'
        else:
            fin=fin+out[j]
    return str(int(fin,2))
           
def cal_sub(ip,net):
    ip4=ip.split('.')[0]
    ip3=ip.split('.')[1]
    ip2=ip.split('.')[2]
    ip1=ip.split('.')[3]
    net=32-net
    if net <=32 and net>24:
        ip4 = adjust(ip4,32-net)
        out=ip4+'.0.0.0'                  
        return out
    if net <=24 and net>16:
        ip3 = adjust(ip3,24-net)
        out=ip4+'.'+ip3+'.0.0'
        return out
    if net <=16 and net>8:
        ip2 = adjust(ip2,16-net)
        out=ip4+'.'+ip3+'.'+ip2+'.0'
        return out
    if net <=8 and net>0:
        ip1 = adjust(ip1,8-net)
        out=ip4+'.'+ip3+'.'+ip2+','+ip1
        return out


def possible_prefixes():
    ind = 0
    for prefix in prefix_list:
        possible_prefix.append([])
        for i in range(1,33):
            ip = cal_sub(prefix,i)
            possible_prefix[ind].append(ip)
        print len(possible_prefix[ind])
        ind = ind+1
            

def read_prefixFile():
    pfile = open('plist.txt','r')
    for line in pfile.readlines():
        prefix_list.append(line.split('\n')[0])

def parser():
    logfile = open('test.txt','r')
    flag=0, 
    init_dict=0
    net=''
    ip=''
    prefix_data=[]
    dict={}
    for line in logfile.readlines():        
        if line.startswith('PREFIX:'):
            net=line.split('/')[1].split('\n')[0]
            ip = line.split(': ')[1].split('/')[0]
            #print ip
            if ip == possible_prefix[0][int(net)]:
                flag=1
                if init_dict==0:
                    dict[ip]=prefix_data
                    init_dict=1
                bgpdata=bgp_rib.bgpData()
                bgpdata.prefix=ip+'/'+net
                #print bgpdata.prefix
        if flag==1:
            if line.startswith('\n'):
                print bgpdata.aspath
                dict[ip].append(bgpdata)
                flag=0
            if line.startswith('From'):
                bgpdata.nbr_ip = line.split(' ')[1]
                bgpdata.nbr_as = line.split(' ')[2].split('\n')[0]
            if line.startswith('ASPATH'):
                bgpdata.aspath= line.split(': ')[1].split('\n')[0]
    print dict['75.121.176.0'][0].aspath
    
                

def main():
    print "Started the prefix search"
    print "read prefixes.."
    read_prefixFile()
    print prefix_list
    print "possible prefixes"
    possible_prefixes()
    print possible_prefix
    print "Parse the log files"
    parser()

if __name__ == "__main__":
    main()