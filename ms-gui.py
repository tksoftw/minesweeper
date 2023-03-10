from minesweeper import Grid
import pygame
pygame.init()

COLORS = {
	'black': (0,0,0),
	'white': (255,255,255),
	'grey': (192,192,192),
	'red': (255,0,0)
}


def draw_everything():
	width, height = 500, 500
	screen = pygame.display.set_mode((width, height))
	screen.fill(COLORS['grey'])

def start_game():
	g = Grid()


def get_border_padding(screen_length, const_border, boxes_per_row):
	W = screen_length
	C = const_border
	A = boxes_per_row
	D = W - 2*C
	T = D // A
	x = (W - 2*C - A*T)/2
	return x

def draw_grid(g: Grid):	
	L = 500
	C = 30
	A = len(g.grid)
	X = get_border_padding(L,C,A)
	print(L, C, X)
	outer_border = C + X
	box_size = (L - 2*outer_border)/A
	print(box_size)

	screen = pygame.display.get_surface()

	for x, row in enumerate(g.grid):
		for y, v in enumerate(row):
			xpos = x*box_size + outer_border
			ypos = y*box_size + outer_border
			box = pygame.Rect(xpos, ypos, box_size, box_size)
			if v == '*':
				pygame.draw.rect(screen, COLORS['red'], box)	
				pygame.draw.rect(screen, COLORS['black'], box, 1)
			else:
				pygame.draw.rect(screen, COLORS['black'], box, 1)
	
	pygame.display.update()

g = Grid(32, 32)
draw_everything()
draw_grid(g)

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
