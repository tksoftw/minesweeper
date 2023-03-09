from minesweeper import Grid
import pygame
pygame.init()


def draw_everything():
	width, height = 512, 512
	screen = pygame.display.set_mode((width, height))

def start_game():
	g = Grid()


def draw_grid(g: Grid):
	box_size = 512//8
	screen = pygame.display.get_surface()

	mat = [[0]*8 for _ in range(8)]
	for x, row in enumerate(mat):
		for y, v in enumerate(row):
			box = pygame.Rect(x*box_size, y*box_size, box_size, box_size)
			pygame.draw.rect(screen, (0, 255, 255), box, 2)
	
	pygame.display.update()

draw_everything()
draw_grid(Grid())

screen = pygame.display.get_surface()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
				
	



pygame.quit()



"""
if event.type == pygame.MOUSEMOTION:
			print(event.pos)
			r, g = [p // 2 for p in event.pos]
			b = (r + g) % 256
			color = (r, g, b)
			screen.fill(color)
			pygame.display.update()

"""
