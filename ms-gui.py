from minesweeper import Grid
import pygame
pygame.init()

COLORS = {
	'black': (0,0,0),
	'white': (255,255,255),
	'grey': (192,192,192)
}


def draw_everything():
	width, height = 500, 500
	screen = pygame.display.set_mode((width, height))
	screen.fill(COLORS['grey'])

def start_game():
	g = Grid()

def draw_grid(g: Grid):	
	L = 500
	C = 10
	X = (-C + ((-L//2) % 4)) % 4
	print(L, C, X)
	outer_border = C + X
	box_size = (L - 2*outer_border)//8
	print(box_size)


	screen = pygame.display.get_surface()

	mat = [[0]*8 for _ in range(8)]
	for x, row in enumerate(mat):
		for y, v in enumerate(row):
			xpos = x*box_size + outer_border
			ypos = y*box_size + outer_border
			box = pygame.Rect(xpos, ypos, box_size, box_size)
			pygame.draw.rect(screen, COLORS['black'], box, 1)
	
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
