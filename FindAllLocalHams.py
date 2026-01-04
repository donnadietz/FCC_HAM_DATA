#Donna Dietz N2SZ donna.dietz@gmail.com
#Jan 2026

print("Thank you for using my Python Script! Help me debug it! donna.dietz@gmail.com N2SZ")
print("Please wait a minute or two while the entire FCC database is being read.")
print("This code attempts to find hams in given state w/in specified center/radius of zip provided.")


#http://wireless.fcc.gov/uls/index.htm?job=transaction&page=weekly
#grab both amateur zipped files
#wireless.fcc.gov/uls/data/complete/a_amat.zip
#wireless.fcc.gov/uls/data/complete/l_amat.zip  <--- using this one
#close to 400 MB in total, takes awhile. unzip. 
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

LAST_DATE_IN_DB=""
fyle=open('l_amat/CO.dat','r')
for line in fyle:
    myline = line
fyle.close()    
if len(myline)>20:
        LAST_DATE_IN_DB=line.split('|')[4]

#print(LAST_DATE_IN_DB+" is last date in Database!")  #ONLY APROX!!!


lic_class={}
# Here, I create my first dictionary!  Yay!
# Key is callsign  (temp[4] in this case)

fyle=open('l_amat/AM.dat','r')
for line in fyle:
    temp=line.split('|')
    lic_class[temp[4]]=temp[5]
fyle.close()


active={}
HAHV={}

# Two more dictionaries, also call for key. 

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
FRN={}          #NOTE: FRN is a better ID than Call FWIW
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
        initial[temp[4]]=temp[9].upper()
    if(len(temp[10])):
        lastname[temp[4]]=temp[10].upper()
    if(len(temp[11])):
        suffix[temp[4]]=temp[11].upper()
    if(len(temp[15])):
        #address[temp[4]]=temp[15].upper()        
        address[temp[4]]=re.sub(","," ",temp[15].upper())
    if(len(temp[16])):
        city[temp[4]]=temp[16].upper()
    if(len(temp[17])):
        stateLived[temp[4]]=temp[17]
    if(len(temp[18])):
        zipcode[temp[4]]=temp[18][0:5]
    if(len(temp[15])==0) and len(temp[19]):
        address[temp[4]]="P.O. BOX "+str(temp[19])
    if(len(temp[22])):
        FRN[temp[4]]=temp[22]
fyle.close()    


calls=list(FRN.keys()) # I need a list of calls. I use it for all my keys.
                       # so I should have a list of them, right?   

for i in range(len(calls)):
    if calls[i] in address and address[calls[i]][0:6].upper()=="PO BOX":
        address[calls[i]]="P.O. Box"+address[calls[i]][6:]

#This stunt is specifically so people like "WX4TV" will be matched with
#his family who is "KM4TXT" etc. Some people write PO Box differently

#end of hamFCC2, start unzipzips.

f=open("zips.csv","r")   # Dictionary to convert zip (string) to lat/lon
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

def findLL(zip):   # Well some zips don't exist so this is a hack.
    if zip in z:
        return (z[zip])
    for i in range(1,5000):
        for j in [-1,1]:
            fakezip = str(int(zip)+i*j)
            if len(fakezip)==4:
                fakezip='0'+fakezip
            if fakezip in z:
                #print("Using zip: "+fakezip+" instead of "+zip)
                return(z[fakezip])
    print("Giving up and using origin for zip")        
    return(("0","0"))

#End unzipzips start newgrants

grant={}            # Create dictionary call -> date
fyle=open('l_amat/HS.dat','r')
for line in fyle:
    temp=line.split('|')
    if temp[5].strip()=="SYSGRT":
        grant[temp[3]]=temp[4]
fyle.close()

def listNew(m,d,yr):
    L=[]
    k=grant.keys()  # a list...
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
    try:                              # I don't recall why, but it's a hack.
       if not temp[6] in zipLists:
           try:
               zipLists[temp[6]]=[temp[18][0:5]]  #temp[6] is like L00132...
           except:
               pass
       else:
           try:
               zipLists[temp[6]].append(temp[18][0:5])  #temp[1][0:5] is zip
           except:
               pass
    except:
               pass

#end MakeZipLists start newaddress

newAddress={}    # Find all new addresses in whole database
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

#CHANGES BELOW_______________________________________________________

L_close=[]
    
def findHamsNearby(cmiles,czip):
  #I'm going to ignore ourstate!!!  .... where does that happen? remind me!?
  print("We will look for hams in our area!")
  #L=listNew(cm,cd,cyr) #date cutoff here
  print("We found nationally: "+str(len(calls))+" licencees in database.")
  #L_close=[]  #Forced into global status. Hopefully you only run this once!
  Neighbors = "LocalHams"      # Use this common file to store hits.
  f=open(Neighbors+".tex","a")
  for e in calls:  #DITCHING "PEOPLE" without names... usually clubs. or addresses...
    try:           #I know ... I'm being too picky! :)
      if (e in lastname) and (active[e]=='A') and notTooFar(e,czip,cmiles) and stateLived[e]==ourstate and len(address[e].strip(" "))>0: #zip=Greenbelt, distance in miles 
             L_close.append(e)
    except:
        
      pass
  print("We found "+str(len(L_close))+" licencees nearby!")
  print(L_close)
  closeBook=[]
  closeBook2=[] #for the csv
  for e in L_close:
         f.write("\lb{ ")     
         record=""
         record2=""
         try:
            record=record+firstname[e]+" "+initial[e]+" "+lastname[e]+" "
            record2=record2+firstname[e]+", "+initial[e]+", "+lastname[e]+", "
            f.write(firstname[e]+" "+initial[e]+" "+lastname[e]+" "+e+" \\\\\n")
         except:
            try:
                record=record+firstname[e]+" "+lastname[e]+" "
                record2=record2+firstname[e]+",, "+lastname[e]+", "            
                f.write(firstname[e]+" "+lastname[e]+" "+e+" \\\\\n")
            except:
              try:
                 record=record+initial[e]+" "+lastname[e]+" "
                 record2=record2+initial[e]+",, "+lastname[e]+", "              
                 f.write(initial[e]+" "+lastname[e]+" "+e+" \\\\\n")
              except:
                 try:
                     record=record+lastname[e]+" "
                     record2=record2+", , "+lastname[e]+", "             
                     f.write(lastname[e]+" "+e+" \\\\\n")
                 except:
                     record=record+" "+e+" "
                     record2=record2+", ,  "+e+", "                     
                     f.write(e+" \\\\\n")
         record=record+" ["+e+"] "+lic_class[e]+" - "
         record2=record2+" "+e+", "+lic_class[e]+" , "         
         
         try:
            record=record+address[e].upper()+" "
            record2=record2+address[e].upper()+", "
            #if address[e].count(",")==0:
            #    record2=record2+" , "
            #if address[e].count(",")>=2:
            #    print("TOO MANY COMMAS IN RECORD FOR "+e)
            f.write(address[e]+" \\\\\n")        
         except:
            pass
         try:
            record=record+city[e].upper()+", "+stateLived[e]+" "+zipcode[e]
            record2=record2+city[e].upper()+", "+stateLived[e]+", "+zipcode[e]+"\n" 
            f.write(city[e]+", "+stateLived[e]+" "+zipcode[e]+" }\n")        
         except:
            pass
         closeBook.append(record)
         closeBook2.append(record2)
  closeBook.sort()
  closeBook2.sort()
  f.close()
  Close="LocalHams"
  f=open(Close+".txt","a")
  for e in closeBook:
      f.write(e)
      f.write("\n")
  f.close()
  #print("Addresses labels not sorted by last name.. . ")
  f=open("LocalHams.csv","a")
  for e in closeBook2:
      f.write(e)
  f.close()
      

  

#If this works, I'll be happy




#----------------------------------START OF USER INTERACTIONS
import time

reply=input("Do you want to run lists to look for local hams? (Y/N): ")
if reply=="Y" or reply=="y" or reply=="":
    print("New files 'LocalHams.txt' and 'LocalHams.tex' will be written/overwritten (unless you abort this code now).")
    '''
    cyr=input("Give cutoff year: ")
    if cyr=="":
        temp=time.asctime()
        cyr=temp.split()[-1]
    cyr=int(cyr)    
    cm=input("Give (numerically) cutoff month: ")
    if cm=="":
        cm=1
    cm=int(cm)    
    cd=input("Give cutoff date: ")
    if cd=="":
        cd=1
    cd=int(cd)
    '''
    cmiles=input("Give max miles or hit enter to use 17 miles: ")
    if cmiles=="":
        cmiles=17
    else:
        cmiles=float(cmiles)
    print("Enter zipcode below or hit enter to default to 20770")
    czip=input("Give zipcode for center: ")
    if czip=="":
        print("Default zipcode of 20770 is being used.")
        czip="20770"
    #Will you look only in your state or all nearby hams?    
    print("Enter state 2-digit code  below or hit enter to default to 'MD' ")
    ourstate=input("Give state: ")
    if ourstate=="":
        print("Default state of 'MD' is being used.")
        ourstate="MD"
    f=open("LocalHams.txt","w")
    f.write("Local Hams: "+str(cmiles)+" miles away from "+czip+"\n")
    #f.write("Start date: "+str(cm)+"/"+str(cd)+"/"+str(cyr)+"\n")
    f.write("Roughly Last date in Database: "+LAST_DATE_IN_DB+"\n")
    f.close()
    f=open("LocalHams.tex","w")
    f.write("% Local Hams: "+str(cmiles)+" miles away from "+czip+"\n")
    f.write("% \n")
    f.write("% Roughly Last date in Database: "+LAST_DATE_IN_DB+"\n")
    f.close()
    f=open("LocalHams.csv","w")
    f.write("FIRST, MI, LAST, CALL, CLASS, ADDRESS, CITY, STATE, ZIP \n")
    f.close()
        
    findHamsNearby(cmiles,czip)  #fills appropriate globals hopefully



    print("Now, trying to alphabetize everything!")
    
    f=open("LocalHams.csv","r")
    d=[]
    for lyne in f:
        d.append(lyne[:-1])
    f.close()

    hold=[]
    for i in range(1,len(d)):
        hold.append((d[i].split(',')[2], d[i]))
    hold.sort()

    f=open("LocalHams.csv","w") #Ruin the old one!!!
    f.write(d[0])
    f.write("\n")
    for i in range(len(hold)):
        f.write(hold[i][1])
        f.write("\n")
    f.close()

    #  Ok, if that works, let's try the tex file now!

    f=open("LocalHams.tex","r")
    d=[]
    for lyne in f:
        d.append(lyne[:-1])
    f.close()

    for i in range(3, len(d)):
        if '#' in d[i]:
            t=""
            for j in range(len(d[i])):
                if d[i][j]=="#":
                    t=t+'\#'
                else:
                    t=t+d[i][j]
            d[i]=t

    hold=[]
    for i in range(3,len(d),3):
            temp=d[i].split(' ')
            if len(temp)>2:
                hold.append((temp[-3], d[i], d[i+1], d[i+2]))  #Crashed here...
    hold.sort()

    f=open("LocalHams.tex","w") #Ruin the old one!!!
    f.write(d[0])
    f.write("\n")
    f.write(d[1])
    f.write("\n")
    f.write(d[2])
    f.write("\n")

    for i in range(len(hold)):
        f.write(hold[i][1])
        f.write("\n")
        f.write(hold[i][2])
        f.write("\n")
        f.write(hold[i][3])
        f.write("\n")
    
    f.close()

# If we are really lucky, this all worked!
