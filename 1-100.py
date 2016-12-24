#-*- coding: utf-8 -*-
def sumScore(englishScores):
	sum = 0
	for name in englishScores:
		print name,":",englishScores[name]
		sum=sum+englishScores[name]
	return sum

def sumIt(two):
	one = 0
	while two > 0:
		one=one+two
		two=two-1
	print "one=",
	print one
	return one

two = 300
one = sumIt(two)
print one

sum=0
for i in range(101):
	sum=sum+i
print sum

englishScores = {"刘浩越":100,"黄原里奥":70,"崔天硕":100}
print englishScores["崔天硕"]

sum = sumScore(englishScores)
print "总成绩",sum
print "平均成绩",sum/len(englishScores)


################
#abc = 123
#bcd = abc*abc*abc*abc + 3
#print bcd
def hello(hao):
	return hao*hao*hao*hao+3
	
abc = 123
bcd = hello(abc)
print bcd




