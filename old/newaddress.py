newAddress={}
fyle=open('l_amat/HS.dat','r')
for line in fyle:
    temp=line.split('|')
    if temp[5].strip()=="LIAUA":
        newAddress[temp[3]]=temp[4]
fyle.close()

def listNewAddress(m,d,yr):
    L=[]
    k=newAddress.keys()
    for e in k:
        d2=newAddress[e]
        Date=d2.split("/")
        (mi,di,yri)=(int(Date[0]), int(Date[1]), int(Date[2]))
        if yri>yr:
            L.append(e)
        elif yri==yr and mi>m:
            L.append(e)
        elif yri==yr and mi==m and di>=d:
            L.append(e)
    return L         
