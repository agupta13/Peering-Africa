import os, sys

#locations=['tunisia', 'jburg','nairobi']
locations=['nairobi']
ixpinfo={'DE-CIX': '80.81.199.0/24', 'LINX': '195.66.224.0/19', 'AS1200 Amsterdam Internet Exchange B.V.': '195.69.144.0/22', 'KIXP': '196.223.21.32/27', 'CINX': '196.223.22.0/24', 'JINX': '196.223.14.0/24'}


for loc in locations:
    print "Processing the location: "+loc
    fname='../'+loc+'/prevalence_analysis.py'
    cmd = 'python '+fname+' '+loc
    os.system('cp prevalence_analysis.py ../'+loc+'/')
    os.system('cp statistics.py ../'+loc+'/')
    os.chdir('../'+loc)
    os.system(cmd)
    os.chdir('../scripts')

print "## Send the files to master's server"
os.system('scp *.eps *png arpit@newton.noise.gatech.edu:~/Bismark_bgp/Traceroutes/prevalence/results/')



