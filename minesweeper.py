import random
import string

class Position:
	p_table = {c: i for i, c in enumerate(string.ascii_uppercase)}
	
	def __init__(self, pos_str):
		self.x = self.p_table[pos_str[0].upper()]
		self.y = int(pos_str[1])-1 # accounting for 0-indexing

class Grid:
	def __init__(self, dim=8):
		self.grid = [['-']*dim for _ in range(dim)]
		self.viewable_grid = [["-"]*dim for _ in range(dim)]
		self.hidden_tiles = {(i,j) for j in range(dim) for i in range(dim)}
		self.mine_count = 0
		self.valleys = []

		# prep functions
		self._scatter_mines()
		self._calc_numbers()
		self.valleys = self._get_valleys()

	def _scatter_mines(self):
		for _ in range(10):
			i = random.randint(0, len(self.grid)-1)
			j = random.randint(0, len(self.grid[i])-1)
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

	def _get_valleys(self):
		nums = range(26)
		valleys = []
		for row_n, row in enumerate(self.grid):
			next_enterance = -1
			while '-' in row[next_enterance+1:]:
				next_enterance = row.index('-', next_enterance+1)
				valleys.append(self._get_valley_set(row_n, next_enterance)) # , replace_ch=string.ascii_uppercase[next(nums)]))

		return valleys

	def _get_valley_by_tile(self, pos: Position):
		for valley in self.valleys:
			if (pos.x, pos.y) in valley:
				return valley
		raise ValueError(f"No valley found containing tile: ({pos.x}, {pos.y})")

	def _print(self):
		for row in self.grid:
			print(' '.join(row))

	def _is_mine(self, pos: Position):
		return self.grid[pos.x][pos.y] == '*'

	def print(self):
		print(' '*2 + ' '.join(str(n) for n in range(1, 9)))
		for i, row in enumerate(self.viewable_grid):
			print(string.ascii_uppercase[i], ' '.join(row))

	def flag(self, pos: Position):
		if self.viewable_grid[pos.x][pos.y] == '-':
			self.viewable_grid[pos.x][pos.y] = '#'
	
	def unflag(self, pos: Position):
		if self.viewable_grid[pos.x][pos.y] == '#':
			self.viewable_grid[pos.x][pos.y] = '-'

	def remove_tile(self, pos: Position):
		real_tile = self.grid[pos.x][pos.y]
		to_apply = [(pos.x, pos.y)]
		if real_tile == '.':
			print("you found a lake!")
			lake = self._get_valley_by_tile(pos)
			to_apply = lake
		for x, y in to_apply:
			self.viewable_grid[x][y] = self.grid[x][y]
			self.hidden_tiles.discard((x,y))
	
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
	g = Grid()
	#g.print()
	#g.flag(Position('A5'))
	#g.print()
	#print('mmmm')
	#g._scatter_mines()
	#g._print()
	#print('nnnn')
	#g._calc_numbers()
	#g._print()
	#print('oooo')
	#lakes = g._get_valleys()
	#g._print()
	#for i, lake in enumerate(lakes):
	#	print(f"Lake {string.ascii_uppercase[i]}:", lake)
	#a = 0
	#while a < 2:
	#	g.print()
	#	p = input('Enter a position: ')
	#	g.remove_tile(Position(p))
	#	a += 1
	g.play_game()
