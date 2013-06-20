# Author: Arpit Gupta (glex.qsd@gmail.com)


class bgpData():
    def __init__(self,prefix='',nbr_as='',nbr_ip='',aspath=[],devid=''):
        self.prefix=prefix
        self.nbr_as=nbr_as
        self.nbr_ip=nbr_ip
        self.aspath=aspath
        self.devid=devid
        #print "Initialized bgpData object"