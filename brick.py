import random 
import pygame
from Config import *

black = (0,0,0)

colors = [RED, GREEN, BLUE, YELLOW, PURPLE, PINK, LIGHTBLUE, WHITE, BLACK] = [(227, 48, 48), (97, 204, 61), (63, 89, 235), (209, 166, 46),
        (151, 66, 255), (230, 34, 230), (29, 219, 197), (227, 209, 209), (40, 40, 40)]

nColors = len(colors)

class Brick(pygame.sprite.Sprite):

	def __init__(self, width=Brick_Values.size_x-Brick_Values.margin, height=Brick_Values.size_y-Brick_Values.margin):
        # Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([width, height])
		self.image.fill(black)
		self.image.set_colorkey(black)
		self.color =colors[random.randint(0, nColors-1)]
		self.level = None
		pygame.draw.rect(self.image, self.color, [0, 0, width, height])

		self.rect = self.image.get_rect()

	def pick_random_color(self):
		self.color =colors[random.randint(0, nColors-1)]
		self.image.fill(self.color)


def addLevel(all_brick,all_sprites_list,maxLevel):
	for brick in all_brick:
		brick.rect.y += int(Brick_Values.size_y)
		if brick.rect.y >= Paddle_Values.y:
			return True
	
	for x in range(0, screen_size[0], int(Brick_Values.size_x)):		
		brick = Brick()
		brick.rect.x = x + Brick_Values.margin
		brick.rect.y = int(Brick_Values.size_y) * (2 + Brick_Values.topMarginLayer) + Brick_Values.margin
		brick.level = maxLevel
		all_sprites_list.add(brick)
		all_brick.add(brick)

	return False

def createBricks(all_brick,all_sprites_list):
	levels = Brick_Values.columns
	for y in range(Brick_Values.columns):
		for x in range(0, screen_size[0], int(Brick_Values.size_x)):
			brick = Brick()
			brick.rect.x = x + Brick_Values.margin
			brick.rect.y = int(Brick_Values.size_y) * (y + 2 + Brick_Values.topMarginLayer) + Brick_Values.margin #CHANGE
			brick.level = levels
			all_sprites_list.add(brick)
			all_brick.add(brick)
		levels -= 1
		