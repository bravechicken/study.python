import pygame, sys
pygame.init()
screen = pygame.display.set_mode([640,480])
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()