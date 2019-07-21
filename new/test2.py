def find237(test):
	number = []
	for o in range (test):
		if o % 2 == 0 and o % 3 ==0 and o % 7 == 0:
			number.append(o)
	return number
g = find237(20000)
print "The number of number" , len(g)