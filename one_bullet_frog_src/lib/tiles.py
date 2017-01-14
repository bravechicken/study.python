import pygame,sys,math,random
from pygame.locals import*
from globals import*
from gameobjects import*

class BoxTile(object):
	def __init__(self,pos,gameObject,orientation="UP",w=64,h=64,kind="grass"):
		self.x,self.y=pos
		self.w=w
		self.h=h
		
		self.game=gameObject
		self.orientation=orientation
		self.imglist=self.game.tileSheet
		self.xw = w/2
		self.yw = h/2
		self.type="normal"
		self.frame=0
		
		
		if self.orientation=="UP":
			if kind=="grass":
				self.frame=0
			elif kind=="redearth":
				self.frame=10
		elif self.orientation=="DOWN":
			if kind=="grass":
				self.frame=1
			elif kind=="redearth":
				self.frame=11
		elif self.orientation=="MID":
			if kind=="grass":
				self.frame=2
			elif kind=="redearth":
				self.frame=12
		
		self.image = self.imglist[self.frame]  
		
		self.cellX,self.cellY = self.game.getCellCoords(self.x,self.y)
		
		self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
		
	def draw(self,Surface):
		Surface.blit(self.image,self.rect)
		
	def update(self,timepassed):
		self.rect.x=self.x
		self.rect.y=self.y
		
class LaserTile(BoxTile):
	def __init__(self,pos,gameObject,orientation="UP",w=64,h=64):
		super(LaserTile,self).__init__(pos,gameObject,orientation,w,h)
		
		self.orientation=orientation
		
		self.type="laser"
		if self.orientation=="LEFT":
			self.frame=3
		elif self.orientation=="UP":
			self.frame=4
		elif self.orientation=="RIGHT":
			self.frame=5
		elif self.orientation=="DOWN":
			self.frame=6
		
		self.image = self.imglist[self.frame]  
		
		self.laserRect=None
		self.laserBeginPoint=None
		self.laserEndPoint=None
		
		self.laserDamage=10
		
		self.colors=[(255,0,29),(255,255,255),(0,230,10)]
		self.colorID=0
		
		self.isReadyToFire=False
		self.isFiring=False
		
		# give it a random starting values to give the lasers some unpredictability
		self.accFireTime=random.randint(100,3000) 
		
		self.updateFireTime=5000
		self.heldReadyAccTime=0
		self.readyToFireHoldTime=1000
		self.firingHeldTime=0
		self.maxFiringTime=2000
		
	def getLaserEnd(self,cellX,cellY):
		# runs through board to check tiles adjacent to itself based on orientation
		if self.orientation=="LEFT":
			startCellX = cellX-1
			for i in range(cellX+40):
				if self.game.map[cellY][startCellX] in self.game.tileIdentifiers:
					return (startCellX,cellY)
					
				startCellX-=1
					
		elif self.orientation=="RIGHT":
			startCellX = cellX+1
			for i in range(cellX+40):	# the +30 here is hacky so I force return a value before exiting the loop
				if self.game.map[cellY][startCellX] in self.game.tileIdentifiers:
					return (startCellX,cellY)
					
				startCellX+=1
		
		elif self.orientation=="UP":
			startCellY = cellY-1
			for i in range(cellY+40):
				if self.game.map[startCellY][cellX] in self.game.tileIdentifiers:
					return (cellX,startCellY)
					
				startCellY-=1
		
		elif self.orientation=="DOWN":
			startCellY = cellY+1
			for i in range(cellY+40):
				if self.game.map[startCellY][cellX] in self.game.tileIdentifiers:
					return (cellX,startCellY)
					
				startCellY+=1
		
	def setState(self):
		"""Call this before running the main game loop as part of initialisation"""
		TILESIZE = self.game.TILESIZE
		
		if self.orientation=="LEFT":
			self.laserEndPoint=(self.rect.left,self.rect.centery)
			tempCellX,tempCellY = self.getLaserEnd(self.cellX,self.cellY)
			endXcoords = (tempCellX * TILESIZE) + TILESIZE
			self.laserBeginPoint=(endXcoords,self.rect.centery)
			
			# create the lasers rect
			w = abs(self.laserEndPoint[0]-self.laserBeginPoint[0])
			h = 5
			self.laserRect=pygame.Rect(self.laserBeginPoint[0],self.laserBeginPoint[1],w,h)
			self.laserRect.centery=self.rect.centery
			
		elif self.orientation=="RIGHT":
			self.laserBeginPoint=(self.rect.right,self.rect.centery)
			
			tempCellX,tempCellY = self.getLaserEnd(self.cellX,self.cellY)
			endXcoords = (tempCellX * TILESIZE)
			
			self.laserEndPoint=(endXcoords,self.rect.centery)
			
			# create the lasers rect
			w = abs(self.laserEndPoint[0]-self.laserBeginPoint[0])
			h = 5
			self.laserRect=pygame.Rect(self.laserBeginPoint[0],self.laserBeginPoint[1],w,h)
			self.laserRect.centery=self.rect.centery
			
		elif self.orientation=="UP":
			self.laserEndPoint=(self.rect.centerx,self.rect.top)
			tempCellX,tempCellY = self.getLaserEnd(self.cellX,self.cellY)
			endYcoords = (tempCellY * TILESIZE) + TILESIZE
			self.laserBeginPoint=(self.rect.centerx,endYcoords)
		
			# create the lasers rect
			w = 5
			h = abs(self.laserEndPoint[1]-self.laserBeginPoint[1])
			self.laserRect=pygame.Rect(self.laserBeginPoint[0],self.laserBeginPoint[1],w,h)
			self.laserRect.centerx=self.rect.centerx
			
		elif self.orientation=="DOWN":
			
			self.laserBeginPoint=(self.rect.centerx,self.rect.bottom)
			tempCellX,tempCellY = self.getLaserEnd(self.cellX,self.cellY)
			endYcoords = (tempCellY * TILESIZE)
			self.laserEndPoint=(self.rect.centerx,endYcoords)
			
			# create the lasers rect
			w = 5
			h = abs(self.laserEndPoint[1]-self.laserBeginPoint[1])
			self.laserRect=pygame.Rect(self.laserBeginPoint[0],self.laserBeginPoint[1],w,h)
			self.laserRect.centerx=self.rect.centerx
			
	def update(self,timepassed):
		super(LaserTile,self).update(timepassed)
		
		self.colorID =(self.colorID+1) % len(self.colors)
		
		if not self.isReadyToFire or not self.isFiring:
			self.accFireTime+=timepassed
		
			if self.accFireTime>self.updateFireTime:
				self.isReadyToFire=True
				self.accFireTime=0
				#self.game.soundHandler.playSound(self.game.lacSnd)
			
		if self.isReadyToFire:
			self.heldReadyAccTime+=timepassed
			
			if self.heldReadyAccTime> self.readyToFireHoldTime:
				self.heldReadyAccTime=0
				self.isReadyToFire=False
				self.isFiring=True
				self.game.soundHandler.playSound(self.game.lafSnd)
				
				
				
		if self.isFiring:
			self.firingHeldTime+=timepassed
				
			if self.firingHeldTime>self.maxFiringTime:
				self.firingHeldTime=0
				self.isFiring=False
				# attach some fx where the beam hits
				
				if self.orientation=="LEFT":
					fxEmitter=AnimEmitter((self.laserRect.left,self.laserRect.centery),self.game.dustObfxSheet)
				elif self.orientation=="RIGHT":
					fxEmitter=AnimEmitter((self.laserRect.right,self.laserRect.centery),self.game.dustObfxSheet)
				elif self.orientation=="UP":
					fxEmitter=AnimEmitter((self.laserRect.centerx,self.laserRect.top),self.game.dustObfxSheet)
				elif self.orientation=="DOWN":
					fxEmitter=AnimEmitter((self.laserRect.centerx,self.laserRect.bottom),self.game.dustObfxSheet)
				
				
				self.game.emitterList.append(fxEmitter)
					
					
	def draw(self,Surface):
		super(LaserTile,self).draw(Surface)
		
		# draw the laser
		if self.isFiring:
			pygame.draw.rect(Surface,self.colors[self.colorID],self.laserRect)
		
		if self.isReadyToFire:
			if self.orientation=="LEFT" or self.orientation=="RIGHT":
				pygame.draw.line(Surface,RED,(self.laserRect.left,self.laserRect.centery),(self.laserRect.right,self.laserRect.centery),1)
			
			elif self.orientation=="UP" or self.orientation=="DOWN":
				pygame.draw.line(Surface,RED,(self.laserRect.centerx,self.laserRect.top),(self.laserRect.centerx,self.laserRect.bottom),1)
			
class DestructableTile(BoxTile):
	def __init__(self,pos,gameObject,orientation=None,w=64,h=64):
		super(DestructableTile,self).__init__(pos,gameObject,orientation,w,h)
		
		self.alive=True
		self.type="destructable"
		self.HP=3
		self.frame=7
		self.image = self.imglist[self.frame]
		
	def update(self,timepassed):
		super(DestructableTile,self).update(timepassed)
		
		if self.HP<=0:
			self.alive=False
		
		if self.HP==3:
			self.frame=7
		elif self.HP==2:
			self.frame=8
		elif self.HP==1:
			self.frame=9
		
		# update and get the new image
		self.image = self.imglist[self.frame]

class FlamingTile(BoxTile):
	def __init__(self,pos,gameObject,orientation=None,w=64,h=64):
		super(FlamingTile,self).__init__(pos,gameObject,orientation,w,h)
		
		self.type="flaming"
		self.frame=13
		self.image = self.imglist[self.frame]
		
		self.isFiring=False
		
		# give it a random starting values to give the lasers some unpredictability
		self.accFireTime=random.randint(100,3000) 
		
		self.updateFireTime=5000
		self.firingHeldTime=0
		self.maxFiringTime=2000
		self.maxFlameEmitters=1
		self.createdEmitters=0
		
	def update(self,timepassed):
		super(FlamingTile,self).update(timepassed)
		
		
		if self.isFiring:
			self.frame=14
			if self.createdEmitters<self.maxFlameEmitters:
				fxEmitter=AnimEmitter((self.rect.centerx-6,self.rect.centery),self.game.flamefxSheet,xvel=0.01,yvel=-3.4,fps=9,collidable=True,collisiontype="flames")
				self.game.emitterList.append(fxEmitter)
				
				self.createdEmitters+=1
						
			
		else:
			self.frame=13
		
		# update and get the new image
		self.image = self.imglist[self.frame]
		
		if not self.isFiring:
			self.accFireTime+=timepassed
		
			if self.accFireTime>self.updateFireTime:
				self.isFiring=True
				self.accFireTime=0
						
		if self.isFiring:
			self.firingHeldTime+=timepassed
				
			if self.firingHeldTime>self.maxFiringTime:
				self.firingHeldTime=0
				self.isFiring=False
				self.createdEmitters=0
		
		
		
