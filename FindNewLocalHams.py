#Donna Dietz N2SZ donna.dietz@gmail.com
#April 2019
#Jan 2019
#May 2018

print("Thank you for using my Python Script! Help me debug it! donna.dietz@gmail.com N2SZ")
print("Please wait a minute or two while the entire FCC database is being read.")


#http://wireless.fcc.gov/uls/index.htm?job=transaction&page=weekly
#grab both amateur zipped files
#wireless.fcc.gov/uls/data/complete/a_amat.zip
#wireless.fcc.gov/uls/data/complete/l_amat.zip
#close to 400 MB in total, takes awhile. unzip. Can delete much of it.
#from a_amat keep EN.dat 
#from l_amat keep AM.dat EN.dat and HD.dat
#keep in their separate folders where they unzipped from
#a_amat and l_amat are subfolders in same directory with this code

#FIELDS OF RELEVANCE
#All folders will be read line by line and split by | symbols first item #0
#a_amat/EN.dat  4:callsign 6: LicenceNumber, 7: Full name
# 8:firstname, 9: initial, 10:lastname, 11:suffix, 15: address, 16: city,
# 17: state, 18:zip, 22: FRN  (This seems to contain all old info, but filling up
# dictionary from top to bottom should be safe. It seems to be chronological.
#l_amat/EN.dat same fields as above, but fewer items reflected in this file
# Probably either EN file is fine
#l_amat/HD.dat  4:callsign, 5: 'A'=active etc, 6: HA/HV contains upgrade dates etc.
#l_amat/AM.dat 4:callsign, 5:class

#l_amat/CO.dat tells you dates when new sequ/vanity calls were assigned Keyed by callsign
#l_amat/HD.dat seems to give dates of renewal, upgrades etc. Not sure format...
#l_amat/HS.dat gives original license date and upgrade dates
#l_amat/LA.dat obits
#l_amat/AM.dat lets you pair current call with old call

#python3
import re

lic_class={}
fyle=open('l_amat/AM.dat','r')
for line in fyle:
    temp=line.split('|')
    lic_class[temp[4]]=temp[5]
fyle.close()


active={}
HAHV={}
fyle=open('l_amat/HD.dat','r')
for line in fyle:
    temp=line.split('|')
    active[temp[4]]=temp[5]
    HAHV[temp[4]]=temp[6]
fyle.close()


lastname={}
firstname={}
initial={}
suffix={}
stateLived={}
FRN={}
Lnum={}
address={}
city={}
zipcode={}

fyle=open('l_amat/EN.dat','r')
for line in fyle:
    temp=line.split('|')
    namefield=temp[8]
    namefield=re.sub(","," ",namefield)
    namefield=re.sub("\."," ",namefield)
    namefield=re.sub("'"," ",namefield)
    namefield=re.sub('"'," ",namefield)
    
    if(len(namefield)):
        if ' ' in namefield:
            breakout=namefield.split(' ') 
            myname=''                   
            for e in breakout:
                if len(e)>len(myname):
                    myname=e
            firstname[namefield]=myname.upper()        
        else:
            firstname[temp[4]]=namefield.upper()
    if(len(temp[6])):
        Lnum[temp[4]]=temp[6]
    if(len(temp[9])):
        initial[temp[4]]=temp[9]
    if(len(temp[10])):
        lastname[temp[4]]=temp[10]
    if(len(temp[11])):
        suffix[temp[4]]=temp[11]
    if(len(temp[15])):
        address[temp[4]]=temp[15]
    if(len(temp[16])):
        city[temp[4]]=temp[16]
    if(len(temp[17])):
        stateLived[temp[4]]=temp[17]
    if(len(temp[18])):
        zipcode[temp[4]]=temp[18][0:5]
    if(len(temp[15])==0) and len(temp[19]):
        address[temp[4]]="P.O. Box "+str(temp[19])
    if(len(temp[22])):
        FRN[temp[4]]=temp[22]
fyle.close()    


calls=list(FRN.keys()) 

for i in range(len(calls)):
    if calls[i] in address and address[calls[i]][0:6].upper()=="PO BOX":
        address[calls[i]]="P.O. Box"+address[calls[i]][6:]

#This stunt is specifically so people like "WX4TV" will be matched with
#his family who is "KM4TXT" etc. Some people write PO Box differently

#end of hamFCC2, start unzipzips.

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

#End unzipzips start newgrants

grant={}
fyle=open('l_amat/HS.dat','r')
for line in fyle:
    temp=line.split('|')
    if temp[5].strip()=="SYSGRT":
        grant[temp[3]]=temp[4]
fyle.close()

def listNew(m,d,yr):
    L=[]
    k=grant.keys()
    for e in k:
        d2=grant[e]
        Date=d2.split("/")
        (mi,di,yri)=(int(Date[0]), int(Date[1]), int(Date[2]))
        if yri>yr:
            L.append(e)
        elif yri==yr and mi>m:
            L.append(e)
        elif yri==yr and mi==m and di>=d:
            L.append(e)
    return L

#end newgrants start makeziplists


zipLists={}
fyle=open('a_amat/EN.dat','r')
d=[]
for l in fyle:
    d.append(l[:-1])
fyle.close()    

for e in d:
    temp=e.split('|')
    try:
       if not temp[6] in zipLists:
           try:
               zipLists[temp[6]]=[temp[18][0:5]]
           except:
               pass
       else:
           try:
               zipLists[temp[6]].append(temp[18][0:5])
           except:
               pass
    except:
               pass

#end MakeZipLists start newaddress

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

#end newaddress start Process_data


def notTooFar(lic,zip,dist):
       z1=zipcode[lic]
       return zipDist(z1,zip)<=dist


def findNewGrantsNearby(cyr,cm,cd,cmiles,czip,ourstate):
  print("We will look for brand new hams in our area!")
  #cyr=int(input("Give cutoff year: "))
  #cm=int(input("Give (numerically) cutoff month: "))
  #cd=int(input("Give cutoff date: "))
  #cmiles=float(input("Give max miles: "))
  if czip=='20770':
      print("Zipcode of 20770 is being used.")
  L=listNew(cm,cd,cyr) #date cutoff here
  print("We found nationally: "+str(len(L))+" new licencees in database.")
  L_close=[]
  #newNeighbors=input("Give first part of filename for latex file of addresses: ")
  newNeighbors = "NewLocalHams"
  f=open(newNeighbors+".tex","a")
  for e in L:
    try:     
      if stateLived[e]==ourstate and notTooFar(e,czip,cmiles): #zip=Greenbelt, distance in miles
             L_close.append(e)
    except:
      pass
  print("We found "+str(len(L_close))+" new licencees nearby!")
  print(L_close)
  closeBook=[]
  for e in L_close:
         f.write("\lb{ ")     
         record=""
         try:
            record=record+firstname[e]+" "+initial[e]+" "+lastname[e]+" "
            f.write(firstname[e]+" "+initial[e]+" "+lastname[e]+" "+e+" \\\\\n")
         except:
            try:
                record=record+firstname[e]+" "+lastname[e]+" "
                f.write(firstname[e]+" "+lastname[e]+" "+e+" \\\\\n")
            except:
              try:
                 record=record+initial[e]+" "+lastname[e]+" "
                 f.write(initial[e]+" "+lastname[e]+" "+e+" \\\\\n")
              except:
                 try:
                     record=record+lastname[e]+" "
                     f.write(lastname[e]+" "+e+" \\\\\n")
                 except:
                     record=record+" "+e+" "
                     f.write(e+" \\\\\n")
         record=record+" ["+e+"] "+lic_class[e]+" - "
         try:
            record=record+address[e].upper()+" "
            f.write(address[e]+" \\\\\n")        
         except:
            pass
         try:
            record=record+city[e].upper()+", "+stateLived[e]+" "+zipcode[e]
            f.write(city[e]+", "+stateLived[e]+" "+zipcode[e]+" }\n")        
         except:
            pass
         closeBook.append(record)
  closeBook.sort()
  f.close()
  newAndClose="NewLocalHams"
  #newAndClose=input("Give first part of filename for sorted text list: ")
  f=open(newAndClose+".txt","a")
  for e in closeBook:
      f.write(e)
      f.write("\n")
  f.close()
  print("Addresses labels not sorted by last name.. . ")

def findNewMoveInsNearby(cyr,cm,cd,cmiles,czip,ourstate):
  print("We shall search now for hams who have recently moved into the area!")
  #cyr=int(input("Give cutoff year: "))
  #cm=int(input("Give (numerically) cutoff month: "))
  #cd=int(input("Give cutoff date: "))
  #cmiles=float(input("Give max miles: "))
  #print("Default zipcode of 20770 is being used.")
  L=listNewAddress(cm,cd,cyr) #date cutoff here
  print("We found nationally: "+str(len(L))+" new addresses in database.")
  L_close=[]
  #newNeighbors=input("Give first part of filename for latex file of addresses: ")
  newNeighbors='NewLocalHams'
  f=open(newNeighbors+".tex","a")

  for e in L:
    try:     
      if stateLived[e]==ourstate and notTooFar(e,czip,cmiles): #zip=Greenbelt, distance in miles
             L_close.append(e)
    except:
      pass
  print("We found "+str(len(L_close))+" new neighbors who ended up in the area!")
  print(L_close)
  print("Now we will take out the in-town moves")
  L_close2=[]
  for e in L_close:
     if isActuallyNewArrival(e,cmiles,czip):
         L_close2.append(e)
  print("We found "+str(len(L_close2))+" hams who moved out of area to this area.")
  print(L_close2)
  closeBook=[]
  for e in L_close2:
         f.write("\lb{ ")     
         record=""
         try:
            record=record+firstname[e]+" "+initial[e]+" "+lastname[e]+" "
            f.write(firstname[e]+" "+initial[e]+" "+lastname[e]+" "+e+" \\\\\n")
         except:
            try:
                record=record+firstname[e]+" "+lastname[e]+" "
                f.write(firstname[e]+" "+lastname[e]+" "+e+" \\\\\n")
            except:
              try:
                 record=record+initial[e]+" "+lastname[e]+" "
                 f.write(initial[e]+" "+lastname[e]+" "+e+" \\\\\n")
              except:
                 try:
                     record=record+lastname[e]+" "
                     f.write(lastname[e]+" "+e+" \\\\\n")
                 except:
                     record=record+" "+e+" "
                     f.write(e+" \\\\\n")
         record=record+" ["+e+"] "+lic_class[e]+" - "
         try:
            record=record+address[e].upper()+" "
            f.write(address[e]+" \\\\\n")        
         except:
            pass
         try:
            record=record+city[e].upper()+", "+stateLived[e]+" "+zipcode[e]
            f.write(city[e]+", "+stateLived[e]+" "+zipcode[e]+" }\n")        
         except:
            pass
         closeBook.append(record)
  closeBook.sort()
  f.close()
  #newAndClose=input("Give first part of filename for sorted text list: ")
  newAndClose="NewLocalHams"
  f=open(newAndClose+".txt","a")
  f.write("-------------   new move-ins below ---------------\n")
  for e in closeBook:
      f.write(e)
      f.write("\n")
  f.close()
  #print("Addresses labels not sorted by last name.. . ")


def isActuallyNewArrival(call,dist,czip):
    z=zipLists[Lnum[call]]
    if len(z)>2:
      try:
        result = zipDist(z[-1],czip)<=dist and zipDist(z[-2],czip)>=dist
        return result
      except:
        return None
    return None


reply=input("Do you want to run lists? (Y/N): ")
if reply=="Y" or reply=="y":
    print("New files 'NewLocalHams.txt' and 'NewLocalHams.tex' will be written/overwritten (unless you abort this code now).")
    cyr=int(input("Give cutoff year: "))
    cm=int(input("Give (numerically) cutoff month: "))
    cd=int(input("Give cutoff date: "))
    cmiles=float(input("Give max miles: "))
    print("Enter zipcode below or hit enter to default to 20770")
    czip=input("Give zipcode for center: ")
    if czip=="":
        print("Default zipcode of 20770 is being used.")
        czip="20770"
    print("Enter state 2-digit code  below or hit enter to default to 'MD' ")
    ourstate=input("Give state: ")
    if ourstate=="":
        print("Default state of 'MD' is being used.")
        ourstate="MD"
    f=open("NewLocalHams.txt","w")
    f.write("New Local Hams: "+str(cmiles)+" miles away from "+czip+" "+ourstate+"\n")
    f.write("Start date: "+str(cm)+"/"+str(cd)+"/"+str(cyr)+"\n")
    f.close();
    f=open("NewLocalHams.tex","w")
    f.close();
        
    findNewGrantsNearby(cyr,cm,cd,cmiles,czip,ourstate)
    findNewMoveInsNearby(cyr,cm,cd,cmiles,czip,ourstate)



