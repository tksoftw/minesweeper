from minesweeper import Grid, Position
import pygame
import time
pygame.init()

COLORS = {
	'black': (0,0,0),
	'white': (255,255,255),
	'grey': (138,138,138),
	'red': (255,0,0),
	'green': (0,255,0),
	'blue': (0,0,255),
	'light_grey': (192,192,192),
	'mid_grey': (148,148,148)
}


class GridGUI():
	def __init__(self, g: Grid, screen_length, const_border):
		self.g = g
		self.screen_length = screen_length
		self.row_length = len(g.grid)
		self.const_border = const_border
		self.total_border = const_border + self.get_border_padding()
		self.box_size = self.get_box_size()	
		self.screen = pygame.display.set_mode((screen_length, screen_length))
		k = self.get_px_to_pt_multiplier()
		self.font = pygame.font.Font(pygame.font.get_default_font(), int(self.box_size*k))
		self.hover = None

	def get_px_to_pt_multiplier(self):
		# x -> font pt, y -> font px
		y1 = 10
		f1 = pygame.font.Font(pygame.font.get_default_font(), y1)
		x1 = f1.size('O')[0]
		y2 = 100
		f2 = pygame.font.Font(pygame.font.get_default_font(), y2)
		x2 = f2.size('O')[0]
		return (x1/y1 + x2/y2)/2
				
	def is_in_grid_bounds(self, i, j):
		return i in range(0, self.row_length) and j in range(0, len(self.g.grid[i]))

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
		self.screen.fill(COLORS['grey'])
		for i, row in enumerate(self.g.grid):
			for j, v in enumerate(row):
				viewable = self.g.viewable_grid[i][j]
				xpos, ypos = [ind*self.box_size + self.total_border for ind in (j, i)]
				box = pygame.Rect(xpos, ypos, self.box_size, self.box_size)
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
					pygame.draw.rect(self.screen, COLORS['light_grey'], box)
				elif viewable.isdigit():
					pygame.draw.rect(self.screen, COLORS['light_grey'], box)
					warning_number = self.font.render(v, True, COLORS['black'])
					aligner = warning_number.get_rect(center=(box.centerx, box.centery))
					self.screen.blit(warning_number, aligner)
				pygame.draw.rect(self.screen, COLORS['black'], box, 1)

		pygame.display.update()	

	def draw_tile(self, i, j, color, text=None):
		xpos, ypos = [ind*self.box_size + self.total_border for ind in (j, i)]
		box = pygame.Rect(xpos, ypos, self.box_size, self.box_size)
		pygame.draw.rect(self.screen, color, box)
		pygame.draw.rect(self.screen, COLORS['black'], box, 1)


	def color_hover(self, i, j):
		if A:=(self.hover is not None and self.g.viewable_grid[self.hover[0]][self.hover[1]] == '-'):
			self.draw_tile(*self.hover, COLORS['grey'])
			self.hover = None
		if B:=(self.is_in_grid_bounds(i, j) and self.g.viewable_grid[i][j] == '-'):
			self.draw_tile(i, j, COLORS['mid_grey'])
			self.hover = (i, j)
		if A or B:
			pygame.display.update()

	
	def get_box_inds_from_pos(self, x, y):
		B = self.total_border
		
		row = ((y-B)//self.box_size)
		col = ((x-B)//self.box_size)
		return (int(row), int(col)) # for indexing, needs to be int

g = Grid(20, 25)
gui = GridGUI(g, 800, 50)
gui.draw_grid()

screen = pygame.display.get_surface()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		
		if event.type == pygame.MOUSEMOTION:
			i, j = gui.get_box_inds_from_pos(*event.pos)
			gui.color_hover(i,j)


		if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1,3):
			i, j = gui.get_box_inds_from_pos(*event.pos)
			if not gui.is_in_grid_bounds(i, j):
				break

			p = Position(i, j)
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
