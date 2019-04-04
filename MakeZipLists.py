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