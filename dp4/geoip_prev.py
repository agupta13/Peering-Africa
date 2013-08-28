# Author: Arpit Gupta (****.qsd@gmail.com)
import os,sys
import pygeoip

gi4 = pygeoip.GeoIP('/home/arpit/Bismark_bgp/geoip/pygeoip/GeoIP.dat', pygeoip.MEMORY_CACHE)
giasn = pygeoip.GeoIP('/home/arpit/Bismark_bgp/geoip/pygeoip/GeoIPASNum.dat', pygeoip.MEMORY_CACHE)

gicity= pygeoip.GeoIP('/home/arpit/Bismark_bgp/geoip/pygeoip/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

#print gi4.country_name_by_addr('155.232.13.129')


c=''
asn=''

def main():
	fname='jburg_traceroute_data_146.txt'
	logfile=open(fname,'r')	
	fout='jburg_traceroute_processed146.txt'
	outfile=open(fout,'w+')
	for line in logfile.readlines():
		if line.startswith('Device') or line.startswith('\n') or line.startswith('hops'):
			outfile.write(line)
		else:
			#print line
			if len(line.split('\n')[0].split(','))==3:
				ip = line.split(',')[1]
				#print ip
				rtt=line.split('\n')[0].split(',')[2]
				#print rtt
				hop=line.split('\n')[0].split(',')[0]
				c = gi4.country_name_by_addr(ip)
				if c==None:
					c=''
				asn = giasn.org_by_addr(ip)	
				if asn==None:
					asn=''
				#print asn	
				outfile.write(''+hop+','+ip+','+rtt+','+c+','+asn+'\n')


if __name__ == "__main__":
	main()

