import pg
import os, sys
#devids=['2CB05D830287']
devids=[]
mlab_nairobi='196.24.45.146'

logfile=open('jburg_traceroute_data_146.txt','w+')
ids={}
nhops={}
prev_route=[]

def read_devid():
	pfile = open('devid_africa.txt','r')
	for line in pfile.readlines():
		devids.append(line.split('\n')[0])
	print devids

def unique_ids(dev,i,arr):
	nhops[dev,i]=[]
	for val in arr:
		if val[1] not in nhops[dev,i]:
			print "need to add "+str(val[1])
			nhops[dev,i].append(val[1])
			ids[dev,i,val[1]] = val[0]
	print ids

def capture_ids(i=0):
    for dev in devids:
        try:
		conn=pg.connect(dbname='bismark_openwrt_live_v0_1',user='****', passwd='****')
		print "Connection Successful"
		if i==0:
                	cmd="SELECT id,hops FROM traceroutes WHERE srcip='%s' AND deviceid='%s'"%(mlab_nairobi,dev)
			logfile.write('\nDevice id:'+str(dev)+', direction: from Mlab_Nairobi'+'\n')
		else:
			cmd="SELECT id,hops FROM traceroutes WHERE dstip='%s' AND deviceid='%s'"%(mlab_nairobi,dev)
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
			        logfile.write('\nhops: '+str(hop)+'\n')
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
	capture_ids(0)
	capture_ids(1)

if __name__ == "__main__":
	main()


