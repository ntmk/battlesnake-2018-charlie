from utils import neighbours, distance, check_ahead
from a_star import a_star
from defensive import find_my_tail, find_enemy_tail


SNAKE = 1
DANGER = 5
KILLABLE = 6


def eat_snake(charlie, enemies, grid):
  """
  If enemy is smaller will try to kill by moving into potential spots
  enemy head will be if enemy nest to wall will choke into crash\n
  
  @param charlie -> Own snake information\n
  @param enemies -> Array of enemy snakes\n
  @param grid -> Updated grid\n
  @return temp_path -> Path to eat enemy
  """
  for neighbour in neighbours(charlie['coords'][0], grid, 0, charlie['coords'], [SNAKE, DANGER]):
    if grid[neighbour[0]][neighbour[1]] == KILLABLE:
      kill_path = a_star(charlie['coords'][0], neighbour, grid, charlie['coords'], [SNAKE, DANGER])
      # return check_ahead(kill_path, charlie, neighbour, grid)
      return kill_path


def wall_kill(charlie, enemies, grid):
  """
  Checks if an enemy os on the wall and attempt to cut them off\n

  @param charlie -> Own snake information\n
  @param enemies -> Array of enemy snakes\n
  @param grid -> Updated grid\n
  @return temp_path -> Path for a wall kill
  """
  for enemy in enemies:
    for coords in charlie['coords'][2:]:
      for neighbour in neighbours(charlie['coords'][0], grid, 0, charlie['coords'][0], [SNAKE, DANGER]):
        if neighbour == (0, len(grid)-1) or neighbour == (0, 0) or neighbour == (len(grid[0])-1, len(grid)-1) or neighbour == (len(grid[0])-1, 0):
          continue
        for neigh in neighbours(neighbour, grid, 0, neighbour, [SNAKE]):
          temp_path = a_star(charlie['coords'][0], neigh, grid, charlie['coords'], [SNAKE, DANGER])
          if temp_path:
            if enemy['coords'][0][0] == 0 and enemy['coords'][0][1] == 	coords[1]-1:
              if charlie['coords'][0][0] == 0:
                continue
              if neighbour[0] == 0:
                path = [charlie['coords'][0], neighbour]
                return path
            if enemy['coords'][0][1] == 0 and enemy['coords'][0][0] == coords[0]-1:
              if charlie['coords'][0][1] == 0:
                continue
              if neighbour[1] == 0:
                path =  [charlie['coords'][0], neighbour]
                return path
            if enemy['coords'][0][1] == len(grid)-1 and enemy['coords'][0][1] == coords[1]+1:
              if charlie['coords'][0][1] == len(grid)-1:
                continue
              if neighbour[1] == len(grid)-1:
                path = [charlie['coords'][0], neighbour]
                return path
            if enemy['coords'][0][0] == len(grid[0])-1 and enemy['coords'][0][0] == coords[0]+1:
              if charlie['coords'][0][0] == len(grid[0])-1:
                continue
              if neighbour[0] == len(grid[0])-1:
                path = [charlie['coords'][0], neighbour]