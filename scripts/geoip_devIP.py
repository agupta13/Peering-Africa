# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,sys
import pygeoip

gi4 = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIP.dat', pygeoip.MEMORY_CACHE)
giasn = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIPASNum.dat', pygeoip.MEMORY_CACHE)

gicity= pygeoip.GeoIP('/data/arpit/pygeoip/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

#print gi4.country_name_by_addr('155.232.13.129')


c=''
asn=''
unique_as={}

def main():
	fname='did_to_IP.txt'
	logfile=open(fname,'r')
	fout='did_to_IP-AS.txt'
	outfile=open(fout,'w+')
        did=''
	for line in logfile.readlines():
		if line.startswith('deviceid') or line.startswith('\n'):
			outfile.write(line)
                	if line.startswith('deviceid'):
                        	did=line.split(':')[1].split('\n')[0]
                		unique_as[did]=[]
		else:
			#print line
			if True:
				ip = line.split('\n')[0]
				#print ip
				#rtt=line.split('\n')[0].split(',')[2]
				#print rtt
				#hop=line.split('\n')[0].split(',')[0]
				c = gi4.country_name_by_addr(ip)
				if c==None:
					c=''
				asn = giasn.org_by_addr(ip)
				#print asn
                		if asn not in unique_as[did] and asn != None:
                    			unique_as[did].append(str(asn))
					print asn
					print unique_as[did]
					#unique_as[did].append(asn)

                		if asn==None:
					asn=''
				#print asn
				outfile.write(''+ip+','+asn+','+c+'\n')
    	print unique_as
	fmap=open('did_ASMap.txt','w+')
	for dev in unique_as.keys():
		fmap.write(''+dev+': ')
		for asn in unique_as[dev]:
		
			fmap.write(''+asn+', ')
		fmap.write('\n')
if __name__ == "__main__":
	main()

