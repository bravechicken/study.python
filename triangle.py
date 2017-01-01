def haha(x):
	for w in range(x):
		print "*",
	
fuzhi=3

for i in range(fuzhi,0,-1):
	haha(i)
	print

def sqr(x):
	return mul(x,x)

def mul(x,y):
	return x*y

s = sqr(25)
print s

#5!=5*4*3*2*1
def magic_mul(x):
	if x==1 : 
		return 1
	else:
		return x * magic_mul(x-1)

print magic_mul(15)
# for i in range(1,10000):
# 	try:
# 		print magic_mul(i)
# 	except RuntimeError,e:
# 		print "max is:",i
# 		break
