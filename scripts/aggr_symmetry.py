import os, sys
import symmetry_analysis
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from scipy.stats import cumfreq
#import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import statsmodels.api as sm

locations=['tunisia', 'jburg','nairobi']
results={}

"""
for loc in locations:
    fname=loc+'_symmetry_processed.txt'
    #cmd='python symmetry_analysis.py '+fname
    results[loc]=symmetry_analysis.main(fname,loc)
"""
results={'tunisia': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4329004329004329, 0.8013737836290784, 23.76502002670227], 'jburg': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0380517503805175, 0.042034468263976464, 0.20807324178110695, 0.3472222222222222, 0.5082592121982211, 23.88730093915884, 26.786516853932586, 31.48469093009821, 59.14985590778098, 60.27906976744186], 'nairobi': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.07776049766718507,
    0.08904719501335707, 0.20418580908626852, 1.2949640287769784, 2.3856858846918487, 24.17091836734694, 50.351617440225034, 79.76494634644864]}

print results
print "Plot the CDF now"

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(1,1,1)

#color_n=[[.1,.5,.5],[.4,.3,.5],[.4,.5,.4],[.4,.4,.5],[.4,.3,.3],[.1,.2,.7]]
color_n=['g','m','c']
i=0
p1=[]
for loc in locations:
    a=results[loc]
    num_bins=10000
    counts, bin_edges = np.histogram(a,bins=num_bins,normed=True)
    cdf=np.cumsum(counts)

    #sample = np.random.uniform(0, 1, 50)
    ecdf = sm.distributions.ECDF(a)

    x = np.linspace(min(a), max(a))
    y = ecdf(x)
    scale = 1.0/cdf[-1]
    cdf=cdf*scale
    p1.append([])
    #p1[i]=pl.plot(X,CY,label=loc,color=color_n[i], linewidth=5.0)
    p1[i]=pl.plot(bin_edges[1:],cdf,label=loc,color=color_n[i], linewidth=5.0)
    #p1[i]=plt.step(x, y)
    i+=1
p=[]
i=0
for loc in locations:
    p.append(p1[i][0])
    i+=1
pl.ylim(0.00,1.00)
pl.xlim(-1,80)
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(24)
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(24)

pl.legend((p),locations,'lower right',prop={'size':32})

pl.xlabel('Routing Symmetry (%)',fontsize=32)
pl.ylabel('# Paths ',fontsize=32)
#pl.title('Presence of Symmetry (CDF)',fontsize=32)

ax.grid(True)

plot_name='ip_symmetry.eps'
plot_name='ip_symmetry.png'
pl.savefig(plot_name)
os.system('scp ip_symmetry* arpit@newton.noise.gatech.edu:~/Bismark_bgp/Traceroutes/prevalence/results/')

