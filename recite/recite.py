#!/usr/bin/python
#-*- coding: utf-8 -*-
import random,os,pickle

__total=0
__done=0
__fail=0
__onepass=0
__record={}

#退出时候用于保存当前进度
def recordSave():
	recordFile = open("record","w")
	global record,__total, __done,__fail,__onepass
	record = {"total":__total,"done":__done,"fail":__fail,"onepass":__onepass}
	pickle.dump(record,recordFile)
	recordFile.close()

#重新开始的时候加载进度
def recordLoad():
	if not os.path.exists("./record"): return 
	recordFile = open("record","r")
	global record,__done,__fail,__onepass
	if recordFile:
		record = pickle.load(recordFile)
	__done= int(record["done"])
	__fail= int(record["fail"])
	__onepass = int(record["onepass"])
	print "恢复进度，您之前背过%d,错了%d,一次通过%d..."%(__done,__fail,__onepass)
	recordFile.close();

#用于正确背诵1个后的统计
def statisticsOk(onepassCounter):
	global __total , __done,__onepass
	if(onepassCounter==0): __onepass = __onepass + 1
	__done = __done + 1
	recordSave() #过一个就自动存盘
	if __done%25==0:
		print "厉害哟～，你一口气完成了25个单词，休息，休息，♨️♨️♨️♨️ 一会儿吧......"
		
		raw_input()

#背诵错了的统计
def statisticsFail():
	global __fail
	__fail = __fail + 1

#统计数量的打印
def statisticsPrint():
	global __total , __done,__fail
	print "加油哦，已完成%d/%d,错了%d次,一次对了%d个[quit退出]"%(__done, __total,__fail,__onepass)
	print

#########################################
#从文件words.txt中装载字典
def loadDict():
	dicts = {}
	sentence = {}
	myfile = open('word.txt','r')
	lines = myfile.readlines()
	for line in lines:
			oneWord = line.split("|")
			dicts[oneWord[0]] 	 = oneWord[1]#中文意思
			sentence[oneWord[0]] = oneWord[2]#对应的句子
	myfile.close()
	global __total
	__total = len(dicts)
	return dicts,sentence

#########################################
#随机找3个单词的意思
def getRandomeMean(dicts):
	means3 = []
	for i in range(0,3):
		k = random.randint(0,len(dicts.values())-1)
		_mean = dicts.values()[k]
		means3.append(_mean)
	return means3	

#########################################
#测试中文意思理解
def chineseTest(mean):
	#准备4个单词中文意思
	options = [mean]
	other3 = getRandomeMean(dicts)
	options.extend(other3)
	random.shuffle(options)
	ABCD = ['A','B','C','D']
	statisticsPrint()
	print word
	print 
	print _sentence
	for i in range(0,4):
		print ABCD[i],":",options[i],
	print

	while True:
		choose = raw_input("意思是(ABCD):")
		choose = choose.upper()
		if choose=="QUIT":
			exit()#quit退出

		index = options.index(mean)

		if ABCD[index]==choose:
			break
		else:
			statisticsFail()

#########################################
#测试拼写	
def spellTest(_sentence,word):
	statisticsPrint()
	print _sentence.lower().replace(word.lower(),"______")
	answer = raw_input(mean+":")

	onepassCounter = 0
	while answer.lower()!=word.lower():
		#print "[",answer,"] vs [", word ,"]"
		statisticsFail()
		onepassCounter = onepassCounter + 1
		answer = raw_input(mean+":")
		if answer=="quit":
			exit()#quit退出

	statisticsOk(onepassCounter)


#######################################################################
##  主程序开始
#######################################################################



dicts,sentences = loadDict()

recordLoad()

counter = 0

for (word,mean) in dicts.items():
	if(counter<__done): 
		print "背过了%s,跳过..." %(word)
		counter = counter + 1
		continue
	counter = counter + 1

	_sentence = sentences[word]

	chineseTest(mean)

	os.system('clear')

	spellTest(_sentence,word)
	
	os.system('clear')
	

