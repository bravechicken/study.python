import pygame, sys
pygame.init()
screen = pygame.display.set_mode([740,480])
screen.fill([255,255,255])
my_ball = pygame.image.load("earth2.gif")
RED   = (0,   0,   0)
pygame.draw.ellipse(screen, RED, (10, 10, 600, 200), 1)
screen.blit(my_ball, [20, 20])
pygame.display.flip()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

