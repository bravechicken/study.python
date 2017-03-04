#-*- coding: utf-8 -*-
import pygame, sys, math

class Pig(pygame.sprite.Sprite):
	def __init__(self, image,location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location


#初始化,
pygame.init()
#屏幕大小调整好
surface = pygame.display.set_mode([1024,1000])
#全部填充白色
surface.fill([255,255,255]);

pigs = []

#循环1000次
for i in range(1,10):
	location = [i*100,i*100]
	pig = Pig("pig.jpg",location)
	pigs.append(pig)

for p in pigs:
	surface.blit(p.image, p.rect)

pygame.display.flip()

#处理关闭事件
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()