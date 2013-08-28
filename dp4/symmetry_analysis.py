import pg
import os, sys
#devids=['2CB05D830287']
devids=[]
mlab_nairobi='196.24.45.146'
mlab_tunisia='41.231.21.44'
mlab_nairobi=mlab_tunisia

#logfile=open('jburg_symmetry_data146.txt','w+')
logfile=open('tunisia_symmetry_data.txt','w+')
ids={}
nhops={}
prev_route=[]

def read_devid():
	pfile = open('devid_africa.txt','r')
	for line in pfile.readlines():
		devids.append(line.split('\n')[0])
	print devids



def capture_ids():
    for dev in devids:
        try:
		conn=pg.connect(dbname='bismark_openwrt_live_v0_1',user='****', passwd='****')
		print "Connection Successful"
		#cmd="SELECT id,hops FROM traceroutes WHERE dstip='%s' AND deviceid='%s'"%(mlab_nairobi,dev)
		cmd = "SELECT id,hops,srcip,dstip FROM traceroutes WHERE deviceid ='%s' AND (dstip='%s' OR srcip='%s') ORDER BY eventstamp"%(dev,mlab_nairobi,mlab_nairobi)
		logfile.write('\nDevice id:'+str(dev)+', direction: to Mlab_Nairobi'+'\n')
		print cmd
		try:
			res=conn.query(cmd)
			print "query run success"
			result=res.getresult()
                	#print "No. of entries: "+len(result)
			for val in result:
				id = val[0]
				hop = val[1]
				if val[2]==str(mlab_nairobi):
					flag=0
				elif val[3]==str(mlab_nairobi):
					flag=1
				else:
					flag=2
			        logfile.write('\nhops: '+str(hop)+' direction: '+str(flag)+'\n')
                                #print   
				cmd="SELECT hop,ip,rtt FROM traceroute_hops WHERE id='%s'"%(id)
                                #print cmd
                                try:
                                	res=conn.query(cmd)
                                        result=res.getresult()
                                        #print "results retrieved:"+str(len(result))
                                        for val in result:
                                        	#print val
                                                logfile.write(str(val[0])+','+(val[1])+','+str(val[2])+'\n')
                                except:
                                	print "Error: running second query"
 	
            	except:
			print 'Error: query'
			conn.close()
			print "Connection Closed"
	except:
		print 'Errorr: DB conn'
def main():
	read_devid()
	capture_ids()

if __name__ == "__main__":
	main()


