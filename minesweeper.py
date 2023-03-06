import random
import string

class Position:
	p_table = {c: i for i, c in enumerate(string.ascii_uppercase)}
	
	def __init__(self, pos_str):
		self.x = self.p_table[pos_str[0].upper()]
		self.y = int(pos_str[1])

class Grid:
	def __init__(self):
		self.grid = [['-']*8 for _ in range(8)]
		self.viewable_grid = [["-"]*8 for _ in range(8)]
		self.lakes = []


	def _scatter_mines(self):
		for _ in range(10):
			i = random.randint(0, len(self.grid)-1)
			j = random.randint(0, len(self.grid[i])-1)
			self.grid[i][j] = '*'

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
	
	def _get_lake_set(self, i, j, curr_set=None, replace_ch='.'):	
		curr_tile = self.grid[i][j]
		if curr_tile != '-':
			return curr_set

		self.grid[i][j] = replace_ch
		if curr_set is None:
			curr_set = set()
		curr_set.add((i, j))
		
		neighbors = self._get_adj_inds(i, j, edges=False)
		for adj_i, adj_j in neighbors:
			curr_set.update(self._get_lake_set(adj_i, adj_j, curr_set, replace_ch))
		return curr_set


	def _get_lakes(self):
		ch_n = 0
		lakes = []
		for row_n, row in enumerate(self.grid):
			next_mouth = -1
			while '-' in row[next_mouth+1:]:
				next_mouth = row.index('-', next_mouth+1)
				lakes.append(self._get_lake_set(row_n, next_mouth)) # , replace_ch=string.ascii_uppercase[ch_n]))
				ch_n += 1

		return lakes

	def _get_lake_by_tile(self, pos: Position):
		for lake in lakes:
			if (pos.x, pos.y) in lake:
				return lake
		raise ValueError(f"No lake found containing tile: ({pos.x}, {pos.y})")

	def _get_extended_lake(self, lake):
		# Assuming lake in lakes
		edge_numbers = []
		adjs = set()
		for x, y in lake:
			adjs = self._get_adj_inds(x, y)
			if adjs != set(lake):

	def _print(self):
		for row in self.grid:
			print(' '.join(row))

	def print(self):
		print(' '*2 + ' '.join(str(n) for n in range(8)))
		for i, row in enumerate(self.viewable_grid):
			print(string.ascii_uppercase[i], ' '.join(row))

	def flag(self, pos_str):
		pos = Position(pos_str)
		if self.viewable_grid[pos.x][pos.y] == '-':
			self.viewable_grid[pos.x][pos.y] = '#'
	
	def unflag(self, pos_str):
		pos = Position(pos_str)
		if self.viewable_grid[pos.x][pos.y] == '#':
			self.viewable_grid[pos.x][pos.y] = '-'

	def remove_tile(self, pos_str):
		pos = Position(pos_str)
		real_tile = self.grid[pos.x][pos.y]
		to_apply = [(pos.x, pos.y)]
		if real_tile == '.':
			print("you found a lake!")
			lake = self._get_lake_by_tile(pos)
			to_apply = lake
		for x, y in to_apply:
			self.viewable_grid[x][y] = real_tile
		
	




if __name__ == '__main__':
	g = Grid()
	g.print()
	g.flag('A5')
	g.print()
	print('mmmm')
	g._scatter_mines()
	g._print()
	print('nnnn')
	g._calc_numbers()
	g._print()
	print('oooo')
	lakes = g._get_lakes()
	g._print()
	for i, lake in enumerate(lakes):
		print(f"Lake {string.ascii_uppercase[i]}:", lake)
	a = 0
	while a < 10:
		g.print()
		p = input('Enter a position: ')
		g.remove_tile(p)
