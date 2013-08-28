import pg
import os, sys
servers=[]
"""nfile=open('nairobi_servers.txt','r')
for line in nfile.readlines():
	servers.append(line.split('\n')[0])
"""
devids=[]
fdid = open('devid_africa.txt','r')
fout = open('did_to_IP.txt','w+')
for line in fdid.readlines():
	devids.append(line.split('\n')[0])


devIP={}
#servers=['197.136.0.108']
src=[]

try:
	conn=pg.connect(dbname='bismark_openwrt_live_v0_1',user='****', passwd='****')
	print "Connection Successful"
	
	for did in devids:
		fout.write('\ndeviceid: '+did+'\n')
		cmd="SELECT DISTINCT srcip FROM traceroutes WHERE deviceid='%s' AND dstip='197.136.0.108'"%(did)
		print cmd
		try:
			res=conn.query(cmd)
			result=res.getresult()
			#print result
			for ip in result:
				print ip[0]
				fout.write(ip[0]+'\n')
			
			devIP[did]=result
			#src.append(result)
		except:
			#print res.sqlstate
			print "Couldn't run the query"
		
	conn.close()
	print "Connection Closed"
except:
	print "Connection Error"

#print devIP
"""print src[0][0]
fl=open('src_nairobi','w+')
for s in src[0]:
	ip = str(s)
	ip = ip.split('(\'')[1].split(',')[0].split('\'')[0]
	fl.write(ip+'\n')
	print "Searcing for ip :"+ip
	if ip in open('/home/****/Bismark_bgp/plist_africa.txt').read():
		print "match found for ip:"

"""
