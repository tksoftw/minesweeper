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
		self.slider_font = pygame.font.Font(pygame.font.get_default_font(), pt//2)

		self.debug_boxes = {}

		self.buttons = self.get_buttons()
		self.start_button = self.get_start_button()
		self.slider_ball_radius, self.sliders = self.get_sliders(bar_percents=bar_ps)

		self.custom_settings_visible = c_visible
		self.selected_button = 0	

		self.slider_ratio_map = {n : 10 for n in range(len(self.sliders))}
		self.slider_ratio_map[1] = 0.1
		self.slider_ratio_map[2] = 5
		self.slider_ratio_map[3] = 0.5

		self.absolute_slider_mins = {n: lambda : 1 for n in range(len(self.sliders))}
		self.absolute_slider_mins[2] = lambda : .2
		self.absolute_slider_mins[3] = lambda : ((self.sliders[2][-1]*self.slider_ratio_map[2])**(1/2)+1)/self.slider_ratio_map[3]


		self.difficulty_percent_map = {i: (6**(i+1)/2**(i+1), (i+1)*5) for i in range(3)}
		self.difficulty_percent_map = {i: (n[0]/self.slider_ratio_map[2], n[1]/self.slider_ratio_map[3]) for i, n in self.difficulty_percent_map.copy().items()} # to cancel out ratios
		
		self.update_custom_percents(*self.difficulty_percent_map[0])

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
			if i == self.selected_button:
				shadow = pygame.Rect(b)
				shadow.topleft = b.x-b.w*.02, b.y-b.h*.02
				pygame.draw.rect(self.screen, COLORS['grey'], shadow)
			# render box
			pygame.draw.rect(self.screen, COLORS['red'], b)
			# draw text
			text = self.button_font.render(messages[i%len(self.buttons)], True, COLORS['white'])
			aligner = text.get_rect(center=(b.center))
			self.screen.blit(text, aligner)
	
	def change_selected_button(self, new_n):
		self.selected_button = new_n
		offset_midleft = (self.inner_box.x, self.buttons[0].centery*0.95)
		offset_size = (self.inner_box.w, self.buttons[0].h*1.25)
		eraser = pygame.Rect((0, 0), offset_size)
		eraser.midleft = offset_midleft
		pygame.draw.rect(self.screen, COLORS['black'], eraser)
		self.draw_buttons()
		return eraser

	def get_start_button(self):
		a = 15
		b = pygame.Rect(0, 0, self.inner_box.w/2, self.inner_box.h/2)
		xmid = (self.inner_box.x*2+self.inner_box.w)/2
		b.midtop = xmid, -b.h+self.inner_box.bottomleft[1]-(self.inner_box.h-b.h)*(a/100) # a% up

		return b

	def draw_start_button(self):
		# draw start button
		pygame.draw.rect(self.screen, COLORS['red'], self.start_button)
		# draw text
		text = self.button_font.render('START GAME', True, COLORS['white'])
		aligner = text.get_rect(center=self.start_button.center)
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
		messages = ['Window size', 'Border length', 'Mine count', 'Tiles per row']
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
					sc4.midright = self.buttons[-1].x+self.buttons[-1].w, inner_ymid
				else:
					sc4.midleft = self.buttons[0].x, inner_ymid
				debug_sc4s.append(sc4)
				
				if j % 2 == 0: # even
					# setup text
					msg_n = len(mps)*int(opposite_side)+i
					message = messages[msg_n]
					sliders.append((message, sc4, 50))
				else:
					# setup rect
					s = pygame.Rect(0,0, sc4.w/1.25, sc4.h/16)
					s.center = sc4.center	
					sb = pygame.Rect(0,0, sc4.h/2.5, sc4.h/2.5)
					sb.center = s.midleft
					self.slider_radius = int(sc4.h//2)
					sliders[-1] = (s, sb) + sliders[-1]
					self.update_centerx_from_percent(sliders[-1])
		

		if bar_percents is not None:
			for i, sl in enumerate(sliders):
				sb_n = len(sliders)*int(opposite_side)+i
				sliders[i] = sl[:-1] + (bar_percents[sb_n],) # update percent
				self.update_centerx_from_percent(sliders[i]) # update centerx

		to_add_debug = (slider_container, sc2, debug_sc3s, debug_sc4s)
		if not opposite_side:
			self.debug_boxes['sliders'] = []
			self.debug_boxes['sliders'].append(to_add_debug)
			return radius, (sliders + self.get_sliders(True, bar_percents))
		else:	
			self.debug_boxes['sliders'].append(to_add_debug)
			return sliders
	
	def draw_slider(self, n):
		s, sb, message, message_cont, percent = self.sliders[n]
		color1, color2, color3 = COLORS['green'], COLORS['mid_grey'], COLORS['white']
		color2 = color2[:-1] + ((n*50)%255,)
		pygame.draw.rect(self.screen, color1, s)
		pygame.draw.rect(self.screen, color2, sb, border_radius=self.slider_ball_radius)
		
		text = self.slider_font.render(message, True, color3)
		p_text = self.slider_font.render(str(int(percent*self.slider_ratio_map[n])), True, color3)
		aligner = text.get_rect(center=message_cont.center)
		aligner2 = p_text.get_rect(midtop=aligner.midbottom)
		self.screen.blit(text, aligner)
		self.screen.blit(p_text, aligner2)

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


	def hide_slider(self, n):
		s, sb, message, message_cont, old_percent = self.sliders[n]
		
		sl_cont = pygame.Rect(s)
		sl_cont.w += sb.w
		sl_cont.h += message_cont.h*2
		sl_cont.midleft = s.x-sb.w//2, (message_cont.centery+s.centery)/2
		sl_cont.y -= s.h

		pygame.draw.rect(self.screen, COLORS['black'], sl_cont)
		return sl_cont
	
	def update_slider(self, n, p):
		self.update_centerx_from_position(n, p)
		percent = self.get_bar_percent(n)
		self.update_slider_percent(n, percent)	
		s, sb, *_ = self.sliders[n]
		eraser = self.update_slider_drawing(n)
		return eraser


	def update_slider_drawing(self, n):
		s, sb, message, message_cont, percent = self.sliders[n]
		
		eraser = self.hide_slider(n)
		self.draw_slider(n)
		return eraser

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

	def button_clicked(self, p):
		for i, bt in enumerate(self.buttons):   
			if bt.collidepoint(p):
				return i
		return None
	
	def render_everything(self):
		# draw buttons
		self.draw_buttons()
		
		# draw sliders
		self.draw_sliders(debug=False)#True)
		
		# draw start button
		self.draw_start_button()

		pygame.display.update()

	def get_bar_percent(self, n):
		s, sb, *_ = self.sliders[n]
		px, bar_min, bar_max = sb.centerx, s.x, s.right
		max_d = bar_max - bar_min
		d = bar_max-px
		return max(self.absolute_slider_mins[n](), round((1-d/max_d)*100, 1))

	def update_slider_percent(self, n, new_percent):
		self.sliders[n] = self.sliders[n][:-1] + (new_percent,)

	def update_custom_percents(self, p1, p2):
		self.update_slider_percent(-2, p1)
		self.update_slider_percent(-1, p2)

	def update_centerx_from_percent(self, sl):
		s, sb, *_, percent = sl
		bar_min, bar_max = s.x, s.right
		max_d = bar_max - bar_min
		x = round(max_d*((percent/100)-1)+bar_max, 1) # algebra
		sl[1].centerx = x
	
	def update_centerx_from_position(self, n, new_ball_pos):	
		s, sb, *_, percent = self.sliders[n]
		new_centerx = min(max(new_ball_pos[0], s.x), s.right) # ensure sliderball doesn't go out of range
		self.sliders[n][1].centerx = new_centerx # slider ball

	def toggle_custom_settings(self):
		self.custom_settings_visible = not self.custom_settings_visible
		update_list = []
		if not self.custom_settings_visible:
			update_list.extend([self.hide_slider(-i) for i in range(1,3)])
		else:
			for i in range(1, 3):
				# reset slider positions
				self.sliders[-i] = self.sliders[-i][:-1] + (50,) # update percent
				self.update_centerx_from_percent(self.sliders[-i]) # update centerx
				self.draw_slider(len(self.sliders)-i)
				to_add = list(self.sliders[-i][:2])+[self.sliders[-i][-1]]
				update_list.extend(to_add)

		return update_list
	
	def toggle_start_button_shadow(self, shown=False):
		b = self.start_button
		shadow = pygame.Rect(b)
		shadow.topleft = b.x-b.w*.01, b.y-b.h*.01
		color = COLORS['grey'] if shown else COLORS['black']
		pygame.draw.rect(self.screen, color, shadow)
		self.draw_start_button()
		return shadow

	def run(self):
		# main stuff
		hovered_sb_num = -1
		prev_click = -1, 0
		on_start_button = False
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:	
					return None				
				if event.type == pygame.WINDOWRESIZED:
					new_w, new_h = event.x, event.y
					percents = [sl[-1] for sl in self.sliders]
					self.__init__(new_w, new_h, self.custom_settings_visible, percents)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # click
					if (bt_ind := self.button_clicked(event.pos)) is not None and bt_ind != self.selected_button: # click on button
						prev_bt_ind = self.selected_button
						eraser = self.change_selected_button(bt_ind)
						to_update = [eraser]
						if (A := (bt_ind == (len(self.buttons)-1))) or prev_bt_ind == (len(self.buttons)-1):
							self.toggle_custom_settings()
							to_update.append(self.custom_slider_box)
						if not A:
							self.update_custom_percents(*self.difficulty_percent_map[bt_ind])

						pygame.display.update(to_update)
					elif (sl_ind := self.slider_clicked(event.pos, allowed_error=0.1)) is not None: # click on slider
						if sl_ind >= 2 and not self.custom_settings_visible:
							continue
						if self.in_range_pythag(self.sliders[sl_ind][1].center, event.pos, self.slider_ball_radius):
							if prev_click[0] == sl_ind and prev_click[1] > 0:
								self.update_slider_percent(sl_ind, 50)
								self.update_centerx_from_percent(self.sliders[sl_ind])
							prev_click = sl_ind, prev_click[1]+1
						else:
							self.update_centerx_from_position(sl_ind, event.pos)
							percent = self.get_bar_percent(sl_ind)
							self.update_slider_percent(sl_ind, percent)	

						s, sb, *_ = self.sliders[sl_ind]
						eraser = self.update_slider_drawing(sl_ind)	
						pygame.display.update([sb, s, eraser])
						hovered_sb_num = sl_ind
					elif self.start_button.collidepoint(event.pos):	
						on_start_button = True	
						shadow = self.toggle_start_button_shadow(True)
						pygame.display.update(shadow)

				if on_start_button and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.start_button.collidepoint(event.pos):
					percents = [sl[-1] for sl in self.sliders]
					return percents

				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					hovered_sb_num = -1
					if on_start_button:
						shadow = self.toggle_start_button_shadow(False)
						pygame.display.update(shadow)
					on_start_button = False
								
				if prev_click[0] != -1 and event.type == pygame.MOUSEMOTION:
					prev_click = -1, 0

				if hovered_sb_num != -1 and event.type == pygame.MOUSEMOTION:
					sl = self.sliders[hovered_sb_num]
					if (self.get_bar_percent(hovered_sb_num) != 100.0) or (event.pos[0] in range(sl[0].x, sl[0].right+1)):
						eraser = self.update_slider(hovered_sb_num, event.pos)
						pygame.display.update([sb, s, eraser])
		
		

class GridGUI():
	def __init__(self, g: Grid, screen_length, const_border=5):
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

	def get_px_to_pt_multiplier(self, ch='O'):
		# x -> font pt, y -> font px
		y1 = 10
		f1 = pygame.font.Font(pygame.font.get_default_font(), y1)
		x1 = f1.size(ch)[0]
		y2 = 100
		f2 = pygame.font.Font(pygame.font.get_default_font(), y2)
		x2 = f2.size(ch)[0]
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

	def blur_screen(self):
		old_dims = (self.screen_length, self.screen_length)
		new_dims = list(d*0.1 for d in old_dims)
		
		new_screen = pygame.transform.smoothscale(self.screen, new_dims)
		new_screen = pygame.transform.smoothscale(new_screen, old_dims)
		self.screen.blit(new_screen, (0,0))
	
	def pause_menu(self):
		# blur screen
		self.blur_screen()

		# setup boxes
		screen_box = pygame.Rect(0,0, self.screen_length, self.screen_length)
		exit_main_menu_box = pygame.Rect(0, 0, self.screen_length*0.25, self.screen_length*0.2)
		resume_game_box = pygame.Rect(exit_main_menu_box)
		exit_main_menu_box.midleft = screen_box.midleft
		resume_game_box.midright = screen_box.midright
		exit_main_menu_box.x += exit_main_menu_box.w/1.5
		resume_game_box.x -= resume_game_box.w/1.5

		# setup text
		font_pt = self.get_px_to_pt_multiplier()*resume_game_box.w/4
		font = pygame.font.Font(pygame.font.get_default_font(), int(font_pt))
		resume_text = font.render('Resume', True, COLORS['white'])
		resume_text2 = font.render('game', True, COLORS['white'])
		exit_text = font.render('Exit', True, COLORS['white'])
		exit_text2 = font.render('to menu', True, COLORS['white'])
		bt_height = resume_game_box.centery-resume_game_box.h/7.5
		resume_aligner = resume_text.get_rect(center=(resume_game_box.centerx, bt_height))
		exit_aligner = exit_text.get_rect(center=(exit_main_menu_box.centerx, bt_height))
		resume_aligner2 = resume_text2.get_rect(center=(resume_game_box.centerx, bt_height+resume_aligner.h))
		exit_aligner2 = exit_text2.get_rect(center=(exit_main_menu_box.centerx, bt_height+exit_aligner.h))	
		
		# draw
		pygame.draw.rect(self.screen, COLORS['red'], exit_main_menu_box, 10)
		pygame.draw.rect(self.screen, COLORS['green'], resume_game_box, 10)
		self.screen.blit(resume_text, resume_aligner)
		self.screen.blit(exit_text, exit_aligner)
		self.screen.blit(resume_text2, resume_aligner2)
		self.screen.blit(exit_text2, exit_aligner2)

		pygame.display.update()

		state = -1
		while state == -1:
			for event in pygame.event.get():				
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					state = 0
				
				if event.type == pygame.MOUSEBUTTONUP and resume_game_box.collidepoint(event.pos):
					state = 0

				if event.type == pygame.MOUSEBUTTONUP and exit_main_menu_box.collidepoint(event.pos):
					state = 1

		self.draw_grid()
		return bool(state)

	def play_game(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False

				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					quit = self.pause_menu()
					if quit:
						return

				if event.type == pygame.MOUSEMOTION:
					i, j = self.get_box_inds_from_pos(*event.pos)
					self.color_hover(i,j)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_in_playable_area(*event.pos):
					i, j = self.get_box_inds_from_pos(*event.pos)
					p = Position(i, j)
					removed_mine = not self.g.remove_tile(p)
					self.game_is_over = removed_mine or self.g.is_completed_board() 
					self.draw_grid()
					if self.game_is_over:
						return

				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.is_in_playable_area(*event.pos):
					i, j = self.get_box_inds_from_pos(*event.pos)
					p = Position(i, j)
					
					self.g.flag(p, unflag_if_flagged=True)
					self.draw_grid()

if __name__ == '__main__':
	m = MenuGUI()
	ps = m.run()
	ps = [int(p*m.slider_ratio_map[i]) for i, p in enumerate(ps.copy())]
	window_length, border_length, mine_count, tiles_per_row = ps
	
	print(ps)

	g = Grid(tiles_per_row, mine_count) # 25, 50
	gui = GridGUI(g, window_length, border_length) # 500, 50
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
