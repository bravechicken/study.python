import pygame,sys,math,random,cPickle,os.path
from pygame.locals import*
from globals import*
from gameobjects import*
from utils import*
from tiles import*

absdir=os.path.abspath(__file__)
libdir=os.path.split(absdir)[0]
maindir=os.path.split(libdir)[0]
fontdir=os.path.join(maindir,"fonts")
imagedir=os.path.join(maindir,"images")
sfxdir=os.path.join(maindir,"sfx")

class Game(object):
	def __init__(self,keyID=None,soundBool=True,screen=None):
		
		
		self.globalscreen=screen
		self.gameFontSmall=pygame.font.Font(os.path.join(fontdir,"bitout.fon"),6)
		self.gameFontMed=pygame.font.Font(os.path.join(fontdir,"bitout.fon"),16)
		self.uiFontMed=pygame.font.Font(os.path.join(fontdir,"8-BIT WONDER.TTF"),10)
		self.uiFontBig=pygame.font.Font(os.path.join(fontdir,"8-BIT WONDER.TTF"),17)
		self.bannerFontBig=pygame.font.Font(os.path.join(fontdir,"PressStart2P.ttf"),14)
		self.bannerFontNorm=pygame.font.Font(os.path.join(fontdir,"PressStart2P.ttf"),11)
		self.bannerFontMed=pygame.font.Font(os.path.join(fontdir,"PressStart2P.ttf"),8)
		self.gameClock=pygame.time.Clock()
		self.timepassed=0
		self.numMenuOptions=4
		self.pointerAngle=0
		self.gameIsRunning=True
		self.gameMaxTime=180000
		self.formattedTime=self.getTime(self.gameMaxTime)
		
		self.condition=None
		self.levelChoice=None
		
		if keyID == None:
			self.keyID=0
		else:
			self.keyID=keyID
			
		self.tempLevelTexts=None
		self.continueFromLastLvl=False
		
		# startScreenVars
		self.selectedOption=0
		self.pointerImage=pygame.image.load(os.path.join(imagedir,"ui_pointer.png")).convert_alpha()
		self.pointerRect=self.pointerImage.get_rect()
		self.soundAllow="on"
		self.startTextY=(HEIGHT/2)+20
		
		
		self.bannerGameText=DamageTextBar((0,0),"One Bullet Frog",self.bannerFontBig,0,0,(200,50,110))
		startGameText=DamageTextBar((0,0),"level",self.bannerFontNorm,0,0)
		soundToggleText=DamageTextBar((0,0),"sound  %s" % self.soundAllow,self.bannerFontNorm,0,0)
		creditsText=DamageTextBar((0,0),"credits",self.bannerFontNorm,0,0)
		quitGameText=DamageTextBar((0,0),"quit",self.bannerFontNorm,0,0)
		
		self.uiTextBarList=[]
		self.uiTextBarList.append(startGameText)
		self.uiTextBarList.append(soundToggleText)
		self.uiTextBarList.append(creditsText)
		self.uiTextBarList.append(quitGameText)
		
		# initialise the textBar positions
		for textBar in self.uiTextBarList:
			textBar.x=(WIDTH/3)-20
			textBar.y=self.startTextY
			self.startTextY+=20
		
		
		# i actually dont need these vars
		self.statesList=["startscreen","gamerunning","gamepaused","gameend"]
		self.state=self.statesList[0]
		
		# define global game variables
		
		self.MAPWIDTH=40
		self.MAPHEIGHT=20
		self.TILESIZE=16
		self.SURFACEWIDTH= (self.MAPWIDTH * self.TILESIZE) + 10
		self.SURFACEHEIGHT= (self.MAPHEIGHT * self.TILESIZE) + 10
		
		self.levelsList={}
		self.leveldata=None
		self.importantObs=[] 		# holds doors and shit
		self.agents=[]
		self.enemyObjects=[]
		self.gameObjectsList=[] 		# holds animated effects,mostly ones which interact with other objects
		self.emitterList=[]				# holds purely aesthetic fx ; dust etc
		self.collidableTiles=[]
		self.surface=pygame.Surface((self.SURFACEWIDTH,self.SURFACEHEIGHT))
		self.surface.set_colorkey((255,0,255))
		
		self.surfaceRect=self.surface.get_rect()
		self.slackPixels=15
		self.cameraMinX = (WIDTH/2) - self.slackPixels
		self.cameraMaxX = (WIDTH/2) + self.slackPixels
		self.cameraMinY = (HEIGHT/2) - self.slackPixels
		self.cameraMaxY = (HEIGHT/2) + self.slackPixels
		self.camSpeed=1
		self.cameraShakeVal=4.0
		self.isShaking=False
		self.numIteration=0
		self.defaultCamShake=4.0
		self.angle=0 		# for the camera shake
		
		self.explosionDamage=5
		self.swordDamage=3
		self.maxExplosionVel=4.0
		self.maxSwordDVel=1.8
		self.maxFlameDVel=2.0
		self.flameDamage=3
		self.eggDamage=5
		
		self.map=[]
		
		self.tileIdentifiers=["F","D","W","M","B","S","T","U","V","X","Y","Z"]
		
		# load images
		self.masterPlayerImgs=[]
		self.bloaterMasterImgs=[]
		self.redmanMasterImgs=[]
		self.jumperMasterImgs=[]
		self.trampMasterImgs=[]
		
		self.gunMasterImages=[]
		
		runleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"frog_rn_lft.png"))
		runrightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"frog_rn_rt.png"))
		standSheet=self.sliceSheet(16,16,os.path.join(imagedir,"frog_stand.png"))
		jumpSheet=self.sliceSheet(16,16,os.path.join(imagedir,"frog_jump.png"))
		deathleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"death_lft.png"))
		deathrightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"death_rt.png"))
		
		self.masterPlayerImgs.append(standSheet)
		self.masterPlayerImgs.append(runleftSheet)
		self.masterPlayerImgs.append(runrightSheet)
		self.masterPlayerImgs.append(jumpSheet)
		self.masterPlayerImgs.append(deathleftSheet)
		self.masterPlayerImgs.append(deathrightSheet)
		
		# bloater images
		bloaterstandSheet=self.sliceSheet(16,16,os.path.join(imagedir,"bloater_stand.png"))
		bloaterfireleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"bloater_fire_lft.png"))
		bloaterfirerightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"bloater_fire_rt.png"))
		
		self.bloaterMasterImgs.append(bloaterstandSheet)
		self.bloaterMasterImgs.append(bloaterfireleftSheet)
		self.bloaterMasterImgs.append(bloaterfirerightSheet)
		
		# redman images
		redmanstandSheet=self.sliceSheet(16,16,os.path.join(imagedir,"redman_stand.png"))
		redmanwalkleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"redman_walk_lft.png"))
		redmanwalkrightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"redman_walk_rt.png"))
		redmanrunleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"redman_rn_lft.png"))
		redmanrunrightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"redman_rn_rt.png"))
		redmandieleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"redman_die_lft.png"))
		redmandierightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"redman_die_rt.png"))
		
		self.redmanMasterImgs.append(redmanstandSheet)
		self.redmanMasterImgs.append(redmanwalkleftSheet)
		self.redmanMasterImgs.append(redmanwalkrightSheet)
		self.redmanMasterImgs.append(redmanrunleftSheet)
		self.redmanMasterImgs.append(redmanrunrightSheet)
		self.redmanMasterImgs.append(redmandieleftSheet)
		self.redmanMasterImgs.append(redmandierightSheet)
		
		# jumper images
		jumperstandSheet=self.sliceSheet(22,22,os.path.join(imagedir,"jumper_stand.png"))
		jumpersjumpSheet=self.sliceSheet(22,22,os.path.join(imagedir,"jumper_jump.png"))
		
		self.jumperMasterImgs.append(jumperstandSheet)
		self.jumperMasterImgs.append(jumpersjumpSheet)
		
		# tramp images
		self.trampstandSheet=self.sliceSheet(16,16,os.path.join(imagedir,"tramp_stand.png"))
		self.tramprunleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"tramp_rn_lft.png"))
		self.tramprunrightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"tramp_rn_rt.png"))
		self.trampjumpSheet=self.sliceSheet(16,16,os.path.join(imagedir,"tramp_rn_rt.png"))
		self.trampthrowleftSheet=self.sliceSheet(16,16,os.path.join(imagedir,"tramp_throw_lft.png"))
		self.trampthrowrightSheet=self.sliceSheet(16,16,os.path.join(imagedir,"tramp_throw_rt.png"))
		self.trampswordSheet=self.sliceSheet(12,6,os.path.join(imagedir,"tramp_sword.png"))
		
		self.trampMasterImgs.append(self.trampstandSheet)
		self.trampMasterImgs.append(self.tramprunleftSheet)
		self.trampMasterImgs.append(self.tramprunrightSheet)
		self.trampMasterImgs.append(self.trampjumpSheet)
		self.trampMasterImgs.append(self.trampthrowleftSheet)
		self.trampMasterImgs.append(self.trampthrowrightSheet)
		
		# madbat images
		self.madbatMasterImgs=self.sliceSheet(16,16,os.path.join(imagedir,"madbat.png"))
		
		# dandy images
		self.dandyMasterImgs=self.sliceSheet(16,16,os.path.join(imagedir,"dandy.png"))
		
		# gun images
		destroyergunSheet=self.sliceSheet(12,12,os.path.join(imagedir,"destroyer_gun.png"))
		basicgunSheet=self.sliceSheet(12,12,os.path.join(imagedir,"basic_gun.png"))
		
		self.gunMasterImages.append(basicgunSheet)
		self.gunMasterImages.append(destroyergunSheet)
		
		# tile images
		self.tileSheet=self.sliceSheet(16,16,os.path.join(imagedir,"tile2.png"))
		
		# load animated effects images
		self.hitfxSheet=self.sliceSheet(16,16,os.path.join(imagedir,"hitfx.png"))
		self.hitObfxSheet=self.sliceSheet(16,16,os.path.join(imagedir,"hitobfx.png"))
		self.puffObfxSheet=self.sliceSheet(22,16,os.path.join(imagedir,"puff.png"))
		self.splashObfxSheet=self.sliceSheet(22,20,os.path.join(imagedir,"eggsplash.png"))
		self.dustObfxSheet=self.sliceSheet(12,12,os.path.join(imagedir,"dust_fx.png"))
		self.tileblowfxSheet=self.sliceSheet(12,12,os.path.join(imagedir,"tileblow_fx.png"))
		self.flamefxSheet=self.sliceSheet(12,12,os.path.join(imagedir,"fire_fx.png"))
		self.explosionfxSheet=self.sliceSheet(64,64,os.path.join(imagedir,"explosion_fx.png"))
		self.startBannerAnim=self.sliceSheet(160,120,os.path.join(imagedir,"tadanim_st.png"))
		
		
		# create banner animation object
		self.banner=AnimObject((0,0),self.startBannerAnim,fps=6,numLoops = -1)
		self.banner.x=(WIDTH/2) -(self.banner.rect.width/2)
		self.banner.y=14
		
		
		# load bgs for parallax scrolling 
		self.staticBgImage=pygame.image.load(os.path.join(imagedir,"bluerocks_bg.png")).convert_alpha()
		self.staticParaImg=pygame.image.load(os.path.join(imagedir,"bluerocks_para.png")).convert_alpha()
		
		self.staticBgRect=self.staticBgImage.get_rect()
		self.staticParRect=self.staticParaImg.get_rect()
		
		# single images
		# load bullet images
		self.bloaterBulletImg=pygame.image.load(os.path.join(imagedir,"pngbullets.png")).convert_alpha()
		self.egggImage=pygame.image.load(os.path.join(imagedir,"egg.png")).convert_alpha()
		self.rocketBulletImg=pygame.image.load(os.path.join(imagedir,"rocket.png")).convert_alpha()
		self.rocketBulletImgBlit=pygame.image.load(os.path.join(imagedir,"rocket.png")).convert_alpha()
			
		self.lockedImg=pygame.image.load(os.path.join(imagedir,"locked.png")).convert_alpha()
		
		self.soundList=[]
		
		# load sounds
		scrollSnd=pygame.mixer.Sound(os.path.join(sfxdir,"cursormove.ogg"))
		enterSnd=pygame.mixer.Sound(os.path.join(sfxdir,"enter.ogg"))
		escSnd=pygame.mixer.Sound(os.path.join(sfxdir,"altmenu.ogg"))
		hitTileSnd=pygame.mixer.Sound(os.path.join(sfxdir,"hitTile.ogg"))
		hurtSnd=pygame.mixer.Sound(os.path.join(sfxdir,"hurt.ogg"))
		landSnd=pygame.mixer.Sound(os.path.join(sfxdir,"land.ogg"))
		laserCSnd=pygame.mixer.Sound(os.path.join(sfxdir,"lasercharge.ogg"))
		laserFSnd=pygame.mixer.Sound(os.path.join(sfxdir,"laserfire.ogg"))
		shootSnd=pygame.mixer.Sound(os.path.join(sfxdir,"shoot.ogg"))
		swordSnd=pygame.mixer.Sound(os.path.join(sfxdir,"swordthrow.ogg"))
		gun1Snd=pygame.mixer.Sound(os.path.join(sfxdir,"firegun.ogg"))
		gun2Snd=pygame.mixer.Sound(os.path.join(sfxdir,"firegun2.ogg"))
		ouchSnd=pygame.mixer.Sound(os.path.join(sfxdir,"ouch.ogg"))
		doorSnd=pygame.mixer.Sound(os.path.join(sfxdir,"doorcol.ogg"))
		refuseSnd=pygame.mixer.Sound(os.path.join(sfxdir,"refuse.ogg"))
		
		# music
		pygame.mixer.music.load(os.path.join(sfxdir,"bgmusic.ogg"))
		pygame.mixer.music.play(-1)
		
		# constants to access sounds to play
		self.scSnd=0
		self.enSnd=1
		self.escSnd=2
		self.httSnd=3
		self.hrtSnd=4
		self.lnSnd=5
		self.lacSnd=6
		self.lafSnd=7
		self.shoSnd=8
		self.swrSnd=9
		self.g1Snd=10
		self.g2Snd=11
		self.owSnd=12
		self.doSnd=13
		self.rfSnd=14
		
		self.soundList.append(scrollSnd)
		self.soundList.append(enterSnd)
		self.soundList.append(escSnd)
		self.soundList.append(hitTileSnd)
		self.soundList.append(hurtSnd)
		self.soundList.append(landSnd)
		self.soundList.append(laserCSnd)
		self.soundList.append(laserFSnd)
		self.soundList.append(shootSnd)
		self.soundList.append(swordSnd)
		self.soundList.append(gun1Snd)
		self.soundList.append(gun2Snd)
		self.soundList.append(ouchSnd)
		self.soundList.append(doorSnd)
		self.soundList.append(refuseSnd)
		
		
		self.soundHandler=SoundManager(self.soundList)
		self.soundHandler.canPlaySounds=soundBool
		
	def sliceSheet(self,w,h,filename,setcolorkey=0):
	
		master_image=pygame.image.load(filename).convert_alpha()
		#if setcolorkey==1:
			#master_image.set_colorkey((255,0,255))
			#print "setting color key"
		master_w,master_h=master_image.get_size()
		imglist=[]
	
		for i in xrange(int(master_w/w)):
			imglist.append(master_image.subsurface(i*w,0,w,h))
		return imglist

	
	def showStartScreen(self):
		
		self.loadLevels()
		
		levelTexts=self.levelsList.keys()
		levelTexts.sort()
		self.tempLevelTexts=levelTexts
		
		#print self.levelsList
		lockedImgRect = self.lockedImg.get_rect()
		#lockedImgRect.topleft=()
		
		self.bannerGameText.textRect.center=(self.banner.rect.x+160,self.banner.rect.centery+50)
		
		levText=self.uiFontMed.render(levelTexts[self.keyID],False,(200,50,110))
		levTextRect=levText.get_rect()
		levTextRect.top=self.uiTextBarList[0].textRect.top
		levTextRect.left=self.uiTextBarList[0].textRect.right+24
		
		while True:
			self.timepassed=self.gameClock.tick(45)
			
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						pygame.quit()
						sys.exit()
					
					if event.key==K_LEFT:
						if self.selectedOption==0:
							self.keyID = (self.keyID-1) % len(levelTexts)
							self.soundHandler.playSound(self.scSnd)
						
					if event.key==K_RIGHT:
						if self.selectedOption==0:
							self.keyID = (self.keyID+1) % len(levelTexts)
							self.soundHandler.playSound(self.scSnd)
						
					if event.key==K_UP:
						self.selectedOption = (self.selectedOption-1) % self.numMenuOptions
						self.soundHandler.playSound(self.scSnd)
						
					if event.key==K_DOWN:
						self.selectedOption= (self.selectedOption+1) % self.numMenuOptions
						self.soundHandler.playSound(self.scSnd)
						
					if event.key==K_z or event.key==K_RETURN:
						if self.selectedOption==0:
							if self.leveldata.levelnamesDict[levelTexts[self.keyID]]==1:
								# only register if level is playable
								self.levelChoice=levelTexts[self.keyID]
								self.state=self.statesList[1]
								self.soundHandler.playSound(self.enSnd)
								return
							else:
								self.soundHandler.playSound(self.rfSnd)
							
						elif self.selectedOption==1:
							if self.soundHandler.canPlaySounds:
								self.soundHandler.canPlaySounds=False
								pygame.mixer.music.stop()
								self.soundAllow="off"
							else:
								self.soundHandler.canPlaySounds=True
								self.soundAllow="on"
								self.soundHandler.playSound(self.enSnd)
								pygame.mixer.music.play(-1)
						
						elif self.selectedOption==2:
							self.showCreditsScreen()
							
						elif self.selectedOption==3:
							pygame.quit()
							sys.exit()
			
			
			self.pointerRect.x = self.uiTextBarList[self.selectedOption].textRect.left-25
			self.pointerRect.centery = self.uiTextBarList[self.selectedOption].textRect.centery
			self.pointerAngle+=10
			
			self.pointerRect.x += 4* math.cos((self.pointerAngle * (math.pi/180)))
			
			# set this counter to 0 because its been accumulating before the game begins
			# prevents lasers from going off at the same time
			#for tile in self.collidableTiles:
			#	if tile.type=="laser":
			#		tile.accFireTime=random.randint(100,3000)

			
			for i in range(self.numMenuOptions):
				if i==self.selectedOption:
					self.uiTextBarList[i].color=(10,255,0)
				else:
					self.uiTextBarList[i].color=(255,255,255)
			
			# draw sound enabled text
			self.uiTextBarList[1].text= "sound  %s" % self.soundAllow
			
			for textBar in self.uiTextBarList:
				textBar.update(self.timepassed)
			
			self.banner.update(self.timepassed)
			
			self.globalscreen.fill(BLACK)
			
			self.bannerGameText.draw(self.globalscreen)
			
			for textBar in self.uiTextBarList:
				textBar.draw(self.globalscreen)
				
			levText=self.uiFontMed.render(levelTexts[self.keyID],False,(200,50,110))
			
			if self.leveldata.levelnamesDict[levelTexts[self.keyID]]==0:
				# level is not playable
				# draw its text kinda transparent
				levText.set_alpha(60)
			else:
				levText.set_alpha(255)
			
			
			levTextRect=levText.get_rect()
			levTextRect.top=self.uiTextBarList[0].textRect.top
			levTextRect.left=self.uiTextBarList[0].textRect.right+24
			
			lockedImgRect.topright=(levTextRect.left-5,levTextRect.top)
		
					
			# draw level name on screen
			self.globalscreen.blit(levText,levTextRect)
			
			if self.leveldata.levelnamesDict[levelTexts[self.keyID]]==0:
				self.globalscreen.blit(self.lockedImg,lockedImgRect)
				
			self.banner.draw(self.globalscreen)
			
			self.globalscreen.blit(self.pointerImage,self.pointerRect)
			
			pygame.display.flip()
	
	def showCreditsScreen(self):
		blackSurface=pygame.Surface((WIDTH,HEIGHT))
		blackSurface.set_alpha(245)
		blackSurfaceRect=blackSurface.get_rect()
		line1Text=DamageTextBar((60,150),"A game by Fyeidale Edmond.",self.bannerFontMed,0,0,(255,240,210))
		line2Text=DamageTextBar((60,150),"fienixgdev@gmail.com",self.bannerFontMed,0,0,(255,240,210))
		line3Text=DamageTextBar((60,150),"twitter: @fydmyster",self.bannerFontMed,0,0,(255,240,210))
		line4Text=DamageTextBar((60,150),"Thanks to Dr Petters sfxr and musagi.",self.bannerFontMed,0,0,(255,240,210))
		
		line1Text.textRect.topleft=(10,50)
		line2Text.textRect.topleft=(10,90)
		line3Text.textRect.topleft=(10,105)
		line4Text.textRect.topleft=(10,120)
		
		
		notblitted=True
		while True:
		
			self.timepassed=self.gameClock.tick(45)
			
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						self.soundHandler.playSound(self.escSnd)
						return
					if event.key==K_z or event.key==K_RETURN:
						self.soundHandler.playSound(self.escSnd)
						return
						
			
			if notblitted:
				self.globalscreen.blit(blackSurface,blackSurfaceRect)
				line1Text.draw(self.globalscreen)
				line2Text.draw(self.globalscreen)
				line3Text.draw(self.globalscreen)
				line4Text.draw(self.globalscreen)
				
				notblitted=False
			
			pygame.display.flip()
	
	
	
	def showInstructionScreen(self):
		
		blackSurface=pygame.Surface((WIDTH,HEIGHT))
		blackSurface.set_alpha(220)
		blackSurfaceRect=blackSurface.get_rect()
		line1Text=DamageTextBar((60,150),"Get to the Door to complete the room.",self.bannerFontMed,0,0,(255,240,210))
		line2Text=DamageTextBar((60,150),"The Door will only open when",self.bannerFontMed,0,0,(255,240,210))
		line3Text=DamageTextBar((60,150),"the room is clear of monsters.",self.bannerFontMed,0,0,(255,240,210))
		line4Text=DamageTextBar((60,150)," ",self.bannerFontMed,0,0,(255,240,210))
		
		line5Text=DamageTextBar((60,150),"Press Z to jump, and X to shoot.",self.bannerFontMed,0,0,(255,240,210))
		
		
		doorOpenImage=self.tileSheet[17]
		doorClosedImage=self.tileSheet[16]
		
		line1Text.textRect.topleft=(10,50)
		line2Text.textRect.topleft=(10,90)
		line3Text.textRect.topleft=(10,105)
		line4Text.textRect.topleft=(10,120)
		line5Text.textRect.topleft=(10,135)
		
		doorOpenImageRect=doorOpenImage.get_rect()
		doorClosedImageRect=doorClosedImage.get_rect()
		
		doorClosedImageRect.topleft=(50,line1Text.textRect.bottom+8)
		doorOpenImageRect.topleft=(line2Text.textRect.right+12,line2Text.textRect.centery-4)
		
		notblitted=True
		while True:
		
			self.timepassed=self.gameClock.tick(45)
			
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						self.soundHandler.playSound(self.escSnd)
						return
					if event.key==K_z or event.key==K_RETURN:
						self.soundHandler.playSound(self.escSnd)
						return
						
			
			if notblitted:
				self.globalscreen.blit(blackSurface,blackSurfaceRect)
				line1Text.draw(self.globalscreen)
				line2Text.draw(self.globalscreen)
				line3Text.draw(self.globalscreen)
				line4Text.draw(self.globalscreen)
				line5Text.draw(self.globalscreen)
				self.globalscreen.blit(doorClosedImage,doorClosedImageRect)
				self.globalscreen.blit(doorOpenImage,doorOpenImageRect)
				notblitted=False
			
			pygame.display.flip()
	
	
	
	def showDeadScreen(self):
		
		deathText=DamageTextBar((WIDTH/2-50,200),"YOU DIED",self.uiFontBig,0,-7,(245,10,30))
		
		while True:
			self.timepassed=self.gameClock.tick(45)
			
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						self.soundHandler.playSound(self.escSnd)
						return
						
					
					if event.key==K_z:
						self.soundHandler.playSound(self.escSnd)
						return
						
			
			deathText.update(self.timepassed)
			
			self.globalscreen.fill(BLACK)
			
			deathText.draw(self.globalscreen)
			
			pygame.display.flip()
	
	def showPauseScreen(self):
		blackSurface=pygame.Surface((WIDTH,HEIGHT))
		blackSurface.set_alpha(100)
		blackSurfaceRect=blackSurface.get_rect()
		quitFromPauseText=DamageTextBar((60,150),"press Q to quit",self.uiFontMed,0,0,(255,240,210))
		notblitted=True
		while True:
			for event in pygame.event.get():
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						self.soundHandler.playSound(self.escSnd)
						return
					if event.key==K_q:
						self.condition=None
						self.gameIsRunning=False
						self.soundHandler.playSound(self.escSnd)
						return
						
			quitFromPauseText.update(self.timepassed)
			
			if notblitted:
				self.globalscreen.blit(blackSurface,blackSurfaceRect)
				quitFromPauseText.draw(self.globalscreen)
				notblitted=False
				
			pygame.display.flip()
			
	def showCompletedScreen(self):
		numOptions=2
		selectedOption=0
		self.pointerRect.x=40
		
		deathText=DamageTextBar((40,200),"LEVEL COMPLETED",self.uiFontBig,0,-7,(255,240,210))
		gotoNextLevelText=DamageTextBar((60,150),"NEXT LEVEL",self.uiFontMed,0,0,(255,240,210))
		gotoMainMenuText=DamageTextBar((60,170),"MAIN MENU",self.uiFontMed,0,0,(255,240,210))
		
		# write to profile and unlock the next level by setting it to 1
		if self.keyID <= len(self.leveldata.levelkeys) -2:
			
			self.leveldata.levelnamesDict[self.leveldata.levelkeys[self.keyID+1]]=1
			
			
		# overwrite profile data
		f = file("profile.dat","w")
		cPickle.dump(self.leveldata,f)
		f.close()
			
		while True:
			self.timepassed=self.gameClock.tick(45)
			
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				
				if event.type==KEYDOWN:
					if event.key==K_ESCAPE:
						pygame.quit()
						sys.exit()
					
					if event.key==K_UP:
						if numOptions==2:
							selectedOption = (selectedOption-1) % numOptions
							self.soundHandler.playSound(self.scSnd)
							
					if event.key==K_DOWN:
						if numOptions==2:
							selectedOption = (selectedOption+1) % numOptions
							self.soundHandler.playSound(self.scSnd)
					
					if event.key==K_z:
						if numOptions==2:
							if selectedOption==0:
								self.continueFromLastLvl=True
								self.soundHandler.playSound(self.enSnd)
								return
							else:
								self.continueFromLastLvl=False
								self.soundHandler.playSound(self.escSnd)
								return
						else:
							self.continueFromLastLvl=False
							return
						
			
			if self.keyID >= len(self.tempLevelTexts)-1:
				#print "this is the final level"
				numOptions=1
			else:
				numOptions=2
				
			if numOptions==2:
				if selectedOption==0:
					self.pointerRect.centery=gotoNextLevelText.textRect.centery
				else:
					self.pointerRect.centery=gotoMainMenuText.textRect.centery
			
				self.pointerRect.x=40
				self.pointerAngle+=10
				self.pointerRect.x += 3* math.cos((self.pointerAngle * (math.pi/180)))
				
			elif numOptions==1:
				self.pointerRect.centery=gotoMainMenuText.textRect.centery
			
			deathText.update(self.timepassed)
			if numOptions==2:
				gotoNextLevelText.update(self.timepassed)
				
			gotoMainMenuText.update(self.timepassed)
			
			
			
			self.globalscreen.fill(BLACK)
			
			deathText.draw(self.globalscreen)
			if numOptions==2:
				gotoNextLevelText.draw(self.globalscreen)
			
			gotoMainMenuText.draw(self.globalscreen)
			
			
			self.globalscreen.blit(self.pointerImage,self.pointerRect)
			
			pygame.display.flip()
	
	
	
	def getCellCoords(self,xpos,ypos):
		cellX = math.floor( xpos/self.TILESIZE )
		cellY = math.floor( ypos/self.TILESIZE )
		
		return (int(cellX),int(cellY))
	
	def loadLevels(self):
		# open level text file
		f = open("levels.txt")
		
		stringslist=f.readlines()
		
		f.close()
		
		strippedStrings=[]
		# strip newline char from all files
		for string in stringslist:
			line=string.rstrip("\r\n")
			strippedStrings.append(line)
		
		for string in strippedStrings:
			if string=="":
				strippedStrings.remove(string)
		
		for i in range(len(strippedStrings)):
			if strippedStrings[i].startswith("level"):
				# place level name in dictionary
				levelname = strippedStrings[i][12:]
				# put the proceeding 20 strings into the map
				map=[]
				map.append(strippedStrings[i+1 : i+21])
				self.levelsList[levelname]=map
				
				
	def initialise(self,continuelevelChoice=None):
		if continuelevelChoice == None:
			self.map = self.levelsList[self.levelChoice][0] 
			#print self.levelsList.keys()
		else:
			self.map = self.levelsList[continuelevelChoice][0]
			
		# sanity check
		assert len(self.map) == self.MAPHEIGHT and len(self.map[0])==self.MAPWIDTH
		
		# parse the map and append the appropriate tile objects
		for row in range(self.MAPHEIGHT):
			for col in range(self.MAPWIDTH):
				
				if self.map[row][col] == "1":
					# append BoxTile object
					door = Door((col * self.TILESIZE , row * self.TILESIZE),self)
					self.importantObs.append(door)
				
				elif self.map[row][col] == "W":
					# append BoxTile object
					tile = BoxTile((col * self.TILESIZE , row * self.TILESIZE),self,"UP",self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "M":
					# append BoxTile object
					tile = BoxTile((col * self.TILESIZE , row * self.TILESIZE),self,"MID",self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "B":
					# append BoxTile object
					tile = BoxTile((col * self.TILESIZE , row * self.TILESIZE),self,"DOWN",self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "X":
					# append BoxTile object
					tile = BoxTile((col * self.TILESIZE , row * self.TILESIZE),self,"UP",self.TILESIZE,self.TILESIZE,kind="redearth")
					self.collidableTiles.append(tile)
					
				elif self.map[row][col] == "Y":
					# append BoxTile object
					tile = BoxTile((col * self.TILESIZE , row * self.TILESIZE),self,"DOWN",self.TILESIZE,self.TILESIZE,kind="redearth")
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "Z":
					# append BoxTile object
					tile = BoxTile((col * self.TILESIZE , row * self.TILESIZE),self,"MID",self.TILESIZE,self.TILESIZE,kind="redearth")
					self.collidableTiles.append(tile)
				
				
				elif self.map[row][col] == "S":
					# append BoxTile object
					tile = LaserTile((col * self.TILESIZE , row * self.TILESIZE),self,"LEFT",self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "T":
					# append BoxTile object
					tile = LaserTile((col * self.TILESIZE , row * self.TILESIZE),self,"UP",self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "U":
					# append BoxTile object
					tile = LaserTile((col * self.TILESIZE , row * self.TILESIZE),self,"RIGHT",self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "V":
					# append BoxTile object
					tile = LaserTile((col * self.TILESIZE , row * self.TILESIZE),self,"DOWN",self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "D":
					# append BoxTile object
					tile = DestructableTile((col * self.TILESIZE , row * self.TILESIZE),self,None,self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "F":
					# append BoxTile object
					tile = FlamingTile((col * self.TILESIZE , row * self.TILESIZE),self,None,self.TILESIZE,self.TILESIZE)
					self.collidableTiles.append(tile)
				
				elif self.map[row][col] == "P":
					# append the player controlled object
					player=AAB((col * self.TILESIZE , row * self.TILESIZE),self)
					self.agents.append(player)
						
				elif self.map[row][col] == "E":
					# append the player controlled object
					enemy=Enemy((col * self.TILESIZE , row * self.TILESIZE),"bloater",self)
					self.enemyObjects.append(enemy)
				
				elif self.map[row][col] == "Q":
					# append the player controlled object
					enemy=Enemy((col * self.TILESIZE , row * self.TILESIZE),"tramp",self)
					self.enemyObjects.append(enemy)
				
				elif self.map[row][col] == "K":
					# append the player controlled object
					enemy=Enemy((col * self.TILESIZE , row * self.TILESIZE),"madbat",self)
					self.enemyObjects.append(enemy)
				
				elif self.map[row][col] == "L":
					# append the player controlled object
					enemy=Enemy((col * self.TILESIZE , row * self.TILESIZE),"dandy",self)
					self.enemyObjects.append(enemy)
				
				elif self.map[row][col] == "R":
					# append the player controlled object
					enemy=Enemy((col * self.TILESIZE , row * self.TILESIZE),"redman",self)
					self.enemyObjects.append(enemy)
				
				elif self.map[row][col] == "J":
					# append the player controlled object
					enemy=Enemy((col * self.TILESIZE , row * self.TILESIZE),"jumper",self,22,22)
					self.enemyObjects.append(enemy)
				
				
				elif self.map[row][col] == "F":
					# append the player controlled object
					enemy=FlyingCreature((col * self.TILESIZE , row * self.TILESIZE),self)
					self.enemyObjects.append(enemy)
		
		# set the state for special tiles
		for tile in self.collidableTiles:
			if tile.type=="laser":
				tile.setState()
		
	def drawGameObjects(self,Surface):
		# clear surface
		self.surface.fill((255,0,255))
		
		# draw map tiles
		for tile in self.collidableTiles:
			tile.draw(self.surface)
		
		# draw importantObs
		for item in self.importantObs:
			item.draw(self.surface)
		
		
		# draw agents
		for agent in self.agents:
			agent.draw(self.surface)
		
		# draw enemies
		for enemy in self.enemyObjects:
			enemy.draw(self.surface)
		
		# draw animated effects and animated aesthetics
		for effect in self.gameObjectsList:
			effect.draw(self.surface)
		
		for emitter in self.emitterList:
			emitter.draw(self.surface)
		
		
		#print len(self.collidableTiles)
		
		# draw surface to screen
		Surface.blit(self.surface,self.surfaceRect)
		
		#pygame.draw.circle(screen,RED,(self.cameraMinX,HEIGHT/2),5)
		#pygame.draw.circle(screen,WHITE,(self.cameraMaxX,HEIGHT/2),5)
		
	def updateGameObjects(self,timepassed):
		
		# update game played time
		self.gameMaxTime-=timepassed
		self.formattedTime=self.getTime(self.gameMaxTime)
		
		# handle camera movement
		#self.camSpeed = abs(self.agents[0].xvel)
		self.cameraPositionToCenter((self.agents[0].rect.centerx,self.agents[0].rect.centery))
		
		
		# update all tiles
		# only when game state is running
		#if self.state==self.statesList[1]:
		for tile in self.collidableTiles:
			tile.update(timepassed)
		
		# remove dead destructable tiles
		for tile in self.collidableTiles:
			if tile.type=="destructable":
				if not tile.alive:
					self.collidableTiles.remove(tile)
		
		
		
		# update all agents
		for agent in self.agents:
			agent.update(timepassed)
		
		# update all agents
		for agent in self.agents:
			if not agent.alive:
				# you die ;end the game
				
				self.condition="lose"
				self.gameIsRunning=False
		
		# calculate velocity for scrolling bg
		
		xvec=self.agents[0].xvel
		yvec=self.agents[0].yvel
		
		self.staticParRect.x -= xvec *0.2
		self.staticParRect.y -= yvec *0.2
		
		# handle enemy AI
		for enemy in self.enemyObjects:
			if enemy.type=="troop":
				enemy.decideState()
				enemy.Act()
				#print enemy.state
			elif enemy.type=="flyer":
				enemy.Act()
			
			
		# update all enemies
		for enemy in self.enemyObjects:
			enemy.update(timepassed)
		
		# remove dead enemies
		for enemy in self.enemyObjects:
			if not enemy.alive:
				self.enemyObjects.remove(enemy)
		
		# update effects
		for effect in self.gameObjectsList:
			effect.update(timepassed)
		
		for emitter in self.emitterList:
			emitter.update(timepassed)
			
		# remove dead effects
		for effect in self.gameObjectsList:
			if not effect.alive:
				self.gameObjectsList.remove(effect)
		 
		for emitter in self.emitterList:
			if not emitter.alive:
				self.emitterList.remove(emitter)
		
		# update importantObs
		for item in self.importantObs:
			item.update(timepassed)
		
		
	def handleCollisions(self):
		# handle agent tile collisions
		
		for agent in self.agents:
			# reset the length collidedTiles list to 0 before recount
			agent.collidedTiles=[]
			#agentCellX,agentCellY = self.getCellCoords(agent.x,agent.y)
			
			for tile in self.collidableTiles:
				# only collide with tiles in a given range
				# get tile cell coords
				#tileCellX,tileCellY = self.getCellCoords(tile.x,tile.y)
				#if tile.cellX in range(agentCellX-agent.collisionRange,agentCellX+agent.collisionRange) and \
				#tile.cellY in range(agentCellY-agent.collisionRange,agentCellY+agent.collisionRange):
				
				agent.resolveBoxTile(tile)
				
				# dont think this is the best place to handle this but for now
				# handle collisions with the tiles laser if it has one
				if tile.type=="laser":
					if tile.isFiring and not agent.tempInvicibilty:
						if tile.laserRect.colliderect(agent.colrect):
							# lose some HP
							# reset the object's textBar variables
							agent.shotAccWindowTime=0
							agent.accDamage+=tile.laserDamage
							agent.HP-=tile.laserDamage
							agent.damagedDisplayed=False
							agent.tempInvicibilty=True
							
							self.soundHandler.playSound(self.owSnd)
							
			# handle collisions with deadly enemies
			for enemy in self.enemyObjects:
				if enemy.kind=="jumper" or enemy.kind=="redman" or enemy.kind=="madbat":
					if not agent.tempInvicibilty:
						if enemy.rect.colliderect(agent.colrect):
						
							agent.xvel*= (-agent.xvel/(agent.xvel+0.01))*2.9
							agent.shotAccWindowTime=0
							agent.accDamage+=enemy.touchDamage
							agent.HP-=enemy.touchDamage
							agent.damagedDisplayed=False
							agent.tempInvicibilty=True
							self.soundHandler.playSound(self.owSnd)
		# handle enemy tile collisions
		
		for enemy in self.enemyObjects:
			if enemy.type=="troop":
				# reset the length collidedTiles list to 0 before recount
				enemy.collidedTiles=[]
				#enemyCellX,enemyCellY = self.getCellCoords(enemy.x,enemy.y)
				for tile in self.collidableTiles:
					# only collide with tiles in a given range
					# get tile cell coords
					#tileCellX,tileCellY = self.getCellCoords(tile.x,tile.y)
				
					#if tile.cellX in range(enemyCellX-enemy.collisionRange,enemyCellX+enemy.collisionRange) and \
					#tile.cellY in range(enemyCellY-enemy.collisionRange,enemyCellY+enemy.collisionRange):
				
					enemy.resolveBoxTile(tile)
			
			elif enemy.type=="flyer":
				for tile in self.collidableTiles:
					if enemy.rect.colliderect(tile.rect):
						enemy.getCollisonInfo(tile)
						
		
		player=self.agents[0]
		
		# check for player bullet collision with dandy bullets
		for enemy in self.enemyObjects:
			if enemy.kind=="dandy":
				
				for dandybullet in enemy.gun.bulletsList:
					
					for playerbullet in player.gun.bulletsList:
						if playerbullet.bulletrect.colliderect(dandybullet.bulletrect):
							playerbullet.alive=False
							dandybullet.alive=False
							self.soundHandler.playSound(self.scSnd)
							
							# create fx animated object
							fxObject = AnimObject((dandybullet.bulletrect.centerx,dandybullet.bulletrect.centery),self.hitfxSheet,0,0)
							self.gameObjectsList.append(fxObject)
					
							
		# check if we touch a door then offer to go to next level of retry or quit
		for item in self.importantObs:
			if item.state=="open":
				if self.agents[0].colrect.colliderect(item.rect):
					self.soundHandler.playSound(self.enSnd)
					
					# show completed level screen
					self.condition="win"
					self.gameIsRunning=False
		
		# handle tile collision with fx
		for tile in self.collidableTiles:
			for fx in self.gameObjectsList:
				if fx.collisiontype=="sword" or fx.collisiontype=="egg":
					if fx.rect.colliderect(tile.rect):
						
						fxObject = AnimObject((fx.rect.centerx-11,fx.rect.y-9),self.splashObfxSheet,0,0)
						#fxObject.rect.center=(self.rect.centerx,self.rect.centery)
						self.gameObjectsList.append(fxObject)
						self.gameObjectsList.remove(fx)
						
		
		# handle collision with flame emitter particles
		for emitter in self.emitterList:
			if emitter.collidable:
				if emitter.collisiontype=="flames":
					for particle in emitter.particleList:
						if player.colrect.colliderect(particle.rect) and not player.tempInvicibilty:
							player.damagedDisplayed=False
							player.tempInvicibilty=True
							player.shotAccWindowTime=0
							player.accDamage+=self.flameDamage
							player.HP-=self.flameDamage
							self.soundHandler.playSound(self.owSnd)
							
							# blow player away
							# get vector from player to fx center
							# doing the calculation the other way round to reverse the heading
							playerFxVX= player.rect.centerx - particle.rect.centerx 
							playerFxVY= player.rect.centery - particle.rect.centery
	
							# normalise
							len = math.sqrt(playerFxVX*playerFxVX + playerFxVY*playerFxVY)
					
							playerFxVX /= len
							playerFxVY /= len
					
							headingX = playerFxVX * self.maxFlameDVel
							headingY = playerFxVY * self.maxFlameDVel
					
							player.xvel+=headingX
							player.yvel+=headingY
			
		
		
		# handle player collision with fx
		for fx in self.gameObjectsList:
			if fx.collisiontype=="explosion":
				# its an explosion
				if fx.collidable and not player.tempInvicibilty:
					if player.colrect.colliderect(fx.rect):
						#print "hit by explosion"
					
						player.damagedDisplayed=False
						player.tempInvicibilty=True
						player.shotAccWindowTime=0
						player.accDamage+=self.explosionDamage
						player.HP-=self.explosionDamage
						self.soundHandler.playSound(self.owSnd)
						
						# blow player away
						# get vector from player to fx center
						# doing the calculation the other way round to reverse the heading
						playerFxVX= player.rect.centerx - fx.rect.centerx 
						playerFxVY= player.rect.centery - fx.rect.centery
	
						# normalise
						len = math.sqrt(playerFxVX*playerFxVX + playerFxVY*playerFxVY)
					
						playerFxVX /= len
						playerFxVY /= len
					
						headingX = playerFxVX * self.maxExplosionVel
						headingY = playerFxVY * self.maxExplosionVel
					
						player.xvel+=headingX
						player.yvel+=headingY
			elif fx.collisiontype=="sword":
				# player hit by sword
				if player.colrect.colliderect(fx.rect):
						#print "hit by sword"
						
						player.damagedDisplayed=False
						player.tempInvicibilty=True
						player.shotAccWindowTime=0
						player.accDamage+=self.swordDamage
						player.HP-=self.swordDamage
						self.soundHandler.playSound(self.owSnd)
						
						# blow player away
						# get vector from player to fx center
						# doing the calculation the other way round to reverse the heading
						playerFxVX= player.rect.centerx - fx.rect.centerx 
						playerFxVY= player.rect.centery - fx.rect.centery
	
						# normalise
						len = math.sqrt(playerFxVX*playerFxVX + playerFxVY*playerFxVY)
					
						playerFxVX /= len
						playerFxVY /= len
					
						headingX = playerFxVX * self.maxSwordDVel
						headingY = playerFxVY * self.maxSwordDVel
					
						player.xvel+=headingX
						player.yvel+=headingY
			
						# remove fx from list
						self.gameObjectsList.remove(fx)
						
			elif fx.collisiontype=="egg":
				# player hit by egg
				if player.colrect.colliderect(fx.rect):
						#print "hit by egg"
						
						player.damagedDisplayed=False
						player.tempInvicibilty=True
						player.shotAccWindowTime=0
						player.accDamage+=self.eggDamage
						player.HP-=self.eggDamage
						self.soundHandler.playSound(self.owSnd)
						
						fxObject = AnimObject((fx.rect.centerx-11,player.colrect.y-14),self.splashObfxSheet,0,0)
						#fxObject.rect.center=(self.rect.centerx,self.rect.centery)
						self.gameObjectsList.append(fxObject)
						
						# remove fx from list
						self.gameObjectsList.remove(fx)
			
						
	def handleInput(self):
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			
			if event.type==KEYDOWN:
				if event.key==K_ESCAPE:
					self.soundHandler.playSound(self.escSnd)
					self.showPauseScreen()
			
				if event.key==K_LEFT:
					if not self.agents[0].isDead:
						self.agents[0].moveleft=True
			
				if event.key==K_RIGHT:
					if not self.agents[0].isDead:
						self.agents[0].moveright=True
			
				if event.key==K_UP:
					
					self.agents[0].moveup=True
			
				if event.key==K_DOWN:
					if not self.agents[0].isDead:
						self.agents[0].KDIsDown=True
			
				if event.key==K_z:
					if not self.agents[0].isDead:
						self.agents[0].jump()
				
				if event.key==K_x:
					if not self.agents[0].isDead:
						self.agents[0].shootingHeld=True

			if event.type==KEYUP:
				if event.key==K_LEFT:
					self.agents[0].moveleft=False
			
				if event.key==K_RIGHT:
					self.agents[0].moveright=False
			
				if event.key==K_UP:
					self.agents[0].moveup=False
			
				if event.key==K_DOWN:
					self.agents[0].KDIsDown=False
			
				if event.key==K_z:
					pass
				
				if event.key==K_x:
					self.agents[0].shootingHeld=False
	
	def getTime(self,mils):
		secs=int((mils/1000)%60)
		mins=int((mils/(1000*60))%60)
		hours=int((mils/(1000*60*60))%24)
		return (hours,mins,secs)

	
	def runGame(self):
		timepassed=0
		clock=pygame.time.Clock()
		firstTick=True
		while True:
			self.handleInput()
			
			self.updateGameObjects(timepassed)
			self.handleCollisions()
			
			
			if not self.gameIsRunning:
				return self.condition
			
			textSurf=self.bannerFontNorm.render("HP : %s" % self.agents[0].HP,False,WHITE)
			textSurf.convert()
			textRect=textSurf.get_rect()
			textRect.topleft=(5,5)
			
			# draw timer
			timerText=self.bannerFontBig.render("%s:%s:%s" % self.formattedTime,False,(255,200,200))
			timerText.convert_alpha()
			timerTextRect=timerText.get_rect()
			timerTextRect.centerx=WIDTH/2
			timerTextRect.y=5
			timerText.set_alpha(150)
			
			self.globalscreen.fill(BLACK)
			self.shakeCamera()
			
			self.globalscreen.blit(self.staticBgImage,self.staticBgRect)
			#screen.blit(self.staticParaImg,self.staticParRect)
			
			self.drawGameObjects(self.globalscreen)
			self.globalscreen.blit(textSurf,textRect)
			#screen.blit(timerText,timerTextRect)
	
			pygame.display.flip()
	
	
			timepassed=clock.tick(50)
			FPS=clock.get_fps()
			
			# just discovered that timepassed is cumulative from  the last call to tick
			# so to start without accumalated time i ignore the first timepassed return value
			if firstTick:
				timepassed=0
				firstTick=False
			
			
			
			
	def getWorldToScreenCoords(self,worldPos):
		# returns screen coords of object
		worldX,worldY=worldPos
		screenX = (worldX % WIDTH) + self.surfaceRect.x 
		screenY = (worldY % HEIGHT) + self.surfaceRect.y
		
		return (screenX,screenY)
		
	def cameraMove(self,playerPos):
		playerScreenX,playerScreenY = self.getWorldToScreenCoords(playerPos)
		#print playerScreenX,playerScreenY
		
		# handle x axis
		if playerScreenX < self.cameraMinX and self.surfaceRect.x < 0 and self.agents[0].xvel < 0:
			# move camera left ; ie move surface right 
			self.surfaceRect.x += self.camSpeed
		elif playerScreenX > self.cameraMaxX and self.surfaceRect.right > WIDTH and self.agents[0].xvel > 0:
			# move camera right ; ie move surface left
			self.surfaceRect.x -= self.camSpeed
		
		# handle y axis
		if playerScreenY < self.cameraMinY and self.surfaceRect.y < 0 and self.agents[0].yvel < 0:
			# move camera up ; ie move surface down 
			self.surfaceRect.y += self.camSpeed
		elif playerScreenY > self.cameraMaxY and self.surfaceRect.bottom > HEIGHT and self.agents[0].yvel > 0:
			# move camera down ; ie move surface up
			self.surfaceRect.y -= self.camSpeed
	
	def shakeCamera(self):
	
		if not self.isShaking:
			pass
			
		else:
			self.angle+=80
			self.cameraShakeVal-=0.3
			
			if self.cameraShakeVal>0:
				self.surfaceRect.y += self.cameraShakeVal * math.cos(self.angle *(math.pi/180))
			
			else:
				
				self.isShaking=False
				self.cameraShakeVal=self.defaultCamShake
			
	def cameraPositionToCenter(self,playerPos):
		if True:
			xpos,ypos=playerPos
		
			# distance from player to center of the screen
			xvec = (WIDTH/2) - xpos 
			yvec = (HEIGHT/2) - ypos
			
		
			self.surfaceRect.x = xvec
			self.surfaceRect.y = yvec
		
	def lerp(self,color1,color2,factor):
		r1,g1,b1=color1
		r2,g2,b2=color2
		
		newR = r1 + (r2-r1) * factor
		newG = g1 + (g2-g1) * factor
		newB = b1 + (b2-b1) * factor
	
		newColor=(newR,newG,newB)
		return newColor
	
	def readLevelDataFile(self):
		
		# open profile.dat for reading
		# if it doesnt exist create it and chuck a LevelProfile object in it
		self.loadLevels()
		
		levelTexts=self.levelsList.keys()
		levelTexts.sort()
		self.tempLevelTexts=levelTexts
		
		try:
			f=file("profile.dat")
			f.close()
		except IOError:
			#print "theres no dat file ; create it"
			f=file("profile.dat","w")
			
			# create level object and place in file
			leveldata=LevelProfile(self.tempLevelTexts)
			cPickle.dump(leveldata,f)
			f.close()
			#print "dat file created"
		
		# read level object from profile
		f=file("profile.dat")
		self.leveldata=cPickle.load(f)
		f.close()
