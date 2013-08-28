import pg
import os, sys
servers=[]
"""nfile=open('nairobi_servers.txt','r')
for line in nfile.readlines():
	servers.append(line.split('\n')[0])
"""
# M-lab tunisia 41.231.21.9
for i in range(1,255):
	s='41.231.21.'+str(i)
	servers.append(s)

#servers=['197.136.0.108']
src=[]
try:
	conn=pg.connect(dbname='bismark_openwrt_live_v0_1',user='****', passwd='****')
	print "Connection Successful"
	#print "Tables:"+conn.gettables()
	#cmd="select* from traceroutes where srcip='196.215.129.124'"
	for s in servers:
		cmd="SELECT srcip FROM traceroutes WHERE dstip='%s'"%(s)
		print cmd
		try:
			res=conn.query(cmd)
			result=res.getresult()
			print result
			#src.append(result)
		except:
			#print res.sqlstate
			print "Couldn't run the query"
		
	conn.close()
	print "Connection Closed"
except:
	print "Connection Error"

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
