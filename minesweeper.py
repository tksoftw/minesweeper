import random
import string

class ValleyManager:
	def __init__(self):
		self.valleys = []
		self.enterances = {}
	
		

class Position:
	p_table = {c: i for i, c in enumerate(string.ascii_uppercase)}
	
	def __init__(self, row, col):
		self.x = col
		self.y = row

	@classmethod
	def from_str(cls, pos_str):
		px = cls.p_table[pos_str[0].upper()]
		py = int(pos_str[1])-1 # accounting for 0-indexing
		return Position(py, px)

class Grid:
	def __init__(self, dim=8, mines=10, debug_mode=False):
		self.grid = [['-']*dim for _ in range(dim)]
		self.viewable_grid = [["-"]*dim for _ in range(dim)]
		self.hidden_tiles = {(i,j) for j in range(dim) for i in range(dim)}
		self.mine_count = 0
		self.valleys = []
		self.debug_mode = debug_mode

		# prep functions
		if not self.debug_mode:
			self._scatter_mines(mines)
			self._calc_numbers()
			self.valleys = self._get_valleys()

	def _scatter_mines(self, mines_to_place):
		placed = set()
		for _ in range(mines_to_place):
			i = random.randint(0, len(self.grid)-1)
			j = random.randint(0, len(self.grid[i])-1)
			while (i, j) in placed:
				i = random.randint(0, len(self.grid)-1)
				j = random.randint(0, len(self.grid[i])-1)
			placed.add((i,j))
			self.grid[i][j] = '*'
			self.mine_count += 1

	def _get_adj_inds(self, i, j, edges=True):
		mat = self.grid
		adj = []
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				rangeX = range(0, len(mat))  # X bounds
				rangeY = range(0, len(mat[i])) # Y bounds

				(newX, newY) = (i+dx, j+dy) # adjacent cell    
				if (newX in rangeX) and (newY in rangeY) and (dx, dy) != (0, 0) and (edges or (abs(dy), abs(dx)) != (1, 1)):
					adj.append((newX, newY))

		return adj		

	def _calc_numbers(self):
		for row_n, row in enumerate(self.grid):
			next_mine = -1
			while '*' in row[next_mine+1:]:
				next_mine = row.index('*', next_mine+1)
				adj_inds = self._get_adj_inds(row_n, next_mine)
				for ind_i, ind_j in adj_inds:
					tile = self.grid[ind_i][ind_j]					
					if tile == '-':
						self.grid[ind_i][ind_j] = '1'
					elif tile != '*':
						self.grid[ind_i][ind_j] = str(int(tile)+1)
	
	def _get_valley_set(self, i, j, curr_set=None, replace_ch='.'):	
		curr_tile = self.grid[i][j]
			
		if curr_set is None:
			curr_set = set()
		curr_set.add((i, j))
		
		if curr_tile != '-':
			return curr_set

		self.grid[i][j] = replace_ch

		neighbors = self._get_adj_inds(i, j) # edges=False) maybe unnessary?
		for adj_i, adj_j in neighbors:
			curr_set.update(self._get_valley_set(adj_i, adj_j, curr_set, replace_ch))
		return curr_set

	def _get_valleys_old(self):
		nums = range(26)
		valleys = []
		for row_n, row in enumerate(self.grid):
			next_enterance = -1
			while '-' in row[next_enterance+1:]:
				next_enterance = row.index('-', next_enterance+1)
				valleys.append(self._get_valley_set(row_n, next_enterance)) # , replace_ch=string.ascii_uppercase[next(nums)]))

		return valleys

	def _add_valley_tile(self, i, j, valleys, enterances):
		tile = (i, j)
		#print('CT', tile)
		valley = None
		if tile in enterances:
			valley = enterances.get(tile)
			valley.append(tile)
		else:
			#print('happening!!!!!!!!!!!!!!')
			valleys.append([(tile)])
			valley = valleys[-1]

		#print('ADJs')
		for adj in self._get_adj_inds(*tile):	
			#print(adj)
			#print(valleys)
			if adj in enterances and enterances[adj] != valley:
				#print('FIXING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				#print('adj', adj, ':', enterances[adj])
				#print('val', valley)
				precursor_valley = enterances[adj]
				valley_n = valleys.index(precursor_valley)
				#print(valley)
				#print(precursor_valley)
				valley = precursor_valley
				precursor_valley.extend(valleys[valley_n])
				#print('oneeee', valley)
				#print('twoooo', precursor_valley)
			elif self.grid[adj[0]][adj[1]] == '-':
				enterances[adj] = valley

	def _add_valley_iter_dfs(self, i, j, valleys):
		new_valley = set()
		bounds = len(self.grid)
		visited = [False]*bounds**2
		stack = [i*bounds+j]

		self.grid[i][j] = '.'

		while len(stack):
			v = stack.pop()
			i, j = divmod(v, bounds)
			print(i, j)
			if not visited[v]:
				new_valley.add((i,j))
				visited[v] = True

			last = self.grid[i][j]
			for p, q in self._get_adj_inds(i, j):
				if visited[p*bounds+q]:
					continue
				if self.grid[p][q] == '-':
					self.grid[p][q] = '.'
					stack.append(p*bounds+q)
				elif self.grid[p][q] != '*' and last == '.': 
					stack.append(p*bounds+q)
		valleys.append(new_valley)


	def _get_valleys(self):
		valleys = []
		for i, row in enumerate(self.grid):
			for j, v in enumerate(row):
				if v == '-':

					self._add_valley_iter_dfs(i,j,valleys)
		print(valleys)
		return valleys

	def _get_valley_by_tile(self, pos: Position):
		for valley in self.valleys:
			if (pos.x, pos.y) in valley:
				return valley
		return -1

	def _print(self):
		for row in self.grid:
			print(' '.join(row))

	def _is_mine(self, pos: Position):
		return self.grid[pos.x][pos.y] == '*'

	def print(self):
		print(' '*2 + ' '.join(str(n) for n in range(1, 9)))
		for i, row in enumerate(self.viewable_grid):
			print(string.ascii_uppercase[i], ' '.join(row))

	def flag(self, pos: Position, unflag_if_flagged=False):
		print(self.viewable_grid)
		if self.viewable_grid[pos.x][pos.y] == '-':
			self.viewable_grid[pos.x][pos.y] = '#'
		elif self.viewable_grid[pos.x][pos.y] == '#' and unflag_if_flagged:
			self.unflag(pos)
	
	def unflag(self, pos: Position):
		if self.viewable_grid[pos.x][pos.y] == '#':
			self.viewable_grid[pos.x][pos.y] = '-'

	def remove_tile(self, pos: Position):
		real_tile = self.grid[pos.x][pos.y]
		to_apply = [(pos.x, pos.y)]
		if real_tile == '.':
			lake = self._get_valley_by_tile(pos)
			to_apply = lake
		for x, y in to_apply:
			self.viewable_grid[x][y] = self.grid[x][y]
			self.hidden_tiles.discard((x,y))
		return real_tile != '*'
	
	def is_completed_board(self):
		return len(self.hidden_tiles) == self.mine_count

	def play_game(self):
		print('Welcome to Minesweeper')
		while not self.is_completed_board():
			print('Current board:')
			self.print()
			c = input('\n'.join(["What would you like to do?", "->Explore a tile (E)", "->Place a flag (F)", "->Remove a flag (R)\n"]))
			if c.upper() not in ('E', 'F', 'R'):
				continue
			p = input('Enter a position (e.g. A3): ')
			pos = Position(p)
			
			if c.upper() == 'E':
				self.remove_tile(pos)
				if self._is_mine(pos):
					print("You hit a mine! You lose")
					return
			elif c.upper() == 'F':
				self.flag(pos)
			else:
				self.unflag(pos)




if __name__ == '__main__':
	g = Grid(debug_mode=True)
	if g.debug_mode:
		g.print()
		g.flag(Position.from_str('A5'))
		g.print()
		print('mmmm')
		#g._scatter_mines(10)
		#g._print()
		print('nnnn')
		#g._calc_numbers()
		g._print()
		g.grid = [['-','-','-','1','*','2','1','-',],
				['-','-','-','1','2','*','1','-',],
				['-','1','1','1','1','1','-','-',],
				['1','3','*','2','-','-','-','-',],
				['1','*','*','3','1','1','2','2',],
				['1','2','3','*','2','2','*','-',],
				['-','-','2','3','*','2','-','-',],
				['-','-','1','*','-','-','-','-',]]	
		print('oooo')
		g._print()
		lakes = g._get_valleys()
		g._print()
		for i, lake in enumerate(lakes):
			print(f"Lake {string.ascii_uppercase[i]}:", lake)
		a = 0
		while a < 2:
			g.print()
			p_str = input('Enter a position: ')
			g.remove_tile(Position.from_str(p_str))
			a += 1
	else:
		g.play_game()
