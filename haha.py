import pygame, sys
pygame.init()
screen = pygame.display.set_mode([740,480])
screen.fill([255,255,255])
my_ball = pygame.image.load("haha.jpg")
screen.blit(my_ball, [60, 60])
pygame.display.flip()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

