from utils import distance, reconstruct_path, neighbours


def a_star(start, goal, grid, tail, ignore_list):
  """
  A-Star algorithm for pathfinding\n
  Originally from https://github.com/noahspriggs/battlesnake-python\n
  @param start -> Starting point\n
  @param goal -> End point\n
  @param grid -> Updated grid\n
  @param tail -> Tail of snake / additional coords to ignore\n
  @param ignore_list -> Grid locations to avoid
  """
  start = tuple(start)
  goal = tuple(goal)
  closed_set = []
  open_set   = [start]
  came_from = {} 
  
  g_score = [[10] * len(grid[0]) for _ in xrange(len(grid))]
  g_score[start[0]][start[1]] = 0
  
  f_score = [[10] * len(grid[0]) for _ in xrange(len(grid))]
  f_score[start[0]][start[1]] = distance(start,goal)

  while(len(open_set) > 0):
    current = min(open_set, key=lambda p: f_score[p[0]][p[1]])

    if (current == goal):
      return reconstruct_path(came_from, goal)
    open_set.remove(current)

    closed_set.append(current)
    
    for neighbour in neighbours(current, grid, int(g_score[current[0]][current[1]]), tail, ignore_list):
      if neighbour in closed_set:
        continue
      tentative_g_score = g_score[current[0]][current[1]] + distance(current,neighbour)
      if neighbour not in open_set:
        open_set.append(neighbour)
      elif tentative_g_score == g_score[neighbour[0]][neighbour[1]]:
        dx1 = current[0] - goal[0]
        dy1 = current[1] - goal[1]
        dx2 = start[0] - goal[0]
        dy2 = start[1] - goal[1]
        cross = abs(dx1*dy2 - dx2*dy1)
        tentative_g_score += cross*0.001
      elif tentative_g_score > g_score[neighbour[0]][neighbour[1]]:
        continue
      came_from[neighbour] = current
      g_score[neighbour[0]][neighbour[1]] = tentative_g_score
      f_score[neighbour[0]][neighbour[1]] = tentative_g_score + distance(neighbour,goal)

  return None