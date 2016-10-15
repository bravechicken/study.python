#-*- coding: utf-8 -*-

#先读入逗号分割的一串数字，
#如2，44，3，42，32，47
tmp = raw_input()

#把这个这串字符变成一个字符串数组,用字符串的split函数
#"2，44，3，42，32，47"=>[“2”，“44”，“3”，“42”，“32”，“47”]
arr = tmp.split(",")

#再把字符串数组，转成整形数组
#[“2”，“44”，3，42，32，47]
arrInt = []
for looper in arr:
	arrInt.append(int(looper))

#开始神奇的冒泡排序
arryLen = len(arrInt)

#每次冒泡选1个最大的，
#从最后一个，然后是倒数第二个，然后是倒数第三个。。。
for l1 in range(arryLen-1,0,-1):
	#从0循环到这次定义的那个位置
	for l2 in range(0,l1):
		#如果我比我后面的一个大
		#那么我和他换位置，否则就不换		
		if(arrInt[l2]>arrInt[l2+1]):
			temp = arrInt[l2+1]
			arrInt[l2+1] = arrInt[l2]
			arrInt[l2] = temp

#打印排序结果
for looper in arrInt:
	print looper,	
