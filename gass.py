import random
print "start"
gassNumber = '1'
inputNumber = raw_input()
while gassNumber != inputNumber:
	print "x"
	gassNumber = str(random.randint(1, 10))
	inputNumber = raw_input()
print 'yes'	