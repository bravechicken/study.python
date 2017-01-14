
class LevelProfile(object):
	def __init__(self,levelkeys):
		self.levelnamesDict={}
		self.levelkeys=levelkeys
		
		# init the dict with keys and assign them 0 values
		for key in self.levelkeys:
			self.levelnamesDict[key]=0
		
		# set the 1st to 1 cause its playable by default
		self.levelnamesDict[self.levelkeys[0]]=1
		
	def assignKey(self,key,value):
		self.levelnamesDict[key]=value
		
	def resetValues(self):
		# get all the dict keys
		namesList=self.levelnamesDict.keys()
		
		for name in namesList:
			self.levelnamesDict[name] = 0
			
class SoundManager(object):
	def __init__(self,soundsList):
		self.canPlaySounds=True
		self.soundsList=soundsList
		
	def playSound(self,soundID):
		if self.canPlaySounds:
			self.soundsList[soundID].play()
