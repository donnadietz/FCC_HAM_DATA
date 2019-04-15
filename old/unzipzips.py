f=open("zips.csv","r")
d=[]
for l in f:
    d.append(l[:-1])
f.close()

d.pop(-1)
d.pop(-1)

z={}
for e in d:
    t=e.split(",")
    try:
        z[t[0].strip()]=( float(t[2].strip()) , float(t[3].strip()) )
    except:
        pass





###http://zips.sourceforge.net/
###also google maps scraping with urllib
from math import *

def calcDist(lat_A, long_A, lat_B, long_B):
  distance = (sin(radians(lat_A)) *
              sin(radians(lat_B)) +
              cos(radians(lat_A)) *
              cos(radians(lat_B)) *
              cos(radians(long_A - long_B)))
  distance = (degrees(acos(distance))) * 69.09
  return distance    


def zipDist(A,B):
    try:
        return calcDist(z[A][0],z[A][1],z[B][0],z[B][1]) #miles
    except:
        pass
    (p,q)=findLL(A)
    (r,s)=findLL(B)
    return calcDist(p,q,r,s)

def findLL(zip):
    if zip in z:
        return (z[zip])
    for i in range(1,5000):
        for j in [-1,1]:
            fakezip = str(int(zip)+i*j)
            if len(fakezip)==4:
                fakezip='0'+fakezip
            if fakezip in z:
                print("Using zip: "+fakezip+" instead of "+zip)
                return(z[fakezip])
    print("Giving up and using origin for zip")        
    return(("0","0"))






