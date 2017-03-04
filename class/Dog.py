#this is a dog mu zi
class Dog:
	def __init__(self,_name,_color,_brand,_teeth):
		self.name = _name
		self.color = _color
		self.brand = _brand
		#self.shu = "chichen";
		self.age = 11;
		self.teeth = _teeth

	def bark(self):
		print "wang!wang!wang:",self.name

	def bite(self):
		print "teng!teng!teng:",self.brand
		print "i have ",self.teeth," tooth"


class Hashiqi(Dog):
	def __init__(self):
		Dog.__init__(self, "HaShiQi","white","HSQ",26)

	def sing(self,songName):
		print "I can sing:",songName

	def bite(self):
		print "HSQ bite!!!!"	

# create

dog1 = Dog("liao","yello","dongba",100)
dog2 = Dog("cuitianshuo","white","hujiaolou",1)
dog3 = Dog("leyu","black","hujiaolou",10)
hsq = Hashiqi()

dog1.bark()
dog1.bite()
dog2.bark()
dog3.bark()
shibushi = int(raw_input())
print shibushi
if shibushi == 1 :
	dog1.bite() 
else:
	hsq.sing("huanLeSong")
	hsq.bite()
