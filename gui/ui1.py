import pygame, sys, math
pygame.init()
surface = pygame.display.set_mode([640,480])
surface.fill([255,255,255]);
pygame.draw.circle(surface,[255,0,0],[320,240],100,10)
pygame.draw.circle(surface,[255,0,0],[280,200],10,10)
pygame.draw.circle(surface,[255,0,0],[360,200],10,10)
pygame.draw.arc(surface,[255,0,0],pygame.Rect(280,220,80,60), math.pi,math.pi*2,10) 
pygame.display.flip()

pic = pygame.image.load("pig.jpg")
rect = surface.blit(pic,[100,100])
pygame.display.flip()


for i in range(1,1000):
	#pygame.time.delay(1000)
	#erase
	pygame.draw.rect(surface,[255,255,255],rect,0)
	rect = rect.move(2,1)
	surface.blit(pic,rect)
	pygame.display.flip()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()