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
	def __init__(self, w=640, h=480, c_visible=False, bar_ps=None):
		self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
		self.w, self.h = w, h
		self.screen.fill(COLORS['purple'])
		self.inner_box = pygame.Rect(0, 0, self.w//1.25, self.h//1.5)
		self.inner_box.center = (self.w/2, self.h/2)
		pygame.draw.rect(self.screen, COLORS['black'], self.inner_box)
	
		standard_box_dims = self.inner_box.w/4, self.inner_box.h/5
		C = 1.5*(standard_box_dims[0]+standard_box_dims[1])/(self.inner_box.w+self.inner_box.h)
		pt = int((standard_box_dims[0]+standard_box_dims[1])/2*self.get_px_to_pt_multiplier()*C)
		self.button_font = pygame.font.Font(pygame.font.get_default_font(), pt) 
		
		self.debug_boxes = {}

		self.buttons = self.get_buttons()
		self.slider_ball_radius, self.sliders = self.get_sliders(bar_percents=bar_ps)

		self.custom_settings_box = None
		self.custom_settings_visible = c_visible

		# render rectangles
		self.render_everything()
	
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
	

	def get_buttons(self):
		button_count = 4
		mps = self.get_midpoints(self.inner_box.x, self.inner_box.x+self.inner_box.w, 2) # log_2(4)
		boxes = []
		for xmid in mps:
			b = pygame.Rect(0, 0, self.inner_box.w/5, self.inner_box.h/4)
			b.midtop = xmid, -b.h+self.inner_box.bottomleft[1]-(self.inner_box.h-b.h)*(.85) # 85% up
			boxes.append(b)	
		
		boxes.sort(key=lambda box: box.x)
		return boxes
	
	def draw_buttons(self):
		messages = ('Easy', 'Normal', 'Expert', 'Custom')
		for i, b in enumerate(self.buttons):
			# render box
			pygame.draw.rect(self.screen, COLORS['red'], b, 2)
			# draw text
			text = self.button_font.render(messages[i%len(self.buttons)], True, COLORS['white'])
			aligner = text.get_rect(center=(b.center))
			self.screen.blit(text, aligner)

	def get_sliders(self, opposite_side=False, bar_percents=None):
		slider_container = pygame.Rect(0,0, self.inner_box.w/2, self.inner_box.bottomleft[1]-self.buttons[0].bottomleft[1])
		if not opposite_side:
			slider_container.bottomleft = self.inner_box.bottomleft
		else:
			slider_container.bottomright = self.inner_box.bottomright
			self.custom_slider_box = slider_container

		sc2 = pygame.Rect(0,0, slider_container.w*.8, slider_container.h*.7)
		sc2.center = slider_container.center
		slider_count = 2
		sliders = []
		mps = self.get_midpoints(sc2.y, sc2.y+sc2.h, 1)
		debug_sc3s = []
		debug_sc4s = []
		radius = None
		for i, ymid in enumerate(mps):
			sc3 = pygame.Rect(0,0, self.inner_box.w/2.25, self.inner_box.h/5)
			if opposite_side:
				sc3.midright = self.buttons[-1].midright[0], ymid
			else:
				sc3.midleft = self.buttons[0].x, ymid
			debug_sc3s.append(sc3)

			inner_mps = self.get_midpoints(sc3.y, sc3.y+sc3.h, 1)
			for j, inner_ymid in enumerate(inner_mps):
				sc4 = pygame.Rect(0,0, sc3.w/2, sc3.h/1.70)
				radius = sc4.h//2
				if opposite_side:
					sc4.center = self.buttons[-1].centerx, inner_ymid
				else:
					sc4.midleft = self.buttons[0].x, inner_ymid
				debug_sc4s.append(sc4)
				
				if j % 2 == 0: # even
					# setup text
					message = str(j*2)
					sliders.append((message, sc4))
				else:
					# setup rect
					s = pygame.Rect(0,0, sc4.w/1.25, sc4.h/16)
					s.center = sc4.center
					sb_n = len(mps)*int(opposite_side)+i
					sb = pygame.Rect(0,0, (sb_n+1)*(sc4.h/2.5), (sb_n+1)*(sc4.h/2.5))
					sb.center = s.midleft if bar_percents is None else self.get_centers_from_percents(bar_percents)
					self.slider_radius = int(sc4.h//2)
					sliders[-1] = (s, sb) + sliders[-1]

		
		to_add_debug = (slider_container, sc2, debug_sc3s, debug_sc4s)
		if not opposite_side:
			self.debug_boxes['sliders'] = []
			self.debug_boxes['sliders'].append(to_add_debug)
			return radius, (sliders + self.get_sliders(True, sb_centers))
		else:	
			self.debug_boxes['sliders'].append(to_add_debug)
			return sliders
	
	def draw_slider(self, n):
		s, sb, message, message_cont = self.sliders[n]
		color1, color2, color3 = COLORS['green'], COLORS['mid_grey'], COLORS['white']
		print(sb.center)
		color2 = color2[:-1] + ((n*200)%255,)
		pygame.draw.rect(self.screen, color1, s)
		pygame.draw.rect(self.screen, color2, sb)#, border_radius=self.slider_ball_radius)
		
		current_percent = self.get_bar_percent(n)
		text = self.button_font.render(f'{message}: {current_percent}', True, color3)
		aligner = text.get_rect(center=message_cont.center)
		self.screen.blit(text, aligner)

	def draw_sliders(self, debug=False):
		for i in range(len(self.sliders)):
			self.draw_slider(i)
		if not self.custom_settings_visible:
			pygame.draw.rect(self.screen, COLORS['black'], self.custom_slider_box)
		if debug:
			for i in range(2):
				slider_container, sc2, dsc3, dsc4 = self.debug_boxes['sliders'][i]
				pygame.draw.rect(self.screen, COLORS['grey'], slider_container, 2)
				pygame.draw.rect(self.screen, COLORS['light_grey'], sc2, 2)
				for sc3 in dsc3:
					pygame.draw.rect(self.screen, COLORS['blue'], sc3, 2)
				for sc4 in dsc4:	
					pygame.draw.rect(self.screen, COLORS['purple'], sc4, 2)
	
	def update_slider(self, n, new_ball_pos):
		s, sb, message, message_cont= self.sliders[n]
		
		sl_cont = pygame.Rect(s)
		sl_cont.w += sb.w*2
		sl_cont.h += message_cont.h*2
		sl_cont.topleft = message_cont.topleft
		sl_cont.y -= s.h
		
		pygame.draw.rect(self.screen, COLORS['black'], sl_cont)
		new_centerx = min(max(new_ball_pos[0], s.x), s.right) # ensure sliderball doesn't go out of range
		self.sliders[n][1].centerx = new_centerx # slider ball
		self.draw_slider(n)
		return sl_cont

	def in_range_rect(self, r, p, allowed_error=0):
		# make copy
		r_cont = pygame.Rect(r)

		# scale
		r_cont.w += r.w*allowed_error
		r_cont.h += r.h*allowed_error*(r.w)

		# re-center
		r_cont.center = r.center	
		#pygame.draw.rect(self.screen, COLORS['red'], r_cont, 2)

		return r_cont.collidepoint(p)
			
	def in_range_2d(self, p, rangeX, rangeY):
		return p[0] in rangeX and p[1] in rangeY

	def in_range_pythag(self, p1, p2, h_limit):
		(x1,y1), (x2,y2) = p1, p2

		# distance formula
		return (( (x2-x1)**2 + (y2-y1)**2 )**(1/2)) < h_limit
	
	def slider_clicked(self, p, allowed_error=0):
		for i, (s, sb, *_) in enumerate(self.sliders):
			if self.in_range_rect(s, p, allowed_error):
				return i
		return None

	def render_everything(self):
		# draw buttons
		self.draw_buttons()
		
		# render sliders
		self.draw_sliders(True)

		pygame.display.update()
	
	def get_bar_percent(self, s_n, round_digits=0):
		s, sb, *_ = self.sliders[s_n]
		px, bar_min, bar_max = sb.centerx, s.x, s.right
		max_d = bar_max - bar_min
		d = bar_max-px
		return round((1-d/max_d)*100, round_digits)

	def get_center_from_percent(self, s_n, percent):
		s, sb, *_ = self.sliders[s_n]
		bar_min, bar_max = s.x, s.right
		max_d = bar_max - bar_min
		x = (1/100)*percent*max_d-1-bar_max # algebra
		return x

	def run(self):
		# main stuff
		last_click = None
		hovered_sb_num = -1
		clock = pygame.time.Clock()
		while True:
			clock.tick(0)	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				
				if event.type == pygame.WINDOWRESIZED:
					new_w, new_h = event.x, event.y
					percents = [self.get_bar_percent(i) for i in range(len(self.sliders))]
					print(percents)
					self.__init__(new_w, new_h, self.custom_settings_visible, percents)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # click
					if self.buttons[-1].collidepoint(event.pos): # click on button
						self.custom_settings_visible = not self.custom_settings_visible
						if self.custom_settings_visible:
							self.draw_sliders(debug=True)
						else:
							pygame.draw.rect(self.screen, COLORS['black'], self.custom_slider_box)
						pygame.display.update(self.custom_slider_box)
					elif (sl_ind := self.slider_clicked(event.pos, allowed_error=0.1)) is not None: # click on slider
						s, sb, *_ = self.sliders[sl_ind]
						eraser = self.update_slider(sl_ind, event.pos)	
						pygame.display.update([sb, s, eraser])
						hovered_sb_num = sl_ind


				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					hovered_sb_num = -1

				if hovered_sb_num != -1 and event.type == pygame.MOUSEMOTION:
					sl = self.sliders[hovered_sb_num]
					if (self.get_bar_percent(hovered_sb_num) != 100.0) or (event.pos[0] in range(sl[0].x, sl[0].right+1)):
						eraser = self.update_slider(hovered_sb_num, event.pos)
						pygame.display.update([sb, s, eraser])


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
		self.game_is_over = False

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
				if self.game_is_over and v == '*':
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
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False

				if event.type == pygame.MOUSEMOTION:
					i, j = gui.get_box_inds_from_pos(*event.pos)
					gui.color_hover(i,j)

				
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gui.is_in_playable_area(*event.pos):
					i, j = gui.get_box_inds_from_pos(*event.pos)
					p = Position(i, j)
					removed_mine = not gui.g.remove_tile(p)
					gui.game_is_over = removed_mine or gui.g.is_completed_board() 
					gui.draw_grid()
					if gui.game_is_over:
						return

				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and gui.is_in_playable_area(*event.pos):
					i, j = gui.get_box_inds_from_pos(*event.pos)
					p = Position(i, j)
					
					gui.g.flag(p, unflag_if_flagged=True)
					gui.draw_grid()

if __name__ == '__main__':
	m = MenuGUI()
	m.run()

	g = Grid(25, 50)
	gui = GridGUI(g, 800, 50)
	gui.draw_grid()
	gui.play_game()
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
