#-*- coding: utf-8 -*-
import random
print "小朋友，我们来猜数吧（1-10）！！！"
print "猜吧:"

guessNumber = str(random.randint(1, 10))
inputNumber = raw_input()

while guessNumber != inputNumber:
	print "没猜对，我大电脑出的数是",guessNumber,"，你接着猜吧："
	guessNumber = str(random.randint(1, 10))
	inputNumber = raw_input()
	#print guessNumber,"/",inputNumber
	
print "牛X，猜对了!"