import os,sys
pr=[]

class test(object):
    def __init__(self,a=0,b=0):
        self.a=a
        self.b=b

def main():
    t1=test(1,2)
    pr.append(t1)
    t1=test(3,4)
    pr.append(t1)
    print pr[1].a
if __name__=="__main__":
        main()
