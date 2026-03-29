#yikes must now update removals yuck
f=open("Removals.txt")
d=[]
for lyne in f:
    d.append(lyne[:-1])

f.close()    

f=open("LocalHams.txt","r")
d2=[]
for lyne in f:
    d2.append(lyne[:-1])
f.close()    

d3=[]
for i in range(2,len(d2)):
    h=d2[i]
    #print(h)
    L=h.index("[")
    R=h.index("]")
    #print(h[L+1:R])
    d3.append(h[L+1:R])
    d.append(h[L+1:R])

f=open("NewRemovalsList.txt","w")
d.sort()
for e in d:
    f.write(e+"\n")
f.close()
