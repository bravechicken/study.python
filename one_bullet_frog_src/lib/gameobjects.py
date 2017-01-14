import pygame,math,sys,random
from pygame.locals import*
from globals import*

class DamageTextBar(object):
	def __init__(self,pos,text,font,xvel=0.0,yvel=-0.8,color=(255,255,255)):
		self.x,self.y=pos
		self.alpha=255
		self.font=font
		self.color=color
		self.text=text
		self.textSurf=font.render(text,False,color)
		self.textRect=self.textSurf.get_rect()
		self.textRect.topleft=(self.x,self.y)
		self.xvel=xvel
		self.yvel=yvel
		self.friction=0.928
		self.maxLiveTime = 2500
		self.acctime=0
		self.alive=True
		
	def update(self,timepassed):
		
		self.acctime+=timepassed
		if self.acctime>self.maxLiveTime:
			self.alive=False
		
		self.textSurf=self.font.render(self.text,False,self.color)
		
		self.x+=self.xvel
		self.y+=self.yvel
		
		self.textRect.topleft=(self.x,self.y)
		self.yvel *= self.friction
		self.xvel *= self.friction
	
	def draw(self,Surface):
		Surface.blit(self.textSurf,self.textRect)
	
class AnimObject(object):
	def __init__(self,pos,spriteSheet,xvel=0,yvel=0,friction=0.97,fps=15,numLoops=1,collidable=False,collisiontype=None):
		self.x,self.y=pos
		self.frameImages=spriteSheet
		self.frame=0
		self.fps=fps
				
		self.collisiontype=collisiontype
		self.collidable=collidable		
		self.xvel=xvel
		self.yvel=yvel
		self.friction=friction
		
		self.alive=True
		self.image=self.frameImages[self.frame]
		self.rect= self.image.get_rect()
		self.numLoops=numLoops
		self.numIteration=0
		self.frameCounter=0
		
		self.acctime=0
		self.updateframetime=1000/self.fps
		
	def play(self,timepassed):
		
		if self.alive:
		
			self.acctime+=timepassed
		
			if self.acctime > self.updateframetime:
				if self.numLoops == -1:
					# infinite loop animation
					self.frame = (self.frame + 1) % len(self.frameImages)
					self.acctime=0
			
				elif self.numLoops>0:
					# play for a set number of loop times
					if self.frameCounter >= len(self.frameImages)-1:
						self.numIteration+=1
						self.frameCounter=0
				
					if self.numIteration < self.numLoops:
						self.frame = (self.frame + 1) % len(self.frameImages)
						self.frameCounter+=1
						self.acctime=0
					else:
						#self.frame=len(self.frameImages)-1
						self.alive=False
		
	def update(self,timepassed):
		
		# cycle through the frames
		self.play(timepassed)
		
		self.image=self.frameImages[self.frame]
		
		self.x+=self.xvel
		self.y+=self.yvel
		
		self.xvel*=self.friction
		self.yvel*=self.friction
		
		# update position
		self.rect.x=self.x
		self.rect.y=self.y
		
	def draw(self,Surface):
		Surface.blit(self.image,self.rect)

class AnimEmitter(object):
	def __init__(self,pos,spriteSheet,xvel=0,yvel=0,fps=5,numParticles=5,friction=0.94,addParticleTime=100,collidable=False,collisiontype=None):
		self.x,self.y=pos
		self.xvel=xvel
		self.yvel=yvel
		self.collidable=collidable
		self.collisiontype=collisiontype
		self.spriteSheet=spriteSheet
		self.fps=fps
		self.acctime=0
		self.numParticles=numParticles
		self.addedParticles=0
		self.alive=True
		self.addParticleTime=addParticleTime
		self.particleList=[]
		self.friction=friction
		
	def update(self,timepassed):
		if self.alive:
			self.acctime+=timepassed
			
			if self.addParticleTime!=0:
			
				if self.acctime>self.addParticleTime:
				
					if self.numParticles>0:
						if self.xvel !=0 and self.yvel==0:
							randyvel=random.choice(range(-3,3))
							newParticle=AnimObject((self.x,self.y),self.spriteSheet,self.xvel,randyvel,self.friction,self.fps,collidable=self.collidable,collisiontype=self.collisiontype)
							
						elif self.yvel !=0 and self.xvel==0:
							randxvel=random.choice(range(-3,3))
							newParticle=AnimObject((self.x,self.y),self.spriteSheet,randxvel,self.yvel,self.friction,self.fps,collidable=self.collidable,collisiontype=self.collisiontype)
							
						elif self.yvel !=0 and self.xvel!=0:
							randxvel=random.choice(range(-3,3))
							newParticle=AnimObject((self.x,self.y),self.spriteSheet,self.xvel,self.yvel,self.friction,self.fps,collidable=self.collidable,collisiontype=self.collisiontype)
						
						else:
							randxvel=random.choice(range(-3,3))
							randyvel=random.choice(range(-3,3))
							newParticle=AnimObject((self.x,self.y),self.spriteSheet,randxvel,randyvel,friction=self.friction,collidable=self.collidable,collisiontype=self.collisiontype)
						self.particleList.append(newParticle)
						self.numParticles-=1
			
						self.acctime=0
			
			else:
				# add particles in one go
				if self.numParticles>0:
					for i in range(self.numParticles):
						tempAdditive=(random.randint(0,200))/1000
						basefriction=0.96
						
						randfriction=basefriction+tempAdditive
						randfps=random.randint(7,12)
						randxvel=random.choice(range(-3,3))
						randyvel=random.choice(range(-3,3))
						newParticle=AnimObject((self.x,self.y),self.spriteSheet,randxvel,randyvel,friction=randfriction,fps=randfps)
						self.particleList.append(newParticle)
			
					self.numParticles=0
					
			for particle in self.particleList:
				if not particle.alive:
					self.particleList.remove(particle)
				
			if self.numParticles <=0 and len(self.particleList)==0:
				self.alive=False
		
		for particle in self.particleList:
			particle.update(timepassed)
		
		
	def draw(self,Surface):
	
		for particle in self.particleList:
			particle.draw(Surface)
		
class AAB(object):
	def __init__(self,pos,gameObject,w=16,h=16):
		self.x,self.y=pos
		self.w=w
		self.h=h
		self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
		self.colrect=pygame.Rect(self.x,self.y,self.w-2,self.h-2)
		self.game=gameObject
		self.collidedTiles=[]
		self.behaviour="PlayerControlled"
		self.collisionRange=2
		self.playedDeathAnim=False
		
		# event management vars
		self.eventNotifications=[]
		
		if self.behaviour=="PlayerControlled":
			self.masterPlayerImgs=self.game.masterPlayerImgs
			self.frame=0
			self.anim=0
			self.image=self.masterPlayerImgs[self.anim][self.frame]
			self.fps=12
			self.acctime=0
			self.updateframetime=1000/self.fps
			
		self.gravity=0.08
		self.friction=0.84
		#self.testxvel=self.xvel
		self.xvel=0.0
		self.yvel=0.0
		
		self.oldx=0.0
		self.oldy=0.0
		
		self.maxyvel=4.4
		self.accel=0.23
		self.chargeaccel=0.42
		self.normaccel=0.23
		self.xw = w/2
		self.yw = h/2
		self.jumpHeight=2.4
		self.tanJumpForce=1.1
		self.isJumping=False
		self.KDIsDown=False
		self.tempInvicibilty=False
		self.maxTempInvicibiltyTime=1500
		self.accInvinciTime=0
		self.setVisible=True
		self.maxVisibleToggleTime=50
		self.accToggleTime=0
		
		# for parallax scrolling need these implicit velocities
		self.impXvel=self.xvel 			# just the difference between current tick and last tick positions
		self.impYvel=self.yvel
		
		# hacky one time variables
		self.deadSet=False
		
		self.textBarList=[]		# list should only ever have one element
		self.damagedDisplayed=True
		self.HP=25
		self.accDamage=0
		self.isDead=False		# use this to trigger death animation  for player
		self.alive=True			# use this to clear the object from object list
		self.waitTimeBforShowDmg=1000
		self.shotAccWindowTime=0
		
		if self.behaviour=="PlayerControlled":
			self.lastpressed="left"
		else:
			self.lastpressed=None
		
		# objects owned by player
		self.gun = GunEmitter((self.x,self.y),self.game,self,"basic") 
		self.gunImageDir="left"
		
		if self.gun.type=="destroyer":
			self.gunImage=self.game.gunMasterImages[1][0]
		elif self.gun.type=="basic":
			self.gunImage=self.game.gunMasterImages[0][0]
		
		self.gunrect=self.gunImage.get_rect()
		self.gunrect.centerx=self.rect.centerx
		self.gunrect.centery=self.rect.centery+4
		
		self.shootingHeld=False
		self.moveleft=False
		self.moveright=False
		self.moveup=False
	
	def showHitDamage(self):
		# create textBar to show HP
		# create it 10 pixels above object
		textBar=DamageTextBar((self.rect.x,self.y-8),"-%s" % self.accDamage,self.game.gameFontMed)
		self.textBarList.append(textBar)
		
	def playAnim(self,timepassed):
		if self.moveleft:
			# play running left animation
			self.acctime+=timepassed
			self.anim=1		# runleftSheet index
			if self.acctime>self.updateframetime:
				# go to next frame
				self.frame = (self.frame +1) % len(self.masterPlayerImgs[self.anim])
				self.acctime=0
				
		if self.moveright:
			# play running left animation
			self.acctime+=timepassed
			self.anim=2		# runrightSheet index
			if self.acctime>self.updateframetime:
				# go to next frame
				self.frame = (self.frame+1) % len(self.masterPlayerImgs[self.anim])
				self.acctime=0
		
		if self.isJumping:
			if self.lastpressed=="left":
				if self.yvel > 0:
					# we going down
					self.anim=3
					self.frame=1
				elif self.yvel <= 0:
					# we going up
					self.anim=3
					self.frame=0
			elif self.lastpressed=="right":
				if self.yvel > 0:
					# we going down
					self.anim=3
					self.frame=3
				elif self.yvel <= 0:
					# we going up
					self.anim=3
					self.frame=2
				
		if not self.moveleft and not self.moveright and not self.isJumping and not self.isDead:
			if self.lastpressed=="left":
				self.anim=0
				self.frame=0
			elif self.lastpressed=="right":
				self.anim=0
				self.frame=1
		
		if self.isDead:
			# play death animation
			if self.alive:
				if self.lastpressed=="left" or self.lastpressed==None:
					self.acctime+=timepassed
					self.anim=4		# runrightSheet index
					if self.acctime>self.updateframetime:
						# go to next frame
						if self.frame < len(self.masterPlayerImgs[self.anim])-1:
							self.frame = self.frame + 1 
							self.acctime=0
							
						else:
							print "You have died"
							self.alive=False
				
			
				elif self.lastpressed=="right":
					self.acctime+=timepassed
					self.anim=5		# runrightSheet index
					if self.acctime>self.updateframetime:
						# go to next frame
						if self.frame < len(self.masterPlayerImgs[self.anim])-1:
							self.frame = self.frame + 1 
							self.acctime=0
		
						else:
							print "You have died"
							self.alive=False
				
				
	def jump(self):
		# only jump if we're on top of a tile
		if len(self.collidedTiles) > 0:
			self.yvel -= self.jumpHeight
			self.isJumping=True
			if self.behaviour == "PlayerControlled":
				# add a directional impulse force to the jump
				if self.moveleft:
					self.xvel -= self.tanJumpForce
				elif self.moveright:
					self.xvel += self.tanJumpForce
				
			
	def draw(self,Surface):
		if self.behaviour !="PlayerControlled":
			pass
		else:
			if self.setVisible:
				Surface.blit(self.image,self.rect)
			
		# draw bullets and gun
		self.gun.draw(Surface)
		if self.behaviour=="PlayerControlled":
			if self.gun.type=="basic":
				if self.gunImageDir=="left":
					self.gunImage=self.game.gunMasterImages[0][0]
				
				elif self.gunImageDir=="right":
					self.gunImage=self.game.gunMasterImages[0][1]
				
				elif self.gunImageDir=="up":
					if self.lastpressed=="left":
						self.gunImage=self.game.gunMasterImages[0][2]
					elif self.lastpressed=="right":
						self.gunImage=self.game.gunMasterImages[0][3]
					
					
				elif self.gunImageDir=="down":
					if self.lastpressed=="left":
						self.gunImage=self.game.gunMasterImages[0][4]
					elif self.lastpressed=="right":
						self.gunImage=self.game.gunMasterImages[0][5]
					
				
				
			elif self.gun.type=="destroyer":
				if self.gunImageDir=="left":
					self.gunImage=self.game.gunMasterImages[1][0]
				
				elif self.gunImageDir=="right":
					self.gunImage=self.game.gunMasterImages[1][1]
				
				elif self.gunImageDir=="up":
					if self.lastpressed=="left":
						self.gunImage=self.game.gunMasterImages[1][2]
					elif self.lastpressed=="right":
						self.gunImage=self.game.gunMasterImages[1][3]
						
				elif self.gunImageDir=="down":
					if self.lastpressed=="left":
						self.gunImage=self.game.gunMasterImages[1][4]
					elif self.lastpressed=="right":
						self.gunImage=self.game.gunMasterImages[1][5]
					
				
				
			Surface.blit(self.gunImage,self.gunrect)
				
		# draw textBarList objects
		for textBar in self.textBarList:
			textBar.draw(Surface)
	
	def blink(self,timepassed):
		self.accToggleTime+=timepassed
		
		if self.accToggleTime>self.maxVisibleToggleTime:
			self.setVisible= not self.setVisible
			self.accToggleTime=0
			
	def update(self,timepassed):
		
		if self.tempInvicibilty and not self.isDead:
			self.blink(timepassed)
			self.accInvinciTime+=timepassed
			
			if self.accInvinciTime>self.maxTempInvicibiltyTime:
				self.accInvinciTime=0
				self.tempInvicibilty=False
		
		else:
			self.setVisible=True
	
		if self.behaviour=="PlayerControlled":
			# play animations
			self.image=self.masterPlayerImgs[self.anim][self.frame]
			
			self.playAnim(timepassed)
		
		if not self.isDead:
		
			# handle inputs
			if self.moveleft:
				if len(self.collidedTiles) > 0:
					# we're on ground ; move faster
					self.xvel-=self.accel
				else:
					if self.behaviour!="PlayerControlled":
						# halve movement force
						self.xvel-=(self.accel * 0.89)
					else:
						self.xvel-=(self.accel * 0.949)
					
				self.lastpressed="left"
			
			if self.moveright:
				if len(self.collidedTiles) > 0:
					# we're on ground ; move faster
					self.xvel+=self.accel
				else:
					if self.behaviour!="PlayerControlled":
						# halve movement force
						self.xvel+=(self.accel * 0.89)
					else:
						self.xvel+=(self.accel * 0.949)
						
				self.lastpressed="right"
			
			# handle gun angle
			# this is a player controlled only behaviour
			if self.behaviour=="PlayerControlled":
				if self.moveleft and self.moveup:
					pass
					#self.gun.angle=225
					#self.gunImageDir="upleft"
				elif self.moveup and not self.moveleft and not self.moveright:
					# fire straight up
					self.gun.x=self.gunrect.centerx
					self.gun.y=self.gunrect.top
				
					self.gun.angle=270
				
					self.gunImageDir="up"
				elif self.moveright and self.moveup:
					pass
					#self.gun.angle=315
					#self.gunImageDir="upright"
				elif self.isJumping and self.KDIsDown:
					self.gun.angle=90
					self.gunImageDir="down"
					self.gun.x=self.gunrect.centerx
					self.gun.y=self.gunrect.bottom
				
			
				else:
					if self.lastpressed=="left":
						self.gun.angle=180
						self.gunImageDir="left"
						self.gun.x=self.gunrect.left
						self.gun.y=self.gunrect.centery
				
						self.gunImageDir="left"
					elif self.lastpressed=="right":
						self.gun.angle=0
						self.gun.x=self.gunrect.right
						self.gun.y=self.gunrect.centery
				
						self.gunImageDir="right"
					
			# add new textBar if display conditions met
			if not self.damagedDisplayed:
				# accumulate time
				self.shotAccWindowTime+=timepassed
			
				if self.shotAccWindowTime > self.waitTimeBforShowDmg:
					self.showHitDamage()
					self.accDamage=0
					self.damagedDisplayed=True
				
			# update textBarList
			for textBar in self.textBarList:
				textBar.update(timepassed)
			
			# clear dead textBar objects
			for textBar in self.textBarList:
				if not textBar.alive:
					self.textBarList.remove(textBar)
		
		
 		
			if self.shootingHeld:
				# fire gun
				self.gun.holdShooting=True
			else:	
				self.gun.holdShooting=False
		
		# if were not on a tile set isJumping to True
		if len(self.collidedTiles) > 0:
			self.isJumping=True
		
		# update owned objects
		self.gun.update(timepassed)
		self.gun.x=self.x
		self.gun.y=self.y
		
		# add gravity
		self.yvel+=self.gravity
		
		if self.yvel>self.maxyvel:
			self.yvel=self.maxyvel
		
		
		self.oldx=self.x
		self.oldy=self.y
		
		
		# update positions
		self.x+=self.xvel
		self.y+=self.yvel
		
		
		self.impXvel=self.x - self.oldx
		self.impYvel=self.y - self.oldy
		
		# damp velocities
		self.xvel *= self.friction
		
		self.rect.x=self.x
		self.rect.y=self.y
		# update gun rect
		if self.lastpressed=="left":
			self.gunrect.centerx=self.rect.centerx-3
		elif self.lastpressed=="right":
			self.gunrect.centerx=self.rect.centerx+3
			
		if self.gunImageDir=="up":
			self.gunrect.centery=self.rect.centery-2
		else:
			self.gunrect.centery=self.rect.centery+2
		
		self.colrect.center=self.rect.center
		
		# monitor hit points
		if self.behaviour=="PlayerControlled":
			if self.HP <=0:
				if not self.deadSet:
					self.moveleft=False
					self.moveright=False
					self.moveup=False
					self.gun.holdShooting=False
					self.frame=0
					self.deadSet=True
					
					self.isDead=True
		
		
			if self.isDead:
				self.updateframetime=1000/5
				self.isFiring=False
			
			
	def resolve45Deg(self,tile):
		pass
		
	
	def resolveBoxTile(self,tile):
		
		# check for collisions
		if self.rect.colliderect(tile.rect):
			# there is collision ; get axis penetration depths
			
			
			xdist= tile.rect.centerx - self.rect.centerx
			xpen = (tile.xw + self.xw) - abs(xdist)
			
			
			ydist= tile.rect.centery - self.rect.centery
			ypen = (tile.yw + self.yw) - abs(ydist)
			
			# find the smallest penetration
			minpen=min(xpen,ypen)
			
			if minpen==xpen:
				# project out along x axis
				if xdist > 0:
					if self.rect.bottom > tile.rect.top+2:		# this prevents catching push lefts/right when tiles are lined up next to each other
						# push left
						self.xvel=0
						#self.xvel-=abs(self.xvel)
						self.x=tile.rect.left - self.w
						#print "colliding left"
						
						if self.behaviour=="EnemyControlled":
							# add collision event notification for enemies ONLY
							self.eventNotifications.append("colLeft")
				else:
					if self.rect.bottom > tile.rect.top+2:
						#push right
						self.xvel=0
						#self.xvel+=abs(self.xvel)
						self.x=tile.rect.right
						#print "colliding right"
						
						if self.behaviour=="EnemyControlled":
							# add collision event notification for enemies ONLY
							self.eventNotifications.append("colRight")
					
			elif minpen==ypen:
				# project out along y axis
				# camera shake on landing if moving  fast enough
			
				if ydist > 0:
					if self.yvel> 1:
						#self.game.isShaking=True
						# add dust puff fx
						
						fxObject = AnimObject((self.rect.x-3,self.rect.y),self.game.puffObfxSheet,0,0)
						#fxObject.rect.center=(self.rect.centerx,self.rect.centery)
						self.game.gameObjectsList.append(fxObject)
						
						self.game.soundHandler.playSound(self.game.lnSnd)
						
						
					# push up
					self.isJumping=False
					self.yvel=0
					#self.yvel -= abs(self.yvel)
					self.y = tile.rect.top-(self.h-1)	# push up but leave 1px in tile
					self.collidedTiles.append(1)  # this list hold the number of tiles the player is on top of
					#print "colliding top"
					
					if self.behaviour=="EnemyControlled":
							# add collision event notification for enemies ONLY
							self.eventNotifications.append("colTop")
				else:
					#push down
					self.yvel=0
					self.y = tile.rect.bottom
					#print "colliding bottom"
					
					if self.behaviour=="EnemyControlled":
							# add collision event notification for enemies ONLY
							self.eventNotifications.append("colBottom")

class Enemy(AAB):
	def __init__(self,pos,kind,gameObject,w=16,h=16):
		super(Enemy,self).__init__(pos,gameObject,w,h)
		self.state = "None"
		self.type="troop"
		self.kind=kind	# two kinds so far; bloater,redman
		
		# low level actions
		self.isWandering=False
		self.isClimbing=False
		self.isFleeing=False
		self.isSeeking=False
		self.isFiring=False
		
		self.sightRange=4 # cell range the enemy can spot the player in
		self.jumpRangeX=3 # adjacent cells we check on either side to see if theyre jumpable
		self.jumpableTiles=[]
		self.targetTile=None
		
		self.blownUp=False		# one time flag for blowing up on death 
		
		self.behaviour="EnemyControlled"
		
		# some helpful AI vars
		# I know, I know my code is a tangled mess
		# redman's shit
		self.walkUpdateTime=5000
		self.timeSinceWalk=0
		self.walkHoldTime=500
		self.accWalkTime=0
		self.walkdir=random.choice(["left","right"])
		self.throwdir=None
		self.isCharging=False
		self.isExploding=False
		self.isWalking=False
		self.state="roam"
		self.touchDamage=5
		self.lastTimeSinceThrow=0
		self.throwWaitTime=700
		self.isThrowing=False
		self.swordSpeed=3.6
		
		self.accDropEggtime=0
		self.maxDropWaitTime=1000
		# init properties based on kind
		if self.kind!=None:
			
			self.anim=0
			self.frame=0
			
			self.fps=12
			self.acctime=0
			self.updateframetime=1000/self.fps
		
		if self.kind=="bloater":
			self.enemyMasterImgs=self.game.bloaterMasterImgs
			self.image=self.enemyMasterImgs[self.anim][self.frame]
			# i need to handle this gun changing thing properly
			self.gun.type="thrower"
			self.gun.fireUpdateTime=350
			
		elif self.kind=="redman":
			self.enemyMasterImgs=self.game.redmanMasterImgs
			self.image=self.enemyMasterImgs[self.anim][self.frame]
			self.walkUpdateTime=1100
			
		elif self.kind=="jumper":
			self.enemyMasterImgs=self.game.jumperMasterImgs
			self.image=self.enemyMasterImgs[self.anim][self.frame]
			self.jumpHeight=2.2
			self.accel=0.9
			self.friction=0.957
			self.gravity=0.14
			
		elif self.kind=="tramp":
			self.enemyMasterImgs=self.game.trampMasterImgs
			self.image=self.enemyMasterImgs[self.anim][self.frame]
			
			self.walkUpdateTime=1500
		
		elif self.kind=="madbat":
			self.enemyMasterImgs=self.game.madbatMasterImgs
			self.image=self.enemyMasterImgs[self.frame]
			self.gravity=0
		
		elif self.kind=="dandy":
			self.enemyMasterImgs=self.game.dandyMasterImgs
			self.image=self.enemyMasterImgs[self.frame]
			self.gun.type="rocket"
			self.gravity=0
		
		# handle enemy inputs
		self.movementToggledOff=True
		self.jumpPosReached=True
	
	def playAnim(self,timepassed):
		
		# manage animations based on kind
		# accumulate time
		self.acctime+=timepassed
		
		if self.kind=="madbat":
			if self.acctime > self.updateframetime:
				self.frame = (self.frame+1) % (len(self.enemyMasterImgs)-1) 
				self.acctime=0
		
		if self.kind=="dandy":
			if self.isFiring:
				self.frame = 1
			else:
				self.frame = 0
				
		
		
		if self.kind=="bloater":
			if not self.isFiring:
				if self.game.agents[0].x < self.x:
					# face left
					self.anim=0
					self.frame=0
				elif self.game.agents[0].x > self.x:
					self.anim=0
					self.frame=1
			
			elif self.isFiring:
				if self.game.agents[0].x < self.x:
					# play firing left anim
					self.anim=1
					if self.frame < len(self.enemyMasterImgs[self.anim])-1:
						# play the animation till its last frame then stop
						if self.acctime > self.updateframetime:
							self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
							self.acctime=0
				
				elif self.game.agents[0].x > self.x:
					# play firing left anim
					self.anim=2
					if self.frame < len(self.enemyMasterImgs[self.anim])-1:
						# play the animation till its last frame then stop
						if self.acctime > self.updateframetime:
							self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
							self.acctime=0
	
		elif self.kind=="redman":
			if self.isWalking and not self.isExploding:
				# get direction
				if self.walkdir=="left":
					self.anim=1
					# loop continuously while walking flag is True		
					if self.acctime > self.updateframetime:
						self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
						self.acctime=0
				
				elif self.walkdir=="right":
					self.anim=2
					# loop continuously while walking flag is True		
					if self.acctime > self.updateframetime:
						self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
						self.acctime=0
				
			if self.isCharging and not self.isExploding:
				# get direction
				if self.walkdir=="left":
					self.anim=3
					# loop continuously while walking flag is True		
					if self.acctime > self.updateframetime:
						self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
						self.acctime=0
				
				elif self.walkdir=="right":
					self.anim=4
					# loop continuously while walking flag is True		
					if self.acctime > self.updateframetime:
						self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
						self.acctime=0
			
			if not self.isWalking and not self.isCharging and not self.isExploding:
				if self.walkdir=="left":
					self.anim=0
					self.frame=0
				else:
					self.anim=0
					self.frame=1
			
			if self.isExploding:
				if self.walkdir=="left":
					self.anim=5
					
					if self.acctime > self.updateframetime:
						if self.frame < len(self.enemyMasterImgs[self.anim])-1:
							self.frame= (self.frame+1) 
							self.acctime=0
						
						else:
							
							# add explosion radius effect here
							fxObject = AnimObject((self.rect.centerx-32,self.rect.centery-32),self.game.explosionfxSheet,0,0,collidable=True,collisiontype="explosion")
							self.game.gameObjectsList.append(fxObject)
							
							fxEmitter=AnimEmitter((self.x,self.y),self.game.dustObfxSheet,numParticles=20,addParticleTime=0)
							fxEmitter.center=self.rect.center
							self.game.emitterList.append(fxEmitter)
							self.game.isShaking=True
							self.game.soundHandler.playSound(self.game.shoSnd)
							self.alive=False
							
				else:		
				
					# walkdir == right
					self.anim=6
					
					if self.acctime > self.updateframetime:
						if self.frame < len(self.enemyMasterImgs[self.anim])-1:
							self.frame= (self.frame+1) 
							self.acctime=0
						
						else:
							# add explosion radius effect here
							fxObject = AnimObject((self.rect.centerx-32,self.rect.centery-32),self.game.explosionfxSheet,0,0,collidable=True,collisiontype="explosion")
							self.game.gameObjectsList.append(fxObject)
							
							fxEmitter=AnimEmitter((self.x,self.y),self.game.dustObfxSheet,numParticles=20,addParticleTime=0)
							self.game.emitterList.append(fxEmitter)
							self.game.soundHandler.playSound(self.game.shoSnd)
							self.game.isShaking=True
							self.alive=False
							
							
		elif self.kind=="jumper":
			if self.isJumping:
				if self.walkdir=="left":
					if self.yvel<0:
						# going up
						self.anim=1
						self.frame=0
					else:
						# going down
						self.anim=1
						self.frame=2
						
				elif self.walkdir=="right":
					if self.yvel<0:
						# going up
						self.anim=1
						self.frame=1
					else:
						# going down
						self.anim=1
						self.frame=3
			
			else:
				if self.walkdir=="left":
					self.anim=0
					self.frame=0
				elif self.walkdir=="right":
					self.anim=0
					self.frame=1
		
		
		if self.kind=="tramp":
		
			
			if self.isWalking :
				# get direction
				if self.walkdir=="left":
					self.anim=1
					
					# loop continuously while walking flag is True		
					if self.acctime > self.updateframetime:
						self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
						self.acctime=0
				
				elif self.walkdir=="right":
					self.anim=2
					# loop continuously while walking flag is True		
					if self.acctime > self.updateframetime:
						self.frame= (self.frame+1) % len(self.enemyMasterImgs[self.anim])
						self.acctime=0
				
				
			elif self.isThrowing:
			
				if self.throwdir=="left":
					self.anim=4
					self.frame=1
				
					self.xvel+=3
					
					# throw anim object that has a single knife frame ;its a single image in a list
					fxObject = AnimObject((self.rect.centerx,self.rect.centery),[self.game.trampswordSheet[0]],-self.swordSpeed,0,numLoops=-1,friction=1,collidable=True,collisiontype="sword")
					self.game.gameObjectsList.append(fxObject)
					#self.game.isShaking=True
						
					# reset lastTimeSinceThrow
					self.lastTimeSinceThrow=0
					self.isThrowing=False
							
				elif self.throwdir=="right":
					self.anim=5
					self.frame=1
					
					# for some freaky reason i cant manipulate yvel in this block somehow
					self.xvel-=3
					
					# throw anim object that has a single knife frame ;its a single image in a list
					fxObject = AnimObject((self.rect.centerx,self.rect.centery),[self.game.trampswordSheet[1]],self.swordSpeed,0,numLoops=-1,friction=1,collidable=True,collisiontype="sword")
					self.game.gameObjectsList.append(fxObject)
					self.game.isShaking=True
					
					# reset lastTimeSinceThrow
					self.lastTimeSinceThrow=0
					self.isThrowing=False
					
			else:
				if self.walkdir=="left":
					self.anim=0
					self.frame=0
				else:
					self.anim=0
					self.frame=1
			
	
	def dropEgg(self):
		if self.accDropEggtime > self.maxDropWaitTime:
			fxObject = AnimObject((self.rect.centerx,self.rect.centery),[self.game.egggImage],0,2.8,numLoops=-1,friction=1.025,collidable=True,collisiontype="egg")
			self.game.gameObjectsList.append(fxObject)
			self.accDropEggtime=0
	
	def throwKnife(self,dir):
		
		
		if self.lastTimeSinceThrow>self.throwWaitTime:
			# throw knife here
			self.throwdir=dir

			self.isThrowing=True 	# this flag trigger the throwing anim; when it ends set is throwing to false and launch a projectile
		# and reset lastTimeSinceThrow to 0 when done
			self.yvel-=0.6
			# remember to do the animation shit
	def walk(self):
	
		if self.accWalkTime<self.walkHoldTime:
			if self.walkdir == "left":
				self.moveleft=True
			elif self.walkdir == "right":
				self.moveright=True
		else:
			self.moveleft=False
			self.moveright=False
			# only reset timeSinceWalk to 0 whan we finish walking
			self.accWalkTime=0  	# this must be reset here too
			self.timeSinceWalk=0
			self.isWalking=False
			
	
	def charge(self):
		if self.isCharging:
			# charge in direction of player until wall is hit
			# then switch back to roam
			self.accel=self.chargeaccel 	# speed up
			
			# test hop if player is jumping
			#if self.game.agents[0].isJumping:
			#	self.jump()
			
			if self.walkdir=="left":
				self.moveleft=True
				self.moveright=False
			elif self.walkdir == "right":
				self.moveright=True
				self.moveleft=False
		
	def update(self,timepassed):
	
		super(Enemy,self).update(timepassed)
		
		
		
		if self.HP<=0:
			if self.kind != "redman":
				# add explosion particles
				fxEmitter=AnimEmitter((self.x,self.y),self.game.dustObfxSheet,numParticles=20,addParticleTime=0)
				self.game.emitterList.append(fxEmitter)
				self.game.soundHandler.playSound(self.game.shoSnd)	
				self.alive=False
			
			else:
				# redman ; play his explosion animation the kill him
				self.isExploding=True
				self.state=None
				self.moveleft=False
				self.moveright=False
				self.isCharging=False
				self.isWalking=False
				self.updateframetime=1000/6
				
				
		# handle queued up events
		for event in self.eventNotifications:
			if event=="colLeft":
				if self.kind != "jumper":
					if self.kind=="tramp":
						pass
					self.walkdir="left"
				
				if self.isCharging:
					self.state="roam"
					self.accel=self.normaccel 	# revert back to normaccel
					self.isCharging=False
					
			if event=="colRight":
				if self.kind != "jumper":
				
					if self.kind == "tramp":
						pass
				
					self.walkdir="right"
				if self.isCharging:
					self.state="roam"
					self.accel=self.normaccel 	# revert back to normaccel
					self.isCharging=False
				
				
		self.eventNotifications=[]
		
		if self.kind=="redman":
			if not self.isWalking:
				# accumulate timeSinceWalk only when NOT walking
				self.timeSinceWalk+=timepassed
			else:
				# accumulate walk time only when walking
				self.accWalkTime+=timepassed
		
			if self.state=="roam":
				if self.timeSinceWalk > self.walkUpdateTime:
					
					self.isWalking=True
					self.walk()
					
			elif self.state=="charge":
				self.isCharging=True
				self.charge()
		
		if self.kind=="tramp":
			if not self.isWalking:
				# accumulate timeSinceWalk only when NOT walking
				self.timeSinceWalk+=timepassed
			else:
				# accumulate walk time only when walking
				self.accWalkTime+=timepassed
		
			if self.state=="roam":
				if self.timeSinceWalk > self.walkUpdateTime:
					
					self.isWalking=True
					self.walk()
			
			elif self.state=="throw":
				self.lastTimeSinceThrow+=timepassed
		
		self.playAnim(timepassed)
		
		if self.kind!=None and (self.kind!= "madbat" and self.kind!= "dandy"):
			self.image=self.enemyMasterImgs[self.anim][self.frame]
		
		if self.kind=="madbat":
			self.image=self.enemyMasterImgs[self.frame]
			self.accDropEggtime+=timepassed
		
		if self.kind=="dandy":
			self.image=self.enemyMasterImgs[self.frame]
		
	def draw(self,Surface):
		super(Enemy,self).draw(Surface)
	
			
		if self.kind != None :
			Surface.blit(self.image,self.rect)
	
	def decideState(self):
		# if close to the player , fire at him
		for agent in self.game.agents:
			# get agent's cell coords
			agentCellX,agentCellY = self.game.getCellCoords(agent.x,agent.y) 
			# get current enemy's cell coords
			selfCellX,selfCellY = self.game.getCellCoords(self.x,self.y)
			
			if self.kind=="madbat":
				# check if its within sightRange
				if agentCellX in range(selfCellX - 1,selfCellX + 1) \
				and agentCellY in range(selfCellY,selfCellY + 8): 
					# player in sight ; drop egg on him
					print "drop egg"
					self.dropEgg()
			
			
			if self.kind=="bloater":
				# check if its within sightRange
				if agentCellX in range(selfCellX - (self.sightRange+3),selfCellX + (self.sightRange+3)) \
				and agentCellY in range(selfCellY - self.sightRange,selfCellY + self.sightRange): 
					# player in sight ; set isFiring state to True
					self.isFiring=True
				else:
					self.isFiring=False
			
			elif self.kind=="dandy":
				# check if its within sightRange
				if agentCellX in range(selfCellX - (self.sightRange+3),selfCellX + (self.sightRange+3)) \
				and agentCellY in range(selfCellY - (self.sightRange+3),selfCellY + (self.sightRange+3)): 
					# player in sight ; set isFiring state to True
					self.isFiring=True
				else:
					self.isFiring=False
			
			
			elif self.kind=="redman":
				# if player is in range ; charge at him ,else roam
				if agentCellX in range(selfCellX - (self.sightRange+1),selfCellX + (self.sightRange+1)) \
				and agentCellY == selfCellY and not self.isExploding:
					if agent.x>self.x:
						self.walkdir="right"
					else:
						self.walkdir="left"
						
					self.state="charge"
			
			elif self.kind=="tramp":
				# if player is in range ; charge at him ,else roam
				if agentCellX in range(selfCellX - (self.sightRange+4),selfCellX + self.sightRange+4) \
				and agentCellY == selfCellY:
					if agent.x>self.x:
						self.state="throw"
						self.throwKnife("right")
						
					else:
						self.throwKnife("left")
						self.state="throw"
						
						
				else:
					self.state="roam"
			
			elif self.kind=="madbat":
				if self.walkdir=="left":
					self.moveleft=True
					self.moveright=False
				elif self.walkdir=="right":
					self.moveright=True
					self.moveleft=False
			
			elif self.kind=="jumper":
				# if player is in range ; charge at him ,else roam
				if agentCellX in range(selfCellX - (self.sightRange+2),selfCellX + (self.sightRange+2)) \
				and agentCellY in range(selfCellY -3,selfCellY+2):
					if agent.x>self.x:
						self.jump()
						self.xvel+=0.2
						self.walkdir="right"
					else:
						self.jump()
						self.xvel-=0.2
						self.walkdir="left"
					
			
			
		'''		
		if len(self.collidedTiles) > 0:
			self.isWandering=True
		else:
			self.isWandering=False
		'''
		
	def Act(self):
		# define actions to take based on current state
		if self.isFiring:
			# set gun to fire
			# set gun angle
			playerEnemyVectorX = self.game.agents[0].x - self.x
			playerEnemyVectorY = (self.game.agents[0].y-10) - self.y # fire a little higher than the target
			
			self.gun.angle = int(math.atan2(playerEnemyVectorY,playerEnemyVectorX) * (180/math.pi))
			self.shootingHeld=True		
		else:
			self.shootingHeld=False
		
		if self.isWandering:
			# set movementToggledOff to False
			self.movementToggledOff=False
			# move left and right if standing on a block
			if self.walkdir==0:
				self.moveleft=True
				self.moveright=False
			elif self.walkdir==1:
				self.moveleft=False
				self.moveright=True
			
			# choose random direction to walk to
			if self.walkdir == None:
				self.walkdir=random.randint(0,1)
			else: 
				if self.walkdir==0:
					# move left if possible
					# check left rect extremity tile position
					# if its in an empty tile underneath the enemy : change direction
					selfCellX,selfCellY = self.game.getCellCoords(self.rect.left,self.y)
					if self.game.map[selfCellY + 1][selfCellX] == ".":
						# ground footing is empty ; change dir
						self.walkdir=1
				
				elif self.walkdir==1:
					# move right if possible
					# check right rect extremity tile position
					# if its in an empty tile underneath the enemy : change direction
					selfCellX,selfCellY = self.game.getCellCoords(self.rect.right,self.y)
					if self.game.map[selfCellY + 1][selfCellX] == ".":
						# ground footing is empty ; change dir
						self.walkdir=0
		
		else:
			# set walking movements to False
			if not self.movementToggledOff:
				self.moveleft=False
				self.moveright=False
				self.movementToggledOff=True
			
		if self.isClimbing:
			# check for tiles you can jump on within your range
			# do this by checking if each tile in your vicinity has at least one empty cell above it
			# within your jumping range
			
			# get current enemy's cell coords
			selfCellX,selfCellY = self.game.getCellCoords(self.x,self.y)
			# reset jumpableTiles list
			self.jumpableTiles=[]
			
			# get possible jumpable tiles from map in self range
			for row in range(selfCellY-1 ,selfCellY+1):
				for col in range(selfCellX-self.jumpRangeX,selfCellX + self.jumpRangeX):
					if self.game.map[row][col] !="." :
						# check the tile above it
						# if its empty append it to jumpable tiles list
						if self.game.map[row-1][col]==".":
							# its empty
							self.jumpableTiles.append((col,row-1))
							break
				break
				
			# prune list so it only contains 1 target at a time
			if len(self.jumpableTiles) >1:
				del self.jumpableTiles[1:]
			
				
			# jump if there is a reachable tile
			if len(self.jumpableTiles) >0 and self.jumpPosReached:
				self.targetTile = self.jumpableTiles[0]
				
				self.jumpPosReached=False
			
			if self.targetTile != None:
				self.jumpTo(self.targetTile)
			
			#print self.jumpableTiles
	
	def jumpTo(self,tileCoords):
		cellX,cellY = tileCoords
		selfCellX,selfCellY = self.game.getCellCoords(self.x,self.y)
		TILESIZE=self.game.TILESIZE
		
		if not self.jumpPosReached:
		
			# get to the left or right of target tile
			# decide if we're moving left or right
			if selfCellX < cellX:
				# moveright
				if self.x < cellX * self.game.TILESIZE:
					self.moveright=True
			
			elif selfCellX > cellX:
				# moveleft
				if self.x > cellX * self.game.TILESIZE:
					self.moveleft=True
			
			
			self.jump()
			if self.x + self.xw < (cellX * TILESIZE) + TILESIZE/2 and selfCellY != cellY-1:
				
				self.moveright=True
				self.moveleft=False
			elif self.x + self.xw > (cellX * TILESIZE) + TILESIZE/2 and selfCellY != cellY-1:
				self.moveleft=True
				self.moveright=False
			else:
				self.jumpPosReached=True
				self.targetTile=None
				self.moveleft=False
				self.moveright=False

class FlyingCreature(object):
	def __init__(self,pos,gameObject,w=16,h=16):
		self.x,self.y=pos
		self.alive=True
		self.health=100
		self.type="flyer"
		
		self.dir="left"
		
		self.accel=0.04
		self.xvel=0.0
		self.yvel=0.0
		self.gravity=0.06
		self.maxyvel=3.0
		self.maxFlapYvel=1.5
		self.maxflapWaitTime=400
		self.flapWaitTime=400
		self.flapStrength=4.2
		self.friction=0.947
		
		self.aiEvents=[]
		self.isFlapping=False
		self.states=["wander","seekPerch","attack"]
		self.state="wander"
		self.currentAction=None
		self.radius=8
		self.rect = pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
	
	def draw(self,Surface):
		pygame.draw.circle(Surface,WHITE,(self.x,self.y),self.radius)
		pygame.draw.rect(Surface,RED,self.rect)
	def flap(self):
		if not self.isFlapping:
			self.isFlapping=True
			self.flapWaitTime=0
			self.yvel-=self.flapStrength
	
	def move(self):
	
		if self.dir =="left":
			self.xvel-= self.accel
		elif self.dir =="right":
			self.xvel+= self.accel
			
	def Act(self):
		if self.state =="wander":
			# DEFINE BEHAVIOUR ALGORITHM FOR WANDER STATE
			if self.yvel > self.maxFlapYvel:
				self.flap()
			
			for event in self.aiEvents:
				if event == "turnleft":
					self.xvel *= -1
					self.dir="left"
				if event == "turnright":
					self.xvel *= -1
					self.dir="right"
					
				self.aiEvents=[]
				
	def update(self,timepassed):
		self.flapWaitTime+=timepassed
		
		self.move()
		
		if self.flapWaitTime > self.maxflapWaitTime:
			self.isFlapping=False
		
		if self.yvel> self.maxyvel:
			self.yvel=self.maxyvel
			
		self.yvel += self.gravity
		
		self.x += self.xvel
		self.y += self.yvel
		
		self.rect.x= self.x-self.radius
		self.rect.y= self.y-self.radius
		
		self.xvel *= self.friction
		
	def getCollisonInfo(self,tile):
		
		if self.x < tile.rect.centerx and self.y in range(tile.rect.top-self.radius,tile.rect.bottom+self.radius):
			self.aiEvents.append("turnleft")
			
		elif self.x > tile.rect.centerx and self.y in range(tile.rect.top-self.radius,tile.rect.bottom+self.radius):
			self.aiEvents.append("turnright")
	
			
		if self.y < tile.rect.centery :#and self.x in range(tile.rect.left,tile.rect.right):
			self.y = self.rect.top - self.radius
			#self.yvel *= -0.1
			#print "this runs at least"
		elif self.y > tile.rect.centery :#and self.x in range(tile.rect.left,tile.rect.right):
			self.y = self.rect.bottom + (self.radius)
			#self.yvel *= -0.1
			#print "this runs at least down"


class Bullet(object):
	def __init__(self, pos, owner, xvel=1.0, yvel=1.0, type="basic"):
		self.x,self.y=pos
		self.yvel= yvel
		self.xvel= xvel
		self.gravity=0.0
		self.accel=0.2
		self.lifetime=0
		self.alive=True
		self.color=(255,255,255)
		self.type=type
		self.radius=2
		self.friction=1
		self.bounceDecay = 0.98
		self.maxyvel=2.0
		self.maxxvel=3.0
		self.maxLiveTime=1300
		self.destroyercolors=[(255,255,255),(220,200,10),(30,30,30)]
		self.basiccolors=[(255,255,255),(10,150,255),(30,30,30)]
		self.colorID=0
		self.factor=0.0
		self.lerpSpeed=0.05
		self.isLerping=True
		self.gunOwner=owner
		self.rocketOrientation=0
		
		self.bsize=6.0
		self.bwidth=9.0
		self.bulletDamage=3
		
		if self.type=="basic":
			self.color=(0,255,20)
			self.bulletrect=pygame.Rect(self.x+self.radius,self.y+self.radius,self.radius*2,self.radius*2)
			
		elif self.type=="destroyer":
			self.color=(255,0,0)
			self.bulletrect=pygame.Rect(self.x-self.bsize,self.y-self.bsize,6,4)
			
		elif self.type=="thrower":
			self.image=self.gunOwner.game.bloaterBulletImg
			self.color=(10,150,200)
			self.radius=3
			self.gravity=0.099
			self.friction=0.957
			self.accel=0.8
			self.bulletrect=pygame.Rect(self.x,self.y,8,8)
		
		elif self.type=="rocket":
			self.image=self.gunOwner.game.rocketBulletImg
			self.imageToBlit=self.gunOwner.game.rocketBulletImgBlit
			self.radius=3
			#self.yvel=self.xvel=0
			self.gravity=0.0
			self.friction=1
			self.accel=0.8
			self.bulletrect=self.image.get_rect()
			self.bulletrect.center=(self.x,self.y)
			self.maxLiveTime=6000
			
		elif self.type=="bouncer":
			self.color=(210,150,20)
			self.radius=2
			self.gravity=0.099
			self.friction=0.99
			
		
	def update(self,timepassed,game):
		
		if not self.type=="rocket":
			self.xvel *= self.friction
			self.yvel += self.gravity
		
		if self.type=="destroyer":
			if self.bsize>2:
				self.bsize-=0.4
			
			if self.bwidth>4:
				self.bwidth-=1.1
		
		elif self.type=="basic":
			if self.radius <9:
				self.radius+=0.19
		
		if self.yvel > self.maxyvel:
			self.yvel=self.maxyvel
		
		# integrate position
		self.x += self.xvel
		self.y += self.yvel
		
		if self.type=="rocket":
			# calculate angle between player and rocket
			player=game.agents[0]
			
			# was trying for something different but got a usable effect
			# makes shit floaty around the player
			angle = math.atan2(player.rect.centery-self.bulletrect.centery,player.rect.centerx-self.bulletrect.centerx)
			self.rocketOrientation = angle *(180/math.pi)
			self.xvel = 1.3 * math.cos(angle) #*(math.pi/180))
			self.yvel = 1.1 * math.sin(angle) #*(math.pi/180))
			#self.xvel *= self.friction
			#self.yvel *= self.friction
			
		# update collision rectangles
		if self.type=="basic" :
			
			self.bulletrect.center=(self.x,self.y)
			self.bulletrect.w=self.radius*2
			self.bulletrect.h=self.radius*2
			
		elif self.type=="destroyer":
			self.bulletrect.center=(self.x,self.y)
		
		elif self.type=="thrower":
			self.bulletrect.center=(self.x,self.y)
		
		elif self.type=="rocket":
			self.image=pygame.transform.rotate(self.imageToBlit,self.rocketOrientation)
			self.image.convert_alpha()
			self.bulletrect=self.image.get_rect()
			self.bulletrect.center=(self.x,self.y)
	
		
		# accumulate lifetime
		if self.alive:
			self.lifetime += timepassed
		
		if self.type=="basic" or self.type=="destroyer" or self.type=="thrower" or self.type=="rocket":
			# get bullet cell coords
			#bulletCellX,bulletCellY = game.getCellCoords(self.x,self.y)
			
			for tile in game.collidableTiles:
				#if tile.cellX in range(bulletCellX-1,bulletCellX+1) and \
				#tile.cellY in range(bulletCellY-1,bulletCellY+1):
					
				if tile.rect.colliderect(self.bulletrect):
					# create fx animated object
					fxObject = AnimObject((self.x,self.y),game.hitfxSheet,0,0)
					game.gameObjectsList.append(fxObject)
					
					if self.gunOwner.behaviour=="PlayerControlled":
						# hit destructable tile
						if tile.type=="destructable":
							tile.HP-=1
							#game.isShaking=True
							fxEmitter=AnimEmitter(tile.rect.center,game.tileblowfxSheet)
							game.emitterList.append(fxEmitter)
							game.soundHandler.playSound(game.httSnd)
						
					self.alive=False
			
			if self.gunOwner.behaviour=="PlayerControlled":
				for enemy in game.enemyObjects:	
					if enemy.rect.colliderect(self.bulletrect):
						# reset the object's textBar variables
						enemy.shotAccWindowTime=0
						enemy.accDamage+=self.bulletDamage
						enemy.HP-=self.bulletDamage
						enemy.damagedDisplayed=False
					
						# create fx animated object
						fxObject = AnimObject((self.x,self.y),game.hitObfxSheet,0,0)
						game.gameObjectsList.append(fxObject)
						
						# play sound
						game.soundHandler.playSound(game.hrtSnd)
						
						self.alive=False
			
			
			elif self.gunOwner.behaviour=="EnemyControlled":
				for agent in game.agents:	
					if agent.colrect.colliderect(self.bulletrect):
						# reset the object's textBar variables
						agent.shotAccWindowTime=0
						# accumulate damaged
						
						agent.accDamage += self.bulletDamage
						
						agent.damagedDisplayed=False
					
					
						# create fx animated object
						if not agent.isDead:
							agent.HP-=self.bulletDamage
							fxObject = AnimObject((self.x,self.y),game.hitObfxSheet)
							game.gameObjectsList.append(fxObject)
							
							game.soundHandler.playSound(game.owSnd)
						self.alive=False
			
					
			if self.lifetime > self.maxLiveTime:
				self.alive=False
					
		
		if self.type=="destroyer":
			# lerp colors
			if self.isLerping:
				self.factor+=self.lerpSpeed
				
				if self.factor >=1:
					if self.colorID==len(self.destroyercolors)-2:
						self.isLerping=False
					else:
						self.colorID+=1
						self.factor=0.0
			# lerp
			self.color=game.lerp(self.destroyercolors[self.colorID],self.destroyercolors[self.colorID+1],self.factor)
		
		if self.type=="basic":
			# lerp colors
			if self.isLerping:
				self.factor+=self.lerpSpeed
				
				if self.factor >=1:
					if self.colorID==len(self.destroyercolors)-2:
						self.isLerping=False
					else:
						self.colorID+=1
						self.factor=0.0
			# lerp
			self.color=game.lerp(self.basiccolors[self.colorID],self.basiccolors[self.colorID+1],self.factor)
		
		
		elif self.type == "bouncer":
			for tile in game.collidableTiles:
				if tile.rect.collidepoint(self.x,self.y):
					# calculate bounce direction based on points distance from center
					xdist = tile.rect.centerx - self.x
					ydist = tile.rect.centery - self.y
					# get min distance
					penDist = min(xdist,ydist)
					
					if penDist == xdist:
						
						# reverse velocity on x axis 
						self.xvel *= -1
						
					elif penDist == ydist:
						
						# reverse velocity on y axis
						self.yvel = -(self.yvel * self.bounceDecay) 
		
		
			
		
	def draw(self,Surface):
		if self.type=="basic":
			pygame.draw.circle(Surface,self.color,(self.x,self.y),self.radius,1)
		
		if self.type=="destroyer":
			pygame.draw.line(Surface,self.color,(self.x-self.bsize,self.y),(self.x+self.bsize,self.y),self.bwidth)
		
		if self.type=="thrower" or self.type=="rocket":
			Surface.blit(self.image,self.bulletrect)
		
		
		
		# draw collision rect debug
		#pygame.draw.rect(Surface,(0,30,200),self.bulletrect)
		
class GunEmitter(object):
	def __init__(self,pos,gameObject,owner,type="basic"):
		# gun types : basic ,thrower, rocket, destroyer, bouncer
	
		self.x,self.y=pos
		self.type = type
		self.holdShooting=False
		self.fireUpdateTime=200			# time in ms that has to pass before new bullet is spawned
		self.accBulletTime=0			# time since last bullet spawning
		self.angle=180
		self.maxBulletSpeed=6
		self.game=gameObject
		self.owner=owner
		
		self.bulletsList=[]
		
		if self.type=="bouncer":
			# halve maxBulletSpeed
			self.maxBulletSpeed /=2
		
		elif self.type == "destroyer":
			self.fireUpdateTime = 160
			
		elif self.type == "thrower":
			self.fireUpdateTime = 250
		
		elif self.type == "rocket":
			self.fireUpdateTime = 10000
		
	def update(self,timepassed):
	
		# accumulate time
		self.accBulletTime += timepassed
		
		# update all bullets
		for bullet in self.bulletsList:
			bullet.update(timepassed,self.game)
				
		# clear dead bullets from bulletsList
		for bullet in self.bulletsList:
			if not bullet.alive:
				self.bulletsList.remove(bullet)
		
		if self.type=="basic" or self.type=="destroyer" or self.type=="thrower" or self.type=="bouncer" :
			if self.holdShooting:
				# fire bullet particles
				if self.accBulletTime > self.fireUpdateTime:
					if self.owner.behaviour=="PlayerControlled":
						#self.game.isShaking=True
						self.game.soundHandler.playSound(self.game.g2Snd)
						
					# reset accumulated times
					self.accBulletTime=0
					# spawn new bullet and add it to bulletsList
					# fire it in a specific direction
					if self.type=="destroyer":
						# calculate bullet direction vector
						angleRange= random.randint(self.angle-11,self.angle+11)
						bulletXvel = math.cos((angleRange * math.pi/180)) * self.maxBulletSpeed
						bulletYvel = math.sin((angleRange * math.pi/180)) * self.maxBulletSpeed
						# add gun kick in reverse firing direction
						self.owner.xvel += -bulletXvel * 0.07
						self.owner.yvel += -bulletYvel * 0.07
						
					else:
						# calculate bullet direction vector
						bulletXvel = math.cos((self.angle * math.pi/180)) * self.maxBulletSpeed
						bulletYvel = math.sin((self.angle * math.pi/180)) * self.maxBulletSpeed
						# add gun kick in reverse firing direction
						self.owner.xvel += -bulletXvel * 0.2
						self.owner.yvel += -bulletYvel * 0.2
						
					newBullet = Bullet((self.x,self.y),self.owner,bulletXvel,bulletYvel,self.type)
					self.bulletsList.append(newBullet)
		
		if self.type=="rocket": 
			if self.holdShooting:
				# fire bullet particles
				if self.accBulletTime > 800:
					if self.owner.behaviour=="PlayerControlled":
						#self.game.isShaking=True
						self.game.soundHandler.playSound(self.game.g2Snd)
						
					# reset accumulated times
					self.accBulletTime=0
					newBullet = Bullet((self.x,self.y),self.owner,0,0,self.type)
					self.bulletsList.append(newBullet)
					
			
	def draw(self,Surface):
		for bullet in self.bulletsList:
			bullet.draw(Surface)
		
class Door(object):
	def __init__(self,pos,gameObject):
		self.x,self.y = pos
		self.game = gameObject
		self.state="closed"
		self.frame=16
		self.imageList=self.game.tileSheet
		self.image=self.imageList[self.frame]
		self.rect=self.image.get_rect()
		self.rect.topleft=(self.x,self.y)
		self.openPlayedSnd=False
		
	def update(self,timepassed):
		if len(self.game.enemyObjects)<=0:
			self.state="open"
			self.frame=17
			if not self.openPlayedSnd:
				self.game.soundHandler.playSound(self.game.enSnd)
				self.openPlayedSnd=True
				
		else:
			self.state="closed"
			self.frame=16
			
		self.image = self.imageList[self.frame]
		
	def draw(self,Surface):
	
		Surface.blit(self.image,self.rect)
	
