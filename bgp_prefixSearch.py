# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,re,string, sys
import logging as log
import bgp_rib

dir = "/Users/arpit/Bismark_bgp/logs/ribs/"

prefix_list=[]
possible_prefix=[]
prefix_identified=[]
dict = {}

def adjust(a,net):
    n=int(a)
    b = bin(n)
    out=fin=''
    for j in range(1,len(b)-1):
        out = b[len(b)-j]+out
    for j in range(0,8-len(out)):
        out='0'+out

    for j in range(0,8):       
        if j>=net:
            fin+='0'
        else:
            fin+=out[j]
    return str(int(fin,2))
           
def cal_sub(ip,net):
    ip4=ip.split('.')[0]
    ip3=ip.split('.')[1]
    ip2=ip.split('.')[2]
    ip1=ip.split('.')[3]
    net=32-net
    if 32 >= net > 24:
        ip4 = adjust(ip4,32-net)
        out = ip4+'.0.0.0'
        return out
    if 24 >= net > 16:
        ip3 = adjust(ip3,24-net)
        out = ip4+'.'+ip3+'.0.0'
        return out
    if 16 >= net > 8:
        ip2 = adjust(ip2,16-net)
        out = ip4+'.'+ip3+'.'+ip2+'.0'
        return out
    if 8 >= net > 0:
        ip1 = adjust(ip1,8-net)
        out = ip4+'.'+ip3+'.'+ip2+'.'+ip1
        return out


def possible_prefixes():
    ind = 0
    for prefix in prefix_list:
        possible_prefix.append([])
        for i in range(1,32):
            ip = cal_sub(prefix,i)
            possible_prefix[ind].append(ip)
        #print len(possible_prefix[ind])
        ind += 1
            

def read_prefixFile():
    pfile = open('plist.txt','r')
    for line in pfile.readlines():
        prefix_list.append(line.split('\n')[0])

def parser():
    ip = ''

    for ind in range(0,len(prefix_list)):
        print 'Searching for ip: '+prefix_list[ind]
        flag = 0
        init_dict = 0
        prefix_data = []
        logfile = open('test.txt','r')
        for line in logfile.readlines():
            if line.startswith('PREFIX:'):
                net = line.split('/')[1].split('\n')[0]
                ip = line.split(': ')[1].split('/')[0]
                #print ip+','+net
                #print possible_prefix[ind][int(net)]
                #print init_dict
                if ip == possible_prefix[ind][int(net)]:
                    flag=1
                    if init_dict==0:
                        #print "init dict entry called"
                        if not (ip in dict):
                            print 'dict init cond satisfied'
                            dict[ip]=prefix_data
                            init_dict=1
                            prefix_identified.append(ip)
                        else:
                            print 'identified repetition'
                            break
                    bgpdata=bgp_rib.bgpData()
                    bgpdata.prefix=ip+'/'+net
                    bgpdata.aspath=[]
                    #print bgpdata.prefix
            if flag==1:
                if line.startswith('NEXT_HOP'):
                    #print bgpdata.aspath
                    dict[ip].append(bgpdata)
                    flag=0
                if line.startswith('From'):
                    bgpdata.nbr_ip = line.split(' ')[1]
                    bgpdata.nbr_as = line.split(' ')[2].split('\n')[0]
                if line.startswith('ASPATH'):
                    for i in range(0,len(line.split(': ')[1].split('\n')[0].split(' '))):
                        bgpdata.aspath.append(line.split(': ')[1].split('\n')[0].split(' ')[i])
    print dict['75.121.176.0'][0].aspath
        #print dict[possible_prefix[ind][int(net)]][1].aspath
                

def main():
    print "Started the program ..."
    print "Read prefixes from the plist file ..."
    read_prefixFile()
    print prefix_list
    print "Determine possible prefixes ..."
    possible_prefixes()
    #print possible_prefix
    print "Parse the log files ..."
    parser()
    print 'Identified prefixes: '
    print prefix_identified
    print 'Output dictionary: '
    print dict

if __name__ == "__main__":
    main()