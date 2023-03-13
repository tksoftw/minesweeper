from minesweeper import Grid, Position
import pygame
import time
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


class GridGUI():
	def __init__(self, g: Grid, screen_length, const_border):
		self.g = g
		self.screen_length = screen_length
		self.row_length = len(g.grid)
		self.const_border = const_border
		self.total_border = const_border + self.get_border_padding()
		self.screen = pygame.display.set_mode((screen_length, screen_length))
		self.font = pygame.font.Font(pygame.font.get_default_font(), 36)


		
	def get_border_padding(self):
		W = self.screen_length
		C = self.const_border
		A = self.row_length
		D = W - 2*C
		T = D // A
		x = (W - 2*C - A*T)/2
		return x
	
	def get_box_size(self):
		W = self.screen_length
		B = self.total_border
		A = self.row_length
		return (W - 2*B)/A

	def draw_grid(self):	
		self.screen.fill(COLORS['light_grey'])
		box_size = self.get_box_size() 
		for i, row in enumerate(self.g.grid):
			for j, v in enumerate(row):
				viewable = self.g.viewable_grid[i][j]
				ypos = i*box_size + self.total_border
				xpos = j*box_size + self.total_border
				box = pygame.Rect(xpos, ypos, box_size, box_size)
				if viewable == '*':
					pygame.draw.rect(self.screen, COLORS['red'], box)
					mine = self.font.render('*', True, COLORS['white'])
					aligner = mine.get_rect(center=(box.centerx, box.centery))
					self.screen.blit(mine, aligner)
				elif viewable == '#':
					flag = self.font.render('#', True, COLORS['red'])
					aligner = flag.get_rect(center=(box.centerx, box.centery))
					self.screen.blit(flag, aligner)
				elif viewable == '.':
					pygame.draw.rect(self.screen, COLORS['grey'], box)
				elif viewable.isdigit():
					pygame.draw.rect(self.screen, COLORS['grey'], box)
					warning_number = self.font.render(v, True, COLORS['black'])
					aligner = warning_number.get_rect(center=(box.centerx, box.centery))
					self.screen.blit(warning_number, aligner)
				pygame.draw.rect(self.screen, COLORS['black'], box, 1)

		pygame.display.update()


	def get_box_inds_from_pos(self, x, y):
		B = self.total_border
		
		box_size = self.get_box_size()
		row = ((x+B)/box_size)-1 # -1 to account for 0-indexing
		col = ((y+B)/box_size)-1
		return (int(row), int(col)) # should be whole numbers anyway


g = Grid(8, 10)
gui = GridGUI(g, 500, 30)
gui.draw_grid()

screen = pygame.display.get_surface()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
		if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1,3):
			box_inds = gui.get_box_inds_from_pos(*event.pos)
			p = Position(*box_inds)
			if event.button == 1:
				removed_mine = not gui.g.remove_tile(p)	
				game_over = gui.g.is_completed_board() or removed_mine
				running = not game_over
			elif event.button == 3:
				gui.g.flag(p, unflag_if_flagged=True)
			gui.draw_grid()


time.sleep(1)
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
