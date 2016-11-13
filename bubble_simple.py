#-*- coding: utf-8 -*-
                    #
a = [12,13,11,21,18,23,56,10,6,33]
print a
myLen10 = len(a)#10

for i in range(myLen10,1,-1): #i: 10-> 1
	
	for j in range(0,i-1): #j: 0-> 6 , range(0,5)
		
		if a[j]>a[j+1]:
			temp = a[j+1]
			a[j+1] = a[j]
			a[j] = temp
	

print a


#range(开始，结束，步长值)