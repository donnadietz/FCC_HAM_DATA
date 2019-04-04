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
    temp=[]
    for e in z:
        v=2000
        try:
            v=abs(int(e)-int(zip))
        except:
            pass
        if v<=1000:
            temp.append((abs(int(e)-int(zip)), e))
        temp.sort()
    if len(temp)==0:
            print("Failed to find "+zip+" or anything nearby.")
            return(("0","0"))
    print("Failed to find "+zip+" using instead: "+temp[0][1])
    return (z[temp[0][1]])





