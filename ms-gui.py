from minesweeper import Grid, Position
import pygame
pygame.init()

COLORS = {
	'black': (0,0,0),
	'white': (255,255,255),
	'grey': (192,192,192),
	'red': (255,0,0),
	'green': (0,255,0),
	'blue': (0,0,255),
	'light_grey': (138,138,138)
}

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
	width, height = 500, 500
	screen = pygame.display.set_mode((width, height))
	screen.fill(COLORS['light_grey'])

	L = 500
	C = 30
	A = len(g.grid)
	X = get_border_padding(L,C,A)
	print(L, C, X)
	outer_border = C + X
	box_size = (L - 2*outer_border)/A
	print(box_size)

	screen = pygame.display.get_surface()
	font = pygame.font.Font(pygame.font.get_default_font(), 36)

	for i, row in enumerate(g.grid):
		for j, v in enumerate(row):
			viewable = g.viewable_grid[i][j]
			ypos = i*box_size + outer_border
			xpos = j*box_size + outer_border
			box = pygame.Rect(xpos, ypos, box_size, box_size)
			if viewable == '*':
				pygame.draw.rect(screen, COLORS['red'], box)
				mine = font.render('*', True, COLORS['white'])
				aligner = mine.get_rect(center=(box.centerx, box.centery))
				screen.blit(mine, aligner)
			elif viewable == '#':
				flag = font.render('#', True, COLORS['red'])
				aligner = flag.get_rect(center=(box.centerx, box.centery))
				screen.blit(flag, aligner)
			elif viewable == '.':
				pygame.draw.rect(screen, COLORS['grey'], box)
			elif viewable.isdigit():
				pygame.draw.rect(screen, COLORS['grey'], box)
				warning_number = font.render(v, True, COLORS['black'])
				aligner = warning_number.get_rect(center=(box.centerx, box.centery))
				screen.blit(warning_number, aligner)
				
			pygame.draw.rect(screen, COLORS['black'], box, 1)
	
	pygame.display.update()


def get_box_inds_from_pos(x, y, window_width, border_length, boxes_per_row):
	L = window_width
	B = border_length
	A = boxes_per_row
	
	avail = int(L-2*B) # should always be an whole number anyway
	box_size = avail//A 
	print(box_size)
	row = ((x+B)//box_size)-1 # -1 to account for 0-indexing
	col = ((y+B)//box_size)-1
	return (row, col)


g = Grid(8, 10)
draw_grid(g)

screen = pygame.display.get_surface()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
		if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1,3):
			box_inds = get_box_inds_from_pos(*event.pos, 500, 30, 8)
			p = Position(*box_inds)
			if event.button == 1:
				not_removed_mine = g.remove_tile(p)	
				running = not_removed_mine
			elif event.button == 3:
				g.flag(p, unflag_if_flagged=True)
			draw_grid(g)

input()

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
