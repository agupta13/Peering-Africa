# Author: Arpit Gupta (glex.qsd@gmail.com)
import os,sys
import pygeoip

gi4 = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIP.dat', pygeoip.MEMORY_CACHE)
giasn = pygeoip.GeoIP('/data/arpit/pygeoip/GeoIPASNum.dat', pygeoip.MEMORY_CACHE)

gicity= pygeoip.GeoIP('/data/arpit/pygeoip/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
countries=['za','ke']
cntry_as={}


def main():

    for cntry in countries:
        cntry_as[cntry]={}
        cname=cntry+'.csv'
        oname=cntry+'_aslist.txt'
        fopen=open(cname,'r')
        ofile=open(oname,'w+')
        for line in fopen.readlines():
            if len(line.split(','))>=2:
                ip=line.split(',')[0]
                #print ip
                c = gi4.country_name_by_addr(ip)
                #print ip
                if c==None:
                    c=''
                asn = giasn.org_by_addr(ip)
                city = gicity.record_by_addr(ip)['city']
                #print city
                if city==None:
                    city=''
                if asn==None:
                    asn=''
                else:
                    asnum=int(asn.split(' ')[0].split('AS')[1])
                    asname=str(asn.split(' ')[1])
                if (cntry,asnum) not in cntry_as:
                    cntry_as[cntry][asnum]=asname

                ofile.write(''+ip+','+city+','+c+','+asn+'\n')
                #print "ip: "+ip+", city: country: "+c+" asn: "+asn

        ofile.close()
        fopen.close()

    #print cntry_as
    #print len(cntry_as['za'].keys())
    #print len(cntry_as['ke'].keys())
    return cntry_as

if __name__ == "__main__":
    main()

