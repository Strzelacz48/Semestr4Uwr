class Cell(object):
    index: int
    cell_type: int
    resources: int
    neighbors: list[int]
    my_ants: int
    opp_ants: int

    def __init__(self, index: int, cell_type: int, resources: int, neighbors: list[int], my_ants: int, opp_ants: int):
        self.index = index
        self.cell_type = cell_type
        self.resources = resources
        self.neighbors = neighbors
        self.my_ants = my_ants
        self.opp_ants = opp_ants



def closest_eggs_bfs(base_idx: int):
    visited: list[int] = []
    queue: list[int] = [base_idx]
    while len(queue) > 0:
        current = queue.pop(0)
        visited.append(current)
        #actions.append(f'MESSAGE BFS {current}')
        for neighbor in cells[current].neighbors:
            #actions.append(f'MESSAGE BFS2 {neighbor}')
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                if cells[neighbor].cell_type == 1 and cells[neighbor].resources > 0:
                    return neighbor
    return cell.index

def closest_gems_bfs(base_idx: int):
    cell = cells[base_idx]
    visited: list[int] = []
    queue: list[int] = [cell.index]
    while len(queue) > 0:
        current = queue.pop(0)
        visited.append(current)
        for neighbor in cells[current].neighbors:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                if cells[neighbor].cell_type == 2 and cells[neighbor].resources > 0:
                    return neighbor
    return cell.index

def dist_to_base(cell_idx: int, base_idx: int):
    visited: list[int] = []
    queue: list[int] = [cell_idx]
    dist = 0
    while len(queue) > 0:
        current = queue.pop(0)
        visited.append(current)
        for neighbor in cells[current].neighbors:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                dist += 1
                if neighbor == base_idx:
                    return dist
    return dist

def my_total_ants():
    total = 0
    for cell in cells:
        total += cell.my_ants
    return total

#returns idx of all cells that we pass while going from start to end
def find_path_dfs(start_idx: int, end_idx: int, path_taken: list[int], visited: list[int]):
    if start_idx == end_idx:
        return path_taken
    visited.append(start_idx)
    for neighbor in cells[start_idx].neighbors:
        if neighbor not in visited:
            path_taken.append(neighbor)
            return find_path_dfs(neighbor, end_idx, path_taken, visited)
    return path_taken
    
def how_long_same_path(idx1: int, idx2: int):
    path1 = find_path_dfs(my_bases[0], idx1, [my_bases[0]], [])
    path2 = find_path_dfs(my_bases[0], idx2, [my_bases[0]], [])
    if len(path1) > len(path2):
        return len(path1)
    else:
        return len(path2)

def wasteland(cell_idx: int):
    cell = cells[cell_idx]
    if cell.cell_type != 0 and cell.resources > 0:
        return False
    active_neighbors = 0
    for neighbor in cell.neighbors:
        if cells[neighbor].my_ants > 0:
            active_neighbors += 1
        if active_neighbors > 1:
            return False
    return True

cells: list[Cell] = []

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    inputs = [int(j) for j in input().split()]
    cell_type = inputs[0] # 0 for empty, 1 for eggs, 2 for crystal
    initial_resources = inputs[1] # the initial amount of eggs/crystals on this cell
    neigh_0 = inputs[2] # the index of the neighbouring cell for each direction
    neigh_1 = inputs[3]
    neigh_2 = inputs[4]
    neigh_3 = inputs[5]
    neigh_4 = inputs[6]
    neigh_5 = inputs[7]
    cell: Cell = Cell(
        index = i,
        cell_type = cell_type,
        resources = initial_resources,
        neighbors = list(filter(lambda id: id > -1,[neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5])),
        my_ants = 0,
        opp_ants = 0
    )
    cells.append(cell)
number_of_bases = int(input())
my_bases: list[int] = []
for i in input().split():
    my_base_index = int(i)
    my_bases.append(my_base_index)
opp_bases: list[int] = []
for i in input().split():
    opp_base_index = int(i)
    opp_bases.append(opp_base_index)

turn = 0

cell_distances: list[int, int] = []
for cell in cells:
    cell_distances.append((dist_to_base(cell.index, my_bases[0]), cell.index))

cell_distances_unsorted = cell_distances.copy()
cell_distances.sort(key=lambda x: x[0])

all_eggs_cells: int = 0
egg_cell_idx: list[int] = []
all_crystals_cells: int = 0
crystal_cell_idx: list[int] = []
for cell in cells:
    if cell.cell_type == 1:
        all_eggs_cells += 1
        egg_cell_idx.append(cell.index)
    elif cell.cell_type == 2:
        all_crystals_cells += 1
        crystal_cell_idx.append(cell.index)

past_actions: list[str] = []
commited_cells: list[int] = []

# game loop
n = 0
while True:
    turn += 1
    for i in range(number_of_cells):
        inputs = [int(j) for j in input().split()]
        resources = inputs[0] # the current amount of eggs/crystals on this cell
        my_ants = inputs[1] # the amount of your ants on this cell
        opp_ants = inputs[2] # the amount of opponent ants on this cell

        cells[i].resources = resources
        cells[i].my_ants = my_ants
        cells[i].opp_ants = opp_ants

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    actions = []

    # TODO: choose actions to perform and push them into actions. E.g:
    #===========================================================================
    if turn == 1:
        n = 3

    for tup in cell_distances:
        cell = cells[tup[1]]
        if cell.resources > 0 and n> 0 and cell.index not in commited_cells:
            cell_distances.remove(tup)
            n -= 1
            past_actions.append(f'LINE {my_bases[0]} {cell.index} 2')
            commited_cells.append(cell.index)

    for idx in commited_cells:
        #actions.append(f'MESSAGE {idx}')
        if cells[idx].my_ants > 0:
            #actions.append(f'MESSAGE removed : {idx}')
            commited_cells.remove(idx)
            n += 1


    actions.extend(past_actions)
    #if cell_distances_unsorted[closest_egg][0] < all_my_ants:
    #    actions.append(f'LINE {my_bases[0]} {closest_egg} 3')
    #    if cell_distances_unsorted[closest_gem][0] <= all_my_ants - cell_distances_unsorted[closest_egg][0] + how_long_same_path(closest_egg, closest_gem):
    #        actions.append(f'LINE {my_bases[0]} {closest_gem} 3')

    #if turn < 15 and closest_egg != my_bases[0]:
        #actions.append(f'MESSAGE EGGS')
        #actions.append(f'LINE {my_bases[0]} {closest_egg} 3')
    
        
    

    

    """

    all_my_ants = my_total_ants()

    closest_egg = closest_eggs_bfs(my_bases[0])
    closest_gem = closest_gems_bfs(my_bases[0])

    

    #collecting direct resources
    for neigh in cells[my_bases[0]].neighbors :
        if cells[neigh].cell_type != 0  and f'BEACON {neigh} 2' not in past_actions: #and cells[neigh].resources > 0:
            past_actions.append(f'BEACON {neigh} 2')
            break
        
    #zaczynamy od najblizszych kryształów
    if closest_gem != my_bases[0] and cells[closest_gem].resources > 0:
        #actions.append(f'MESSAGE GEMS')
        if f'LINE {my_bases[0]} {closest_gem} 2' not in past_actions:
            past_actions.append(f'LINE {my_bases[0]} {closest_gem} 2')

    #zaczynamy od najblizszych jaj
    if closest_egg != my_bases[0] and cells[closest_egg].resources > 0:
        #actions.append(f'MESSAGE EGGS')
        if f'LINE {my_bases[0]} {closest_egg} 2' not in past_actions:
            past_actions.append(f'LINE {my_bases[0]} {closest_egg} 2')

    for cell in cells:

for cell_idx in cell_distances:
            cell = cells[cell_idx[1]]
            if cell.index == cell_idx[1] and cell.resources > 0 and used_ants < all_my_ants:
                break

    for cell in cells:
        
        
            break
        elif cell.resources > 0 and not is_close_to_base(cell, my_bases):
            actions.append(f'MESSAGE CELLS')
            actions.append(f'LINE {my_bases[0]} {cell.index} 2')
            break
    """
    #==============================================================================
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    if len(actions) == 0:
        print('WAIT')
    else:
        print(';'.join(actions))

        """

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
number_of_bases = int(input())
for i in input().split():
    my_base_index = int(i)
for i in input().split():
    opp_base_index = int(i)

# game loop
while True:
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    print("WAIT")

        """