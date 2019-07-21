#-*- coding: utf-8 -*-
def find_5_3(max_num):
	result = []
	for i in range(max_num):
		if i % 3 == 0 and i % 5 == 0:
			result.append(i)
	return result

num_list = find_5_3(10000)	
print num_list
print "一共有：" , len(num_list)