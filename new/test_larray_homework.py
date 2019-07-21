#-*- coding: utf-8 -*-
# 由3个数，0-9，不能重复，可以不能被3整除有多少个？

my_num = [0,1,2,3,4,5,6,7,8,9]

good_num = []
for i in range(0,1000):
	a = i // 100
	a_y = i % 100
	b = a_y // 10
	c = a_y % 10
	# print a,":",b,":",c
	if a == b or b == c or a == c:
		print a,":",b,":",c
	else:
		if i>99 and i % 3 != 0:
			good_num.append(i)	

		
print good_num
print len(good_num)