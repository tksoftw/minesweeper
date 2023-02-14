class Position:
	all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	p_table = {c: i for i, c in enumerate(all_letters)}
	
	def __init__(self, pos_str):
		self.x = self.p_table[pos_str[0].upper()]
		self.y = int(pos_str[1])

class Grid:
	def __init__(self):
		self.grid = [['-']*8 for _ in range(8)]
		self.viewable_grid = [["-"]*8 for _ in range(8)]

	def _scatter_mines(self):
		for i, row in enumerate(self.grid):
			for j, col in enumerate(row):
				if i % 2 == 0 and j % 3 == 0:
					self.grid[i][j] = '*'

	def _get_adj_inds(self, i, j):
		adj = []
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				rangeX = range(0, len(self.grid))  # X bounds
				rangeY = range(0, len(self.grid[0]))  # Y bounds

				(newX, newY) = (i+dx, j+dy)  # adjacent cell    
				if (newX in rangeX) and (newY in rangeY) and (dx, dy) != (0, 0):
					adj.append((newX, newY))

		return adj		


	def _calc_numbers(self):
		for row in self.grid:
			next_mine = 0
			while '*' in row:
				next_mine = row.index('*', start=next_mine)

	def _print(self):
		for row in self.grid:
			print(' '.join(row))

	def print(self):
		for row in self.viewable_grid:
			print(' '.join(row))

	def flag(self, pos_str):
		pos = Position(pos_str)
		if self.viewable_grid[pos.x][pos.y] == '-':
			self.viewable_grid[pos.x][pos.y] = 'F'
	
	def unflag(self, pos_str):
		pos = Position(pos_str)
		if self.viewable_grid[pos.x][pos.y] == 'F':
			self.viewable_grid[pos.x][pos.y] = '-'

	


if __name__ == '__main__':
	g = Grid()
	# g.print()
	g.flag('A5')
	g.print()
	print('mmmm')
	g._scatter_mines()
	g._print()
	print(g._get_adj_inds(0,0))
