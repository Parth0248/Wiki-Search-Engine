import os

def mergefiles(a,b):
    print ("merging files "+ str(a)+" and "+str(b))
    file1 = open('./merge/'+str(a)+'.txt','r')
    file2 = open('./merge/'+str(b)+'.txt','r')
    newfile = open('./merge/'+"merg"+'.txt','w+')
    l1 = file1.readline()
    l2 = file2.readline()
    while (l1 and l2 ): 
        ind1 = l1.split('{')
        ind2 = l2.split('{')
        if ind1[0] < ind2[0]:
            newfile.write(l1)
            l1 = file1.readline()
        elif ind2[0] < ind1[0] : 
            newfile.write(l2)
            l2 = file2.readline()
        elif ind1[0] == ind2[0] :
            newfile.write(ind1[0]+'{' + ind1[1].split('}')[0] + ', ' + ind2[1]) # mergers if two indexes match
            l1 = file1.readline()
            l2 = file2.readline() 
    while (l1):
        newfile.write(l1)
        l1 = file1.readline()
    while (l2):
        newfile.write(l2)
        l2 = file2.readline()
    file1.close()
    file2.close()
    newfile.close()
    os.remove('./merge/'+str(b)+'.txt')
    os.remove('./merge/'+str(a)+'.txt')
    os.rename('./merge/'+"merg"+'.txt', './merge/'+str(a+1)+'.txt')


r=6
for i in range(1,r+1):
    if i == r:
        os.rename('./merge/'+str(i)+'.txt', './merge/'+"temp_final"+'.txt')
        break
    mergefiles((i), i+1)
