a=[34,23,33,32,4,56,88,3,56,73,67,11,56,56,31,8,21]
print a
change=len(a)

for w in range(change,1,-1):

	for e in range(0,w-1):
	

		if a[e]<a[e+1]:
			temp = a[e+1]
			a[e+1] = a[e]
			a[e] = temp

	print a


