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
        if dev not in devices:
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

#print serverinfo
dlat={}
dname={}
mdist=0.0
dist=[]
citiesd={}
for srv in serverinfo.keys():
    for dev in devices.keys():
        if (srv,dev) in mlatency:
            latency=mlatency[srv,device]
            (city,distance)=serverinfo[srv]
            if distance not in dist:
                citiesd[distance]=city
                dist.append(distance)
            dlat[(distance,dev)]=latency
            dname[(distance,dev)]=city
            if distance>=mdist:
                mdist=distance

#print dlat
#print dname




dist.sort()
#print dist
latency=[]
cities=[]
latency_ideal=[]
inflation=[]
i=0
for dev in devices:
    latency.append([])
    latency_ideal.append([])
    inflation.append([])
    for d in dist:
        if citiesd[d] not in cities:
            cities.append(citiesd[d])
        if (d,dev) in dlat:

            #print dlat[d,dev]
            latency[i].append(dlat[(d,dev)])
            #cities.append(dname[(d,dev)])
            temp=1000*float(d)/speedOfLight
            temp2=float(dlat[d,dev])/temp
            latency_ideal[i].append(temp)
            inflation[i].append(temp2)
        else:
            latency[i].append(1.00)
            inflation[i].append(1.00)
    i+=1

inflation2d=inflation
#inflation2d.append(inflation)
#inflation2d.append(inflation)

inflation2d= np.array(inflation2d)
fig, ax = plt.subplots()
heatmap = ax.pcolor(inflation2d, cmap=plt.cm.jet, alpha=0.8)
#plt.set_cmap('spectral')
fig = plt.gcf()
fig.set_size_inches(8,12)

ax.set_frame_on(False)
ax.set_yticks(np.arange(inflation2d.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(inflation2d.shape[1])+0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xticklabels(cities, minor=False)
ax.set_yticklabels(devices.keys(), minor=False)

plt.xticks(rotation=90)

ax.grid(False)
#ax = plt.gca()

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False

cbar = plt.colorbar(heatmap, ticks=[-1,0,1], orientation='horizontal')
print cbar.ax.get_xticklabels()
cbar.ax.set_xticklabels(['Low','Medium','High'])      # horizontal colorbar

print cbar.ax.get_position()
cbar.update_ticks()
plot_name='heatmap.eps'
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
#os.system('scp latency_distance.eps latency_distance.eps arpit@newton.noise.gatech.edu:~/Bismark_bgp/Traceroutes/prevalence/results/')
