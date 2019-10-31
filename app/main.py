import bottle
import copy
import math
import os
import json
from api import start_response, move_response, end_response, ping_response
from a_star import a_star, neighbours
from utils import distance, neighbours, print_grid, direction
from defensive import find_my_tail, trouble, find_enemy_tail, eat_food, find_my_tail_emergency
from offensive import wall_kill, eat_snake

SAFTEY = 0
SNAKE = 1
FOOD = 3
DANGER = 5
KILLABLE = 6


# def log(message, variable):
# 	print(message, variable)


def convert_data(data):
	"""
	Reduce bloat of incoming json data
	"""
	food = []
	enemies = []
	for i in data['board']['food']:
		food.append([i['x'], i['y']])
	for snake in data['board']['snakes']:
		coords = []
		for i in snake['body']:
			coords.append([i['x'], i['y']])
		snake = {
			"id": snake['id'],
			"health": snake['health'],
			"coords": coords,
			"length": len(coords)
		}
		if snake['id'] == data['you']['id']:
			charlie = snake
		else:
			enemies.append(snake)

	food = sorted(food, key = lambda p: distance(p, charlie['coords'][0]))
	enemies = sorted(enemies, key = lambda p: p['length'])
	
	return food, charlie, enemies


def init(data):
	"""
	Initialize grid and update cell values\n

	@param data -> Json response from bottle\n
	@return game_id -> Game id for debuggin purposes when displaying grid\n
	@return grid -> Grid with updated cell values\n
	@return food -> Sorted array of food by closest to charlie\n
	@return charlie -> My snake\n
	@return enemies -> Array of all enemy snakes
	"""
	food, charlie, enemies = convert_data(data)

	game_id = data['game']['id']
	grid = [[0] * data['board']['height'] for _ in xrange(data['board']['width'])]

	for f in food:
		grid[f[0]][f[1]] = FOOD

	for coord in charlie['coords']:
		grid[coord[0]][coord[1]] = SNAKE
	if charlie['health'] < 100 and charlie['length'] > 2 and data['turn'] >= 3:
			grid[charlie['coords'][-1][0]][charlie['coords'][-1][1]] = SAFTEY

	for enemy in enemies:
		for coord in enemy['coords']:
			grid[coord[0]][coord[1]] = SNAKE
			for neighbour in neighbours(enemy['coords'][0], grid, 0, enemy['coords'][-1], [1]):
				if enemy['length'] >= charlie['length']:
					grid[neighbour[0]][neighbour[1]] = DANGER
				else:
					grid[neighbour[0]][neighbour[1]] = KILLABLE
		if enemy['health'] < 100 and enemy['length'] > 2 and data['turn'] >= 3:
			grid[enemy['coords'][-1][0]][enemy['coords'][-1][1]] = SAFTEY

	return game_id, grid, food, charlie, enemies


@bottle.post('/ping')
def ping():
		return ping_response()


@bottle.post('/start')
def start():
		color = "#00fff9"
		return start_response(color)


@bottle.post('/move')
def move():
	data = bottle.request.json
	
	game_id, grid, food, charlie, enemies = init(data)
	
	# TODO - thhe print grid function does not work on rectangles
	# print_grid(grid, game_id)

	# # Only check eat kills if length greater than 3
	if charlie['length'] >= 3 and charlie['health'] >= 20:
	  path = eat_snake(charlie, enemies, grid)
	  if path:
	    # log('eat snake path ', path)
	    return move_response(direction(path[0], path[1]))

	# # Only check wall kills if length greater than 3
	if charlie['length'] >= 3 and charlie['health'] >= 20:
	  path = wall_kill(charlie, enemies, grid)
	  if path:
	    # log('wall kill path ', path)
	    return move_response(direction(path[0], path[1]))

	# Eat food when length or health below threshhold
	if len(enemies) >= 2 or charlie['length'] <= 30 or charlie['health'] <= 60:
		path = eat_food(charlie, grid, food)
		if path:
			# log('eat path ', path)
			return move_response(direction(path[0], path[1]))

	# # if our length is greater than threshold and no other path was available
	if charlie['length'] >= 3:
	  path = find_my_tail(charlie, grid)
	  if path:
	    # log('find my tail path ', path)
	    return move_response(direction(path[0], path[1]))

	# # if no path available to tail check if there is an enemies available
	if not path:
	  path = find_enemy_tail(charlie, enemies, grid)
	  if path:
	    # log('find enemy tail path ', path)
	    return move_response(direction(path[0], path[1]))

	# # if our length is greater than threshold and no other path was available
	if charlie['length'] >= 3:
	  path = find_my_tail_emergency(charlie, grid)
	  if path:
	    # log('find my tail emergency path ', path)
	    return move_response(direction(path[0], path[1]))

	# Choose a random free space if no available enemy tail
	if not path:
		path = trouble(charlie, grid)
		if path:
			# log('trouble path ', path)
			return move_response(direction(path[0], path[1]))


@bottle.post('/end')
def end():
		return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'), quiet = True)
