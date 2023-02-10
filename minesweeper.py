class Position:
	all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	p_table = {c: i for i, c in enumerate(all_letters)}
	
	def __init__(self, pos_str):
		self.x = self.p_table[pos_str[0].upper()]
		self.y = int(pos_str[1])

class Grid:
	def __init__(self):
		self.grid = [["-"]*8 for _ in range(8)]
		self.viewable_grid = [["-"]*8 for _ in range(8)]

	def __scatter_mines(self):
		for i, row in enumerate(self.grid):
			for j, col in enumerate(row):
				if j % 3 == 0:
					self.grid[i][j] = '*'
	def print(self):
		for row in self.viewable_grid:
			print(' '.join(row))

	def flag(self, pos_str):
		pos = Position(pos_str)
		if self.viewable_grid[pos.x][pos.y] == '-':
			self.viewable_grid[pos.x][pos.y] = 'F'
	
	def unflag(self, pos_str):
		pos = Position(pos_str)
		if self.viewable_grid[pox.x][pos.y] == 'F':
			self.viewable_grid[pos.x][pos.y] = '-'

	


if __name__ == '__main__':
	g = Grid()
	# g.print()
	g.flag('A5')
	g.print()
