import pygame
import sys
import random
import time

# --- Globals  Variables ---
# Set screen width and height
screen_width = 500
screen_height = 500

# Colors
bg_color = (237, 215, 14)
snake_color = (113, 50, 168)
food_color = (255, 0, 0)

# Set the no. of rows in the game
row = 20
speed = screen_width//row

# Set the width and height of each snake segment
segment_width = 20
segment_height = 20
# Margin between each segment
segment_margin = 3

	
class Cube(pygame.sprite.Sprite):
	""" Class to rep single block of snake body and food. Inherited from Sprite Class"""
	def __init__(self, x, y, color):
		super().__init__()
		self.image = pygame.Surface((segment_width, segment_height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Snake(object):
	"""docstring for Snake"""
	def __init__(self):
		super(Snake, self).__init__()
		self.score = 0
		self.score_point = 1

		# The change in movement in both direction
		self.x_change = speed
		self.y_change = 0

		# Create a sprite group for the snake 
		self.snake_group = pygame.sprite.Group()
		self.snake_body = []

		# Create an intial Snake
		for i in range(3):
			x = 75 - (i*speed) + segment_margin
			y = speed + segment_margin
			segment = Cube(x, y, snake_color)
			self.snake_body.append(segment)  
			self.snake_group.add(segment)    

	def move_snake(self):
		# Remove the last block from the list and group
		last_segment = self.snake_body.pop()           
		self.snake_group.remove(last_segment)

		# Figure out the where the head next be 
		x = self.snake_body[0].rect.x + self.x_change
		y = self.snake_body[0].rect.y + self.y_change
		segment = Cube(x, y, snake_color)
		self.snake_body.insert(0, segment)  # Insert the new head into the list at index 0
		self.snake_group.add(segment)       # and add it to the group

	def is_hit(self):
		# Check whether the snake hit with its own body
		for body in self.snake_body[2:]:
			if self.snake_body[0].rect.colliderect(body.rect):
				return True
		# Check whether the snake hit the border
		if self.snake_body[0].rect.x < 0 or self.snake_body[0].rect.x >= screen_width \
			or self.snake_body[0].rect.y < 0 or self.snake_body[0].rect.y >= screen_height:
			return True
		return False

	def eat(self, food):
		if self.snake_body[0].rect.colliderect(food):
			self.score += self.score_point
			food.rect.topleft = [random.choice(food_positions)+ segment_margin, random.choice(food_positions)+ segment_margin]

			x = self.snake_body[-1].rect.x 
			y = self.snake_body[-1].rect.y 
			segment = Cube(x, y, snake_color)
			self.snake_body.insert(-1, segment)
			self.snake_group.add(segment)

	def reset(self):
		for body in self.snake_body[3:]:
				segment = self.snake_body.pop()
				self.snake_group.remove(segment)

		self.snake_body[0].rect.topleft = (75+3, 25+3)
		self.x_change = speed
		self.y_change = 0 

	def draw(self, screen):
		self.snake_group.draw(screen)

# Create food for the snake
food_positions = [x for x in range(0, 500, speed)]
food_group = pygame.sprite.Group()
food = Cube(random.choice(food_positions)+ segment_margin, random.choice(food_positions)+ segment_margin, food_color)
food_group.add(food)

def grid():
	cube_size = screen_width//row
	colors = [[(102,255,102) if y%2 == x%2 else (31,255,31) for y in range(row)] for x in range(row)]

	for i in range(row):
		for j in range(row):
			pygame.draw.rect(screen, colors[i][j], (i*cube_size, j*cube_size, cube_size, cube_size))

# Create a snake object
snake = Snake()

class Gamestate(object):
	"""Class for diferent game stages"""
	def __init__(self):
		super(Gamestate, self).__init__()
		self.state = 'main_state'
		self.pause = True
		self.snake_score = 0

	# To handle different states in the gamestates
	def state_manager(self):
		if self.state == 'main_state':
			self.main_state()
		elif self.state == 'score_state':
			self.score_state()

	def main_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				self.pause = False
				if event.key == pygame.K_LEFT and snake.x_change <= 0:
					snake.x_change = speed * -1
					snake.y_change = 0
				if event.key == pygame.K_RIGHT and snake.x_change >= 0:
					snake.x_change = speed
					snake.y_change = 0
				if event.key == pygame.K_UP and snake.y_change <= 0 :
					snake.x_change = 0
					snake.y_change = speed * -1
				if event.key == pygame.K_DOWN and snake.y_change >= 0 :
					snake.x_change = 0
					snake.y_change = speed
				if event.key == pygame.K_SPACE:
					self.pause = True
					
		if not self.pause:
			snake.move_snake()

		# Avoid food appearing on the body of the snake
		for body in snake.snake_body[2:]:
			if body.rect.colliderect(food.rect):
				food.rect.topleft = [random.choice(food_positions)+segment_margin ,random.choice(food_positions)+segment_margin ]

		if snake.is_hit():
			snake.reset()
			self.state = 'score_state'
			self.snake_score = snake.score
			snake.score = 0
			food.rect.topleft = [random.choice(food_positions)+segment_margin ,random.choice(food_positions)+segment_margin ]
			time.sleep(2)

		snake.eat(food)

		# --- Draw ---
		screen.fill(bg_color)
		grid()

		food_group.draw(screen)
		snake.draw(screen)

		pygame.display.update()	

	def score_state(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.state = 'main_state'

		# --- Draw ---
		print(self.snake_score)
		screen.fill((0,100,100, 128))
		pygame.display.update()	


# Gamescreen setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
gamestate = Gamestate()

# Game loop
while True:
	gamestate.state_manager()

	clock.tick(10)


