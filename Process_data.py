#1/1/2019
print("reading hamFCC2.py")
from  hamFCC2 import *
print("reading zipcodes")
from unzipzips import *
print("reading new licence grantees")
from newgrants import *
print("creating zipcode history list")
from MakeZipLists import *
print("figuring out who moved")
from newaddress import *


def notTooFar(lic,zip,dist):
       z1=zipcode[lic]
       return zipDist(z1,zip)<=dist


def findNewGrantsNearby():
  print("We will look for brand new hams in our area!")
  cyr=int(input("Give cutoff year: "))
  cm=int(input("Give (numerically) cutoff month: "))
  cd=int(input("Give cutoff date: "))
  cmiles=float(input("Give max miles: "))
  print("Default zipcode of 20770 is being used.")
  L=listNew(cm,cd,cyr) #date cutoff here
  print("We found nationally: "+str(len(L))+" new licencees in database.")
  L_close=[]
  newNeighbors=input("Give first part of filename for latex file of addresses: ")
  f=open(newNeighbors+".tex","w")
  for e in L:
    try:     
      if stateLived[e]=="MD" and notTooFar(e,'20770',cmiles): #zip=Greenbelt, distance in miles
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
  newAndClose=input("Give first part of filename for sorted text list: ")
  f=open(newAndClose+".txt","w")
  for e in closeBook:
      f.write(e)
      f.write("\n")
  f.close()
  print("Addresses labels not sorted by last name.. . ")

def findNewMoveInsNearby():
  print("We shall search now for hams who have recently moved into the area!")
  cyr=int(input("Give cutoff year: "))
  cm=int(input("Give (numerically) cutoff month: "))
  cd=int(input("Give cutoff date: "))
  cmiles=float(input("Give max miles: "))
  print("Default zipcode of 20770 is being used.")
  L=listNewAddress(cm,cd,cyr) #date cutoff here
  print("We found nationally: "+str(len(L))+" new addresses in database.")
  L_close=[]
  newNeighbors=input("Give first part of filename for latex file of addresses: ")
  f=open(newNeighbors+".tex","w")
  for e in L:
    try:     
      if stateLived[e]=="MD" and notTooFar(e,'20770',cmiles): #zip=Greenbelt, distance in miles
             L_close.append(e)
    except:
      pass
  print("We found "+str(len(L_close))+" new neighbors who ended up in the area!")
  print(L_close)
  print("Now we will take out the in-town moves")
  L_close2=[]
  for e in L_close:
     if isActuallyNewArrival(e,cmiles):
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
  newAndClose=input("Give first part of filename for sorted text list: ")
  f=open(newAndClose+".txt","w")
  for e in closeBook:
      f.write(e)
      f.write("\n")
  f.close()
  print("Addresses labels not sorted by last name.. . ")


def isActuallyNewArrival(call,dist):
    z=zipLists[Lnum[call]]
    if len(z)>2:
      try:
        result = zipDist(z[-1],'20770')<=dist and zipDist(z[-2],'20770')>=dist
        return result
      except:
        return None
    return None
'''
ct=0
distSum=0
for e in GMRA_L:
  //print(e, zipDist(int(zipcode[e]),20770))
  k=zipDist(int(zipcode[e]),20770)
  if k<90:
    ct+=1
    distSum+=k

'''

reply=input("Do you want to run lists? (Y/N): ")
if reply=="Y":
   findNewGrantsNearby()
   findNewMoveInsNearby()
