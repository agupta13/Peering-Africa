# Arpit Gupta (arpitg@cs.princeton.edu)

import json

def parse_updates(fname):
    updates = []
    with open(fname,'r') as f:
        flag = 0
        tmp = {}
        for line in f.readlines():
            if line.startswith("TIME"):
                flag = 1
                tmp = {}
                tmp["time"] = line.split(" ")[2].split("\n")[0]
            elif flag == 1:
                x = line.split("\n")[0].split(": ")
                if len(x) >= 2:
                    tmp[x[0]] = x[1]
                if "ANNOUNCE" in x:
                    flag = 2
            elif flag == 2:

                if line.startswith("\n"):
                    flag = 0
                    updates.append(tmp)
                else:
                    x = line.split("\n")[0].split()[0]
                    print x
                    if "prefixes" not in tmp:
                        tmp["prefixes"] = []
                    tmp["prefixes"] = x
    return updates


if __name__ == "__main__":
    fname = "updates.20150511.2245.txt"
    updates = parse_updates(fname)
    with open("bgp_updates.json",'w') as fp:
        json.dump(updates,fp)
