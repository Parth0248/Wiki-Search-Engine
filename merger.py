import os

def mergefiles(a,b):
    print ("merging files "+ str(a)+" and "+str(b))
    file1 = open('./temp/'+str(a)+'.txt','r')
    file2 = open('./temp/'+str(b)+'.txt','r')
    newfile = open('./temp/'+"merg"+'.txt','w+')
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
    os.remove('./temp/'+str(b)+'.txt')
    os.remove('./temp/'+str(a)+'.txt')
    os.rename('./temp/'+"merg"+'.txt', './temp/'+str(a+1)+'.txt')


r=6
for i in range(1,r+1):
    if i == r:
        os.rename('./temp/'+str(i)+'.txt', './temp/'+"temp_final"+'.txt')
        break
    mergefiles((i), i+1)
