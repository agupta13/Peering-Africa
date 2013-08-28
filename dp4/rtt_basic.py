# Author : Arpit Gupta (****.qsd@gmail.com)

import pg
import os, sys
from statistics import *


servers=[]
devices=[]


fopen=open('servers_paristraceroute.txt','r')

# update list of servers
for line in fopen.readlines():
    servers.append(line.split('\n')[0])


fdev=open('devid_africa.txt','r')
for line in fdev.readlines():
    devices.append(line.split('\n')[0])

#servers=['4.71.254.166']
#devices=['2CB05D830287']
print servers
print devices
rtts={}
rttstats={}

try:
	conn=pg.connect(dbname='bismark_openwrt_live_v0_1',user='****', passwd='****')
	print "Connection Successful"
	#print "Tables:"+conn.gettables()
	#cmd="select* from traceroutes where srcip='196.215.129.124'"
	for s in servers:
		print "Server: "+s
        	for dev in devices:
            		cmd="SELECT id,hops FROM traceroutes WHERE dstip='%s' AND toolid='paristraceroute' AND deviceid='%s'"%(s,dev)
			#cmd ="SELECT DISTINCT dstip FROM traceroutes WHERE deviceid='2CB05D8302AB' AND toolid='paristraceroute' AND srcip='41.177.18.103'"
			print cmd
			try:
				res=conn.query(cmd)
				temp=res.getresult()
				print len(temp)
				rtts[s,dev]=[]
				#print temp
				for (id,hps) in temp:
					cmd1="SELECT hop,rtt FROM traceroute_hops WHERE id='%s'"%(id)
					#print cmd1
					try:
						res1=conn.query(cmd1)
						result=res1.getresult()
						#print result
						(mhop,mrtt)=result[len(result)-1]
						#print mhop
						#print mrtt
						
						# to filter out results creating bias
						if mhop==hps:		
							rtts[s,dev].append(mrtt)
						else:
							print "mhop: "+str(mhop)+", hops: "+str(hps)
					except:
						print "error run 2"						 
					#break			
			except:
				#print res.sqlstate
				print "Couldn't run the query"
	
	
	conn.close()
	print "Connection Closed"
except:
	print "Connection Error"

ofile=open('rttstats.txt','w+')
for s in servers:
	ofile.write('Server: '+s+'\n')
	for dev in devices:
		ofile.write(''+dev+',')
		if (s,dev) in rtts:
			if len(rtts[s,dev])>=2:
				rttstats[s,dev] = [stats(rtts[s,dev])]
				print rttstats[s,dev]
				if len(rttstats[s,dev][0])>=3:
					ofile.write(''+str(rttstats[s,dev][0][1])+','+str(rttstats[s,dev][0][2])+','+str(rttstats[s,dev][0][3])+'\n')
				else:
					ofile.write('\n')
		else:
			ofile.write('\n')
	ofile.write('\n')



	#print rtts
print rttstats

