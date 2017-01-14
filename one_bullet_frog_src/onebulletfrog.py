import pygame,sys,math,random,cPickle,os.path,os
from pygame.locals import*
from getpath import*

# fullpath = os.path.abspath(__file__)
maindir = os.path.split(fullpath)[0]

# change directory to lib and import the code
libdir = os.path.join(maindir,"lib")
#os.chdir(libdir)

# add a module search path	cause im importing from a different folder
sys.path.append(libdir)

#print os.getcwd()

from gameclass import*

#os.chdir(maindir)

pygame.mixer.pre_init(44100,-16,2,1024)
pygame.init()

WIDTH=320
HEIGHT=240

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
timepassed=0
FPS=0
clock=pygame.time.Clock()

pygame.display.set_caption("One Bullet Frog")
screen=pygame.display.set_mode((WIDTH,HEIGHT),HWSURFACE|DOUBLEBUF|FULLSCREEN)

pygame.mouse.set_visible(False)

		
		
# create the master game object
game = Game(screen=screen)
endCondition=None

while True:
	
	if not game.continueFromLastLvl:
		game=Game(screen=screen)
		game.readLevelDataFile()
		game.showStartScreen()
		game.initialise()
		
	else:
		game.keyID+=1
		levelChoice=game.tempLevelTexts[game.keyID]
		game=Game(game.keyID,game.soundHandler.canPlaySounds,screen=screen)
		game.readLevelDataFile()	# theres a ton of duplication of code here unfortunately
		game.loadLevels()			# I load levels twice cause im lazy to rewrite a ton of shit
		game.tempLevelTexts=game.levelsList.keys()
		game.tempLevelTexts.sort()
		game.initialise(levelChoice)
		
	game.showInstructionScreen()	
	endCondition=game.runGame()
	
	if endCondition=="win":
		game.showCompletedScreen()
	elif endCondition=="lose":
		# show dead screen here
		game.showDeadScreen()	
