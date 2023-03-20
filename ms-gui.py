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
	'mid_grey': (148,148,148),
	'purple': (98, 2, 185)
}

class MenuGUI():
	def __init__(self, w=640, h=480, fullscreen=False):
		self.w = w
		self.h = h
		self.fullscreen = fullscreen
		if fullscreen:
			self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
		self.screen.fill(COLORS['purple'])
		self.inner_box = pygame.Rect(0, 0, w//1.25, h//1.5)
		self.inner_box.center = (w/2, h/2)
		pygame.draw.rect(self.screen, COLORS['black'], self.inner_box)
		
		self.font_multiplier = self.get_px_to_pt_multiplier()

		self.buttons = []
		self.sliders = []

		# render rectangles
		self.render_everything()
	
	def update_screen(self, w, h):
		self.w = w
		self.h = h
		self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
		self.screen.fill(COLORS['purple'])
		self.inner_box = pygame.Rect(0, 0, w//1.25, h//1.5)
		self.inner_box.center = (w/2, h/2)
		pygame.draw.rect(self.screen, COLORS['black'], self.inner_box)
		self.font_multiplier = self.get_px_to_pt_multiplier()
	
	def get_px_to_pt_multiplier(self, test_str='O'):
			# x -> font pt, y -> font px
			y1 = 10
			f1 = pygame.font.Font(pygame.font.get_default_font(), y1)
			x1 = f1.size(test_str)[0]
			y2 = 100
			f2 = pygame.font.Font(pygame.font.get_default_font(), y2)
			x2 = f2.size(test_str)[0]
			return (x1/y1 + x2/y2)/2
	
	def get_midpoints(self, l, r, splits=1, cur_depth=0):
			midpoint = (l + r) / 2
			if cur_depth == splits:
				return [midpoint]
			
			l_midpoint = self.get_midpoints(l, midpoint, splits, cur_depth+1)
			r_midpoint = self.get_midpoints(midpoint, r, splits, cur_depth+1)
			return l_midpoint + r_midpoint
		

	def render_buttons(self):
		button_count = 4
		mps = self.get_midpoints(self.inner_box.x, self.inner_box.x+self.inner_box.w, 2) # log_2(4)
		boxes = []
		for xmid in mps:
			b = pygame.Rect(0, 0, self.inner_box.w/5, self.inner_box.h/4)
			b.midtop = xmid, -b.h+self.inner_box.bottomleft[1]-(self.inner_box.h-b.h)*(.85) # 85% up
			boxes.append(b)	
			pygame.draw.rect(self.screen, COLORS['red'], b, 2)
		
		# render text on buttons
		C = 1.5*(boxes[0].w+boxes[0].h)/(self.inner_box.w+self.inner_box.h)
		pt = int((boxes[0].w+boxes[0].h)/2*self.font_multiplier*C) 
		text_font = pygame.font.Font(pygame.font.get_default_font(), pt)
		boxes.sort(key=lambda box: box.x)
		messages = ('Easy', 'Normal', 'Expert', 'Custom')
		for i, box in enumerate(boxes):
			text = text_font.render(messages[i%len(boxes)], True, COLORS['white'])
			aligner = text.get_rect(center=(box.center))
			self.screen.blit(text, aligner)

		return boxes


	def render_sliders(self, slider_container, lock_opposite_side=False):
		sc2 = pygame.Rect(0,0, slider_container.w*.8, slider_container.h*.7)
		sc2.center = slider_container.center
		pygame.draw.rect(self.screen, COLORS['grey'], slider_container, 2)
		pygame.draw.rect(self.screen, COLORS['light_grey'], sc2, 2)
		slider_count = 2
		sliders = []
		mps = self.get_midpoints(sc2.y, sc2.y+sc2.h, 1)
		for ymid in mps:
			sc3 = pygame.Rect(0,0, self.inner_box.w/2.25, self.inner_box.h/5)
			if lock_opposite_side:
				sc3.midright = self.buttons[-1].midright[0], ymid
			else:
				sc3.midleft = self.buttons[0].x, ymid
			pygame.draw.rect(self.screen, COLORS['blue'], sc3, 2)
			inner_mps = self.get_midpoints(sc3.y, sc3.y+sc3.h, 1)
			for i, inner_ymid in enumerate(inner_mps):
				sc4 = pygame.Rect(0,0, sc3.w/2, sc3.h/1.70)
				if lock_opposite_side:
					sc4.center = self.buttons[-1].centerx, inner_ymid
				else:
					sc4.midleft = self.buttons[0].x, inner_ymid
				pygame.draw.rect(self.screen, COLORS['purple'], sc4, 2)
				if (i+1) % 2 == 0:
					s = pygame.Rect(0,0, sc4.w/1.25, sc4.h/16)
					s.center = sc4.center
					pygame.draw.rect(self.screen, COLORS['green'], s)
					sb = pygame.Rect(0,0, sc4.h/2.5, sc4.h/2.5)
					sb.center = s.midleft
					pygame.draw.rect(self.screen, COLORS['mid_grey'], sb, border_radius=int(sc4.h//2))
					sliders.append((s, sb))

		return sliders
	
	def in_range_2d(self, p, rangeX, rangeY):
		return p[0] in rangeX and p[1] in rangeY

	def render_everything(self):	
		# render buttons
		button_boxes = self.render_buttons()
		self.buttons = button_boxes

		# render sliders
		scA = pygame.Rect(0,0, self.inner_box.w/2, self.inner_box.bottomleft[1]-self.buttons[0].bottomleft[1])
		scA.bottomleft = self.inner_box.bottomleft

		scB = pygame.Rect(scA)
		scB.bottomright = self.inner_box.bottomright
	
		slidersA = self.render_sliders(scA)		
		slidersB = self.render_sliders(scB, True)

		# hide custom gamemode sliders
		pygame.draw.rect(self.screen, COLORS['black'], scB)


		self.sliders.append((scA, slidersA))
		self.sliders.append((scB, slidersB))
		pygame.display.update()
	
	def get_c_ranges(self):
		c_xrange = range(self.buttons[-1].x, self.buttons[-1].x+self.buttons[-1].w)
		c_yrange = range(self.buttons[-1].y, self.buttons[-1].y+self.buttons[-1].h)
		return c_xrange, c_yrange

	def run(self):
		# main stuff
		c_xrange, c_yrange = self.get_c_ranges()
		c_sliders = self.sliders[1][0]
		c_settings_visible = False
		last_dims = self.w, self.h 
		
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				
				if event.type == pygame.WINDOWMAXIMIZED:
					self.__init__(fullscreen=True)
					c_xrange, c_yrange = self.get_c_ranges()
					c_sliders = self.sliders[1][0]
					if c_settings_visible:
						self.render_sliders(c_sliders, True)


				elif event.type == pygame.WINDOWRESTORED:
					print('hola!')

				elif event.type == pygame.WINDOWRESIZED and not self.fullscreen:
					new_w, new_h = event.x, event.y
					self.__init__(new_w, new_h)
					c_xrange, c_yrange = self.get_c_ranges()
					c_sliders = self.sliders[1][0]
					if c_settings_visible:
						self.render_sliders(c_sliders, True)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.in_range_2d(event.pos, c_xrange, c_yrange):
					if not c_settings_visible :
						self.render_sliders(c_sliders, True)
					else:
						pygame.draw.rect(self.screen, COLORS['black'], c_sliders)
					pygame.display.update(c_sliders)
					c_settings_visible  = not c_settings_visible 


class GridGUI():
	def __init__(self, g: Grid, screen_length, const_border):
		self.g = g
		self.screen_length = screen_length
		self.row_length = len(g.grid)
		self.const_border = const_border
		self.total_border = const_border + self.get_border_padding()
		self.box_size = self.get_box_size()	
		self.screen = pygame.display.set_mode((screen_length, screen_length))
		self.font_multiplier = self.get_px_to_pt_multiplier()
		self.font = pygame.font.Font(pygame.font.get_default_font(), int(self.box_size*self.font_multiplier))
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
		if B:=(self.g.is_in_bounds(Position(i,j)) and self.g.viewable_grid[i][j] == '-'):
			self.draw_tile(i, j, COLORS['mid_grey'])
			self.hover = (i, j)
		if A or B:
			pygame.display.update()
	
	def get_box_inds_from_pos(self, x, y):
		B = self.total_border
		
		row = ((y-B)//self.box_size)
		col = ((x-B)//self.box_size)
		return (int(row), int(col)) # for indexing, needs to be int

	def is_in_playable_area(self, x, y):
		i, j = self.get_box_inds_from_pos(x,y)
		p = Position(i,j)
		return self.g.is_in_bounds(p)

	def play_game(self):
		self.screen = pygame.display.set_mode((self.screen_length, self.screen_length))
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False

				if event.type == pygame.MOUSEMOTION:
					i, j = gui.get_box_inds_from_pos(*event.pos)
					gui.color_hover(i,j)

				
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gui.is_in_playable_area(*event.pos):
					print('eeeeeeeeee')
					i, j = gui.get_box_inds_from_pos(*event.pos)
					p = Position(i, j)
					removed_mine = not gui.g.remove_tile(p)
					gui.draw_grid()
					if gui.g.is_completed_board():
						return True
					if removed_mine:
						return False
					
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and gui.is_in_playable_area(*event.pos):
					i, j = gui.get_box_inds_from_pos(*event.pos)
					p = Position(i, j)
					
					gui.g.flag(p, unflag_if_flagged=True)
					gui.draw_grid()

if __name__ == '__main__':
	g = Grid(20, 25)
	gui = GridGUI(g, 800, 50)
	#gui.draw_grid()
	
	m = MenuGUI()
	m.run()
	#gui.play_game()


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
