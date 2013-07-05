import pg
import os, sys

ip_list=[]
mac_list=[]
mlab_server=[]
qresult={}
# get list of Mlab Servers

def read_mlabFile():
	mfile=open('mlab_server.txt','r')
	for line in mfile.readlines():
		mlab_server.append(line.split('\n')[0])


# get name of the Router's ip addresses. 
def read_prefixFile():
	pfile = open('plist_africa.txt','r')
	for line in pfile.readlines():
	        ip_list.append(line.split('\n')[0].split(' ')[0])
        	#mac_list.append(line.split('\n')[0].split(' ')[1])


# write the results to a file
def result_to_file():
	fname='analysis_traceroute.txt'
	logfile=open(fname,'w+')
	logfile.write('Analysis of Mlab Server Routes\n\n\n\n')
	for server in mlab_server:
		logfile.write('Server: '+server+'\n\n')
		for ip in ip_list:
			logfile.write('Router: '+ip+', ')
			if qresult[(server, ip)]==[]:
				logfile.write('Path: []\n\n')
				continue
			logfile.write('Path: '+ip+'->')
			for val in qresult[(server, ip)]:
				logfile.write(val+'->')
			logfile.write(server+'\n\n')
		logfile.write('\n\n\n')
		

def main():
	# Read the plist file
	read_prefixFile()
	# Read the Mlab Server File
	read_mlabFile()
	print ip_list
	print mlab_server
	for server in mlab_server:
		dstip=server
		for ip in ip_list:
			srcip=ip
			qresult[(server,ip)]=[]
			try:
				conn=pg.connect(dbname='bismark_openwrt_live_v0_1',user='glex', passwd='arp787')
				print "Connection Successful"
				#print "Tables:"+conn.gettables()
				#cmd="select * from traceroutes where srcip='196.215.129.124'"
				cmd = "SELECT id FROM traceroutes WHERE srcip='%s' AND dstip='%s'"%(srcip,dstip)
				#print cmd
				try:
					res=conn.query(cmd)
					result=res.getresult()
					id = result[0][0]
					cmd="select ip FROM traceroute_hops where id='%s'"%(id)
					try:
						res=conn.query(cmd)
						result=res.getresult()
						#print result
						for val in result:
							#print val
							qresult[(server,ip)].append(val[0])
					except:
						print "Unable to process second query"
					#print result[0][0]
				except:
					#print res.sqlstate
					print "Couldn't run the query"
		
				conn.close()
				print "Connection Closed"
			except:
				print "Connection Error"
	print qresult
	result_to_file()

if __name__ == "__main__":
	main()
