def print_grid(grid, title):
  """
  Reformats and correctly display grid in console for debugging purposes\n
  
  @param grid -> Game board represented as a grid
  """
  new_grid = []
  row = []
  for x in xrange(len(grid)):
    for y in xrange(len(grid[0])):
      if len(row) == len(grid[0]):
        row = []
      char = grid[y][x]
      row.append(char)
    new_grid.append(row)
  print('Game: %s' % title)
  for row in new_grid:
    print(row)


def direction(from_cell, to_cell):
  """
  Determine which direction to move\n

  @param from_cell -> Current cell occupied\n
  @param to_cell -> Destination cell\n
  @returns -> Direction to move\n
  """
  dx = to_cell[0] - from_cell[0]
  dy = to_cell[1] - from_cell[1]

  if dx == 1:
    return 'right'
  elif dx == -1:
    return 'left'
  elif dy == -1:
    return 'up'
  elif dy == 1:
    return 'down'


def distance(p, q):
  """
  Manhattan distance between two points\n

  @param start -> Coordinates of starting point\n
  @param goal -> Coordinates of ending / goal point\n
  @returns -> Distance between cells
  """
  dx = abs(p[0] - q[0])
  dy = abs(p[1] - q[1])
  return dx + dy


def reconstruct_path(came_from, current):
  """
  Helper method for astar to determine path\n

  @param came_from -> Cells searched while finding path\n
  @param current -> Current node where snake head is\n
  @returns total_path -> Reversed list of coordinates to goal
  """
  total_path = [current]
  while current in came_from.keys():
    current =  came_from[current]
    total_path.append(current)
  return list(reversed(total_path))


def neighbours(node, grid, score, tail, ignore_list):
  """
  Retrieve a list of cells around a specific node\n
  Originally from https://github.com/noahspriggs/battlesnake-python\n

  @param node -> Current cell\n
  @param grid -> Current state of the game board\n
  @param score -> TODO - remove if possible not really needed\n
  @param tail -> Coords of snake body used for filter\n
  @param ignore_list -> Danger cells on grid\n
  @returns result -> Array of available connected cells\n
  """
  width = len(grid)
  height = len(grid[0])
  subtail = []
  if score >= len(tail):
    subtail = [tuple(x) for x in tail]
  else:
    subtail = [tuple(x) for x in tail[len(tail)-score:]]
  result = []
  if (node[0] > 0):
    result.append((node[0]-1,node[1]))
  if (node[0] < width-1):
    result.append((node[0]+1,node[1]))
  if (node[1] > 0):
    result.append((node[0],node[1]-1))
  if (node[1] < height-1):
    result.append((node[0],node[1]+1))
  result = filter(lambda p: (grid[p[0]][p[1]] not in ignore_list) or (p in subtail), result)
  return result

# TODO - add path to enemy tail as well maybe even smaller snake head
def check_ahead(tentative_path, charlie, next_move, grid):
  """
  Ensure we have a path to our tail from next move\n
  Originally from https://github.com/noahspriggs/battlesnake-python\n
  
  @param tentative_path -> Potential path to take\n
  @param Charlie -> Own snake information\n
  @param next_move -> Own snakes next move\n
  @param grid -> Updated grid\n
  @return path -> The path if safe to take
  """
  from a_star import a_star
  import copy
  SAFE = 0
  FOOD = 3
  SNAKE = 1
  DANGER = 5
  path_length = len(tentative_path)
  my_length = charlie['length']+1
  if path_length < my_length:
    remainder = my_length - path_length
    my_new_coords = list(reversed(tentative_path)) + charlie['coords'][:remainder]
  else:
    my_new_coords = list(reversed(tentative_path))[:my_length]
  if grid[my_new_coords[0][0]][my_new_coords[0][1]] == FOOD:
    my_new_coords.append(my_new_coords[-1])
  new_grid = copy.deepcopy(grid)
  for coord in charlie['coords']:
    new_grid[coord[0]][coord[1]] = SAFE
  for coord in my_new_coords:
    new_grid[coord[0]][coord[1]] = SNAKE
  path_to_tail = a_star(next_move, my_new_coords[-1], new_grid, my_new_coords, [SNAKE, DANGER])
  if path_to_tail:
    return tentative_path