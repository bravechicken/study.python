#this is a dog mu zi
class Dog:
	def __init__(self,_name,_color,_brand):
		self.name = _name
		self.color = _color
		self.brand = _brand

	def bark(self):
		print "wang!wang!wang:",self.name

	def bite(self):
		print "teng!teng!teng:",self.brand


# create

dog1 = Dog("liao","yello","dongba")
dog2 = Dog("cuitianshuo","white","hujiaolou")
dog3 = Dog("leyu","black","hujiaolou")
dog1.bark()
dog2.bark()
dog3.bark()