from minesweeper import Grid
import pygame
pygame.init()

COLORS = {
	'black': (0,0,0),
	'white': (255,255,255),
	'grey': (192,192,192)
}


def draw_everything():
	width, height = 512, 512
	screen = pygame.display.set_mode((width, height))
	screen.fill(COLORS['grey'])

def start_game():
	g = Grid()

def draw_grid(g: Grid):	
	screen_length = 512
	outer_border=5+screen_length%8*2
	available_length = screen_length-2*outer_border
	print(screen_length, available_length)
	box_size = available_length//8

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
