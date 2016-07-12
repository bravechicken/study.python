#-*- coding: utf-8 -*-
import random
print "star war game start"
print "0 1 2 3 4 5 6 7 8 9 是按照我方战机的等级来排的，请猜出台式战机的等级来帮助我们打败帝国，记住要打出你的战机等级（0 1 2 3 4 5 6 7 8 9 ）"
gassNumber = 7
inputNumber = 0
while gassNumber != inputNumber:
	print "我们损失了",
	for i in range(0,inputNumber):
		print "✈️",
	print "架X翼战机，我们被帝国打败了！"
	gassNumber = random.randint(1, 10)
	inputNumber = int(raw_input())
print '谢谢你，帝国被我们打败了'	