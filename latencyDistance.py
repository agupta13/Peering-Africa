#Author: Arpit Gupta

import os,sys
#import IXP_auxInfo as auxinfo
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#from netaddr import *
from scipy.stats import cumfreq
#import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import statsmodels.api as sm

fserver=open('servers_details.txt','r')
frtt=open('rttstats.txt','r')
speedOfLight=300000 # km/s
mlatency={}
serverinfo={}

from matplotlib.ticker import MaxNLocator
my_locator = MaxNLocator(6)

from matplotlib import rc
rc('/data/arpit/matplotlib_config.rc')


#device='2CB05D830287'
device = '2CB05D830293'
srv=''
devices={}

for line in frtt.readlines():
    temp=line.split('\n')[0]
    if line.startswith('Server'):
        srv=temp.split('Server: ')[1]
    if len(temp.split(','))==4:
        dev=temp.split(',')[0]
        if dev not in devices and dev !='2CB05D873B72':
            devices[dev]=1
        mlatency[srv,dev]=float(temp.split(',')[2])

#print mlatency

for line in fserver.readlines():
    temp=line.split('\n')[0].split(',')
    if len(temp)==5:
        srv=temp[0]
        city=temp[1]
        distance=float(temp[4].split(' km')[0])
        serverinfo[srv]=(city,distance)

print mlatency
#print serverinfo
dlat={}
dname={}
mdist=0.0
dist=[]
citiesd={}
for srv in serverinfo.keys():
    for dev in devices.keys():
        if (srv,dev) in mlatency:
            latency=mlatency[srv,dev]
            (city,distance)=serverinfo[srv]
            if distance not in dist:
                citiesd[distance]=city
                dist.append(distance)
            dlat[(distance,dev)]=latency
            dname[(distance,dev)]=city
            if distance>=mdist:
                mdist=distance


print dlat
#print dname




dist.sort()
#print dist
latency=[]
cities=[]
latency_ideal=[]
inflation=[]
i=0
for dev in devices:
    print dev
    latency.append([])
    latency_ideal.append([])
    inflation.append([])
    for d in dist:
        if citiesd[d] not in cities:
            cities.append(citiesd[d])
        if (d,dev) in dlat:

            print dlat[d,dev]
            latency[i].append(dlat[(d,dev)])
            #cities.append(dname[(d,dev)])

            temp=1000*float(d)/speedOfLight
            print temp
            temp2=float(dlat[d,dev])/temp
            print temp2
            latency_ideal[i].append(temp)
            inflation[i].append(temp2)
        else:
            latency[i].append(1.00)
            inflation[i].append(1.00)
    print inflation[i]
    i+=1

#print inflation
inflation2d=inflation
#inflation2d.append(inflation)
#inflation2d.append(inflation)
#print inflation2d
inflation2d= np.array(inflation2d)
inflation2d=(inflation2d-0)/(inflation2d.max()-0)
#print inflation2d
fig=plt.figure(figsize=(8,10))
ax= fig.add_subplot(1,1,1)
heatmap = ax.pcolor(inflation2d, edgecolors='k', cmap=plt.cm.jet, alpha=0.8)
#plt.set_cmap('spectral')
fig = plt.gcf()
#fig.set_size_inches(7.3,4.2)
plt.xlim(0,9)
#ax.set_frame_on(False)
#ax.set_yticks(np.arange(inflation2d.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(inflation2d.shape[1])+1.0, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
#xlab=['Cape Town, SA','KE','TUN','IT','BR','UK,'AUS','JP','US','US','US']
ax.set_xticklabels(cities, minor=False,fontsize=16)
#ax.set_yticklabels(range(1,len(devices.keys())+1), minor=False)
plt.gca().yaxis.set_major_locator(plt.NullLocator())

plt.xticks(rotation=45)
pl.ylabel('Bismark Routers',fontsize=20)
pl.xlabel('M-Lab Server Host Cities',fontsize=20)

ax.grid(False)
ax = plt.gca()
#citymap={'Cape Town': 'Cape Twn, SA', '':0''}

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
"""
cbar = plt.colorbar(heatmap, ticks=[-1,0],orientation='horizontal')
#print cbar.ax.get_xticklabels()
#cbar.gca().xaxis.set_major_locator(plt.NullLocator())
#cbar.ax.set_xticklabels(['Low','Medium','High'])      # horizontal colorbar

print cbar.ax.get_position()
cbar.update_ticks()
"""
plot_name='heatmap.eps'
pl.savefig(plot_name)


inflation2d = np.array(latency)
fig=plt.figure(figsize=(8,10))
ax= fig.add_subplot(1,1,1)
heatmap = ax.pcolor(inflation2d, edgecolors='k', cmap=plt.cm.jet, alpha=0.8)
#plt.set_cmap('spectral')
fig = plt.gcf()
#fig.set_size_inches(7.3,4.2)
plt.xlim(0,9)
#ax.set_frame_on(False)
#ax.set_yticks(np.arange(inflation2d.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(inflation2d.shape[1])+1.0, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
#xlab=['Cape Town, SA','KE','TUN','IT','BR','UK,'AUS','JP','US','US','US']
ax.set_xticklabels(cities, minor=False,fontsize=16)
#ax.set_yticklabels(range(1,len(devices.keys())+1), minor=False)
plt.gca().yaxis.set_major_locator(plt.NullLocator())

plt.xticks(rotation=45)
pl.ylabel('Bismark Routers',fontsize=20)
pl.xlabel('M-Lab Server Host Cities',fontsize=20)

ax.grid(False)
ax = plt.gca()
#citymap={'Cape Town': 'Cape Twn, SA', '':0''}

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
"""
cbar = plt.colorbar(heatmap, ticks=[-1,0],orientation='horizontal')
#print cbar.ax.get_xticklabels()
#cbar.gca().xaxis.set_major_locator(plt.NullLocator())
#cbar.ax.set_xticklabels(['Low','Medium','High'])      # horizontal colorbar

print cbar.ax.get_position()
cbar.update_ticks()
"""
plot_name='heatmap_abs.eps'
pl.savefig(plot_name)


"""

print inflation
print latency
print latency_ideal
print cities
"""
"""
#fig=plt.figure((figsize=(20,10)))
fig=plt.figure(figsize=(15,15))
ax = fig.add_subplot(1,1,1)
color_n=['g','m','c','r','b','k','w']
p1=pl.plot(latency,'rx',markersize=10.0)
p2=pl.plot(latency_ideal,'--k',linewidth=5.0)
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(24)
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(24)
#pl.xticks(cities)
pl.xlim(-0.1,11.1)
pl.ylim(0.1,600)
ax.grid(True)
#pl.xlabel('Cities',fontsize=32)
pl.ylabel('Latency (ms) ',fontsize=32)

pl.xticks(range(len(cities)), cities, fontsize=16)
locs, labels = pl.xticks()
plt.setp(labels, rotation=90)

plot_name='latency_distance.eps'
plot_name_png='latency_distance.png'
pl.savefig(plot_name)
pl.savefig(plot_name_png)

"""
os.system('scp heatmap* arpit@newton.noise.gatech.edu:~/Writings/glex/PAM14/results/')
