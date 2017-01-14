import pygame, sys, math

DRAW_COLOR = [0,0,0]

pygame.init()
surface = pygame.display.set_mode([700,700])
surface.fill([255,255,255]);
pygame.draw.circle(surface,DRAW_COLOR,[320,240],100,10)#face
pygame.draw.circle(surface,DRAW_COLOR,[280,200],35,0)#glass
pygame.draw.circle(surface,DRAW_COLOR,[360,200],35,0)#glass
pygame.draw.circle(surface,[255,255,255],[280,200],10,10)#eyes
pygame.draw.circle(surface,[255,255,255],[360,200],10,10)#eyes
pygame.draw.arc(surface,DRAW_COLOR,pygame.Rect(200,140,80,60), math.pi/4,3*math.pi/2,10) 
pygame.draw.arc(surface,DRAW_COLOR,pygame.Rect(300,100,80,60), 2*math.pi/3,math.pi*2,0) 
pygame.draw.circle(surface,DRAW_COLOR,[320,240],10,10)#nose
pygame.draw.arc(surface,DRAW_COLOR,pygame.Rect(280,220,80,60), math.pi,math.pi*2,10) 
pygame.display.flip()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()