#-*- coding: utf-8 -*-
def print_array(arr,hand=-1,index=-1):
	print "[",
	for i in range(len(arr)):
		if(i==hand):
			print arr[i],"(#)","\t",
		elif(i==index):	
			print arr[i],"^","\t",
		elif(i==index+1):	
			print arr[i],"^","\t",			
		else:
			print arr[i],"\t",

	print "]"	



a = [12,13,11,21,18,23,56,10,6,33]

#your program....
#use bubble
#要用嵌套循环
#第一层嵌套从头到尾
	#第二层嵌套是从头到一层循环的手指头那
		#当前和后一个比
		#如果我比他大，我就跟他换个
		#否则，我就不动位置
#这里面要用到几个概念：循环(for)、比较(>/<)、判断(if)、数组


myLen = len(a)

#第一层嵌套从头到尾
for i in range(myLen):
	#print myLen-i,":",a[myLen-i-1]

	#我就是第二层嵌套循环
	print "----------------------------------------------------------------------"
	print "我的手指头现在指着：",myLen-i-1
	print_array(a,myLen-i-1)
	print "----------------------------------------------------------------------"
	for j in range(myLen-i-1):
		print "我现在比第",j,"个和",j+1,"个：",a[j],a[j+1],"\t",
		print_array(a,myLen-i-1,j)	
		
		#当前和后一个比
		#如果我比他大，我就跟他换个
		#否则，我就不动位置		
		if a[j]>a[j+1]:
			temp = a[j+1]
			a[j+1] = a[j]
			a[j] = temp
			_tmp = raw_input("我比它大，我们换个")
		_tmp = raw_input("比下面的两个...")
	_tmp = raw_input("手指头继续...")		


# 0	10-0-1 = 9
# 1   10-1-1 = 8 
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9




#print a