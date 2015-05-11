import os
import sys
import logging as log

dlog = "/Users/arpit/Bismark_bgp/logs/ribs/"

def main ():
    print "Started the parsing module"
    lfile = dlog+'rib.20130301.0000.bz2'
    ofile = 'rib.20130301.0000.txt'
    #os.system('cd /Users/arpit/Bismark_bgp/a1-bgp/libbgpdump-1.4.99.11')
    os.system('/Users/arpit/Bismark_bgp/a1-bgp/libbgpdump-1.4.99.11/./bgpdump '+lfile+' >'+ofile)
    #os.system('open '+'parse_dump.py')
    print "Completed the parsing task"

if __name__ == "__main__":
    main()

    