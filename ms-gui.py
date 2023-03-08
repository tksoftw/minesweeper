import pygame
pygame.init()

width, height = 500, 500
screen = pygame.display.set_mode((width, height))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

ball = pygame.image.load("ball.png")
rect = ball.get_rect()
speed = [1, 1]
rect = rect.move(speed)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	rect = rect.move(speed)
	if rect.left < 0 or rect.right > width:
		speed[0] = -speed[0]
	if rect.top < 0 or rect.bottom > height:
		speed[1] = -speed[1]

	screen.fill(GREEN)
	pygame.draw.rect(screen, RED, rect, 1)
	screen.blit(ball, rect)
	pygame.display.update()



pygame.quit()



"""
if event.type == pygame.MOUSEMOTION:
			r, g = [p // 2 for p in event.pos]
			b = (r + g) % 256
			color = (r, g, b)
			screen.fill(color)
			pygame.display.update()
"""
