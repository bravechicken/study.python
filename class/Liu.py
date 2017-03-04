#-*- coding: utf-8 -*-
# 定义一个LiuC,再定义一个LiuHY
# LiuC 有属性(name,age,money)
# LiuC 有方法(study-"print study")
# LiuC 有方法(look)
# LiuHY 也有方法(study-"print study")
# LiuHY 继承了look
class LiuC:
	def __init__(self,_name,_age,_money):
		self.name = _name
		self.age = _age
		self.money = _money

	def look(self):
		print self.name , " will look my money",self.money


class LiuHY(LiuC):
	def __init__(self):
		LiuC.__init__(self, "刘浩越","11",10000000000000)

	def sing(self,songName):
		print "I can sing:",songName

l1 = LiuC("刘创",40,50000000000000)
l2 = LiuHY()
l1.look()
l2.look()
l2.sing("字母歌")