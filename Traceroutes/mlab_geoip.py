import os,sys
import pygeoip

gi4 = pygeoip.GeoIP('/home/arpit/Bismark_bgp/geoip/pygeoip/GeoIP.dat', pygeoip.MEMORY_CACHE)
giasn = pygeoip.GeoIP('/home/arpit/Bismark_bgp/geoip/pygeoip/GeoIPASNum.dat', pygeoip.MEMORY_CACHE)

gicity= pygeoip.GeoIP('/home/arpit/Bismark_bgp/geoip/pygeoip/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

#print gi4.country_name_by_addr('155.232.13.129')




def main():
	fname='analysis_traceroute.txt'
	logfile=open(fname,'r')	
	fout='geo_traceroute.txt'
	outfile=open(fout,'w+')
	for line in logfile.readlines():
		if line.startswith('Router'):
			print line
			outfile.write(line.split('Path: ')[0]+'\nPath: \n')
			temp = line.split('Path: ')[1].split('\n')[0]
			ips=temp.split('->')
			print len(temp)
			print temp
			if len(temp)==2:
				print "no path"
				outfile.write('[]\n')
				continue
			ind=0
			key='city'
			for ip in ips:
				c = gi4.country_name_by_addr(ip)
				asn = giasn.org_by_addr(ip)
				record= gicity.record_by_addr(ip)
				print record 
				if asn==None:
					asn=''
				print asn
				ind+=1
				#print ip
				#print c
				outfile.write('('+ip+','+asn+','+c+')\n')
				if ind==len(ips)-2:
					#outfile.write('\n\n')					
					break
			ip = ips[len(ips)-1]
			c = gi4.country_name_by_addr(ip)
			asn = giasn.org_by_addr(ip)
			outfile.write('('+ip+','+asn+','+c+')\n')
			
		elif line.startswith('Server'):
			print line			
			ip = line.split('Server: ')[1].split('\n')[0]
			c = gi4.country_name_by_addr(ip)
			asn = giasn.org_by_addr(ip)
			outfile.write('Server: '+ip+' Location: '+c)
					
		
		else:
			outfile.write(line)


if __name__ == "__main__":
	main()

