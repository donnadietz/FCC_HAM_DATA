#Donna Dietz
#Jan 2019
#May 2018
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
#from hamFCC2 import *

import random
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

