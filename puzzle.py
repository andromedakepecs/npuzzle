import copy

# Andromeda Kepecs
# Redmond Block C

# Read txt file and return a tuple state
def LoadFromFile(filepath):
	state = []
	n = 0
	with open(filepath) as f:
		count = 0
		contains_hole = False
		for line in f:
			l = []
			if count == 0:
				n = f
			else:
				row = line.strip().split("\t")
				for i in row:
					if i == '*':
						l.append('0')
						contains_hole = True
					else:
						l.append(i)
				state.append(tuple(l))
			count += 1
		if contains_hole == False:
			print("Puzzle does not contain hole")
			return None
	return tuple(state)

def DebugPrint(state):
	for i in state:
		l = ""
		for j in i:
			l += j + "\t"
		print(l)

# Compute and return neighboring numbers 
def ComputeNeighbors(state):
	neighbors = []
	zero_coordinates = FindZero(state)
	row, col = zero_coordinates

	# Left
	if col - 1 >= 0:
		neighbors.append([state[row][col - 1], Swap(state, zero_coordinates, (row, col - 1))])
	# Right
	if col + 1 <= len(state) -1:
		neighbors.append([state[row][col + 1], Swap(state, zero_coordinates, (row, col + 1))])
	# Above
	if row - 1 >= 0:
		neighbors.append([state[row - 1][col], Swap(state, zero_coordinates, (row - 1, col))])
	# Below
	if row + 1 <= len(state) -1:
		neighbors.append([state[row + 1][col], Swap(state, zero_coordinates, (row + 1, col))])

	return neighbors

def FindZero(state):
	for i in range(len(state)):
		for j in range(len(state)):
			if state[i][j] == "0":
				return tuple([i, j])

def Swap(state, zero_coordinates, swap):
	new_state = list(list(row) for row in copy.deepcopy(state))
	zero_row, zero_col = zero_coordinates
	swap_row, swap_col = swap
	new_state[zero_row][zero_col], new_state[swap_row][swap_col] = new_state[swap_row][swap_col], new_state[zero_row][zero_col]
	return tuple(tuple(row) for row in new_state)

def IsGoal(state):
	index = 0
	n = len(state)
	for i in range(n):
		for j in range(n):
			if not int(state[i][j] == index + 1):
				return False
			if i == n - 1 and j == n -2:
				return True
			index += 1

def FindGoal(n):
	total = n * n
	count = 1
	end_state = []
	for i in range(n):
		row = []
		for j in range(n):
			if count == total:
				row.append('0')
			else:
				row.append(str(count))
			count += 1
		end_state.append(tuple(row))

	return tuple(end_state)

# Breadth First Search
def BFS(state):
	frontier = [(0, state)]
	discovered = set(state)
	parents = {(0, state): None}
	path = []
	while len(frontier) != 0:
		current_state = frontier.pop(0)
		discovered.add(current_state[1])
		if IsGoal(current_state[1]):
			while parents.get((current_state[0], current_state[1])) != None:
				path.insert(0, current_state[0])
				current_state = parents.get((current_state[0], current_state[1]))
			return path
		for neighbor in ComputeNeighbors(current_state[1]):
			if neighbor[1] not in discovered:
				frontier.append(neighbor)
				discovered.add(neighbor[1])
				parents.update({(neighbor[0], neighbor[1]): current_state})
	print("Failed")
	return None

# Depth First Search
def DFS(state):
	frontier = [(0, state)]
	discovered = set([state])
	parents = {(0, state): None}
	path = []
	while len(frontier) != 0:
		current_state = frontier.pop(0)
		discovered.add(current_state[1])
		if IsGoal(current_state[1]):
			while parents.get((current_state[0], current_state[1])) != None:
				path.insert(0, current_state[0])
				current_state = parents.get((current_state[0], current_state[1]))
			return path
		for neighbor in ComputeNeighbors(current_state[1]):
			if neighbor[1] not in discovered:
				frontier.insert(0, neighbor)
				discovered.add(neighbor[1])
				parents.update({(neighbor[0], neighbor[1]): current_state})
	print("Failed")
	return None

# Bidirectional Search
def BidirectionalSearch(state):
	goal = FindGoal(len(state))
	frontier1 = [(0, state)]
	frontier2 = [(0, goal)]
	discovered1 = set([state])
	discovered2 = set([goal])
	parents1 = {state: []}
	parents2 = {goal: []}
	while len(frontier1) != 0 or len(frontier2) != 0:
		current_state = frontier1.pop(0)
		current_end_state = frontier2.pop(0)

		discovered1.add(tuple(current_state[1]))
		discovered2.add(tuple(current_end_state[1]))

		intersection = list(discovered2.intersection(discovered1))
		if len(intersection) > 0:
			intersection_point = intersection[0]
			forward_path = parents1[intersection_point]
			backwards_path = list(reversed(parents2[intersection_point]))
			return forward_path + backwards_path
		
		for neighbor in ComputeNeighbors(current_state[1]):
			if neighbor[1] not in discovered1:
				frontier1.append(neighbor)
				discovered1.add(neighbor[1])
				parents1.update({neighbor[1]: parents1[current_state[1]] + [neighbor[0]]})
	
		for neighbor in ComputeNeighbors(current_end_state[1]):
			if neighbor[1] not in discovered2:
				frontier2.append(neighbor)
				discovered2.add(neighbor[1])
				parents2.update({neighbor[1]: parents2[current_end_state[1]] + [neighbor[0]]})
		
	print("Failed")
	return None

def AStar(state):
	pass

def main():
	puzzle = LoadFromFile('easy4.txt')
	print(puzzle)
	print(BidirectionalSearch(puzzle))

if __name__ == "__main__":
	main()