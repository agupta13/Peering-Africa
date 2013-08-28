# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,sys
import pygeoip

gi4 = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIP.dat', pygeoip.MEMORY_CACHE)
giasn = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIPASNum.dat', pygeoip.MEMORY_CACHE)

gicity= pygeoip.GeoIP('/data/arpit/pygeoip/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

fopen=open('servers_paristraceroutes.txt','r')
ofile=open('servers_details','w+')
for line in fopen.readlines():
    ip=line.split('\n')[0]
    c = gi4.country_name_by_addr(ip)

    if c==None:
        c=''
    asn = giasn.org_by_addr(ip)
    city = gicity.record_by_addr(ip)['city']
    #print city
    ofile.write(''+ip+','+city+','+c+','+asn+'\n')
    print "ip: "+ip+", city: country: "+c+" asn: "+asn

ofile.close()
fopen.close()

