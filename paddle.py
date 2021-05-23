import pygame
from Config import Paddle_Values , screen_size
black = (0, 0, 0)

class Paddle(pygame.sprite.Sprite):

	def __init__(self , color=Paddle_Values.color, width=Paddle_Values.size_x, height=Paddle_Values.size_y):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		self.width = width
		self.height = height
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(black)
		self.image.set_colorkey(black)
		self.speed = Paddle_Values.speed
        # Draw a paddle
		pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

		self.rect = self.image.get_rect()

	def updatePaddleSize(self):
		if self.width == 10:
			return
		self.width -= 10
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(black)
		self.image.set_colorkey(black)
		pygame.draw.rect(self.image, Paddle_Values.color, [0, 0, self.width, self.height])
		self.rect = self.image.get_rect()


	def move_left(self):
		if(self.rect.x-self.speed<0):
			return
		self.rect.x-=Paddle_Values.speed
		if self.rect.x<0:
			self.rect = 0

	def move_right(self):
		if(self.rect.x+Paddle_Values.size_x+self.speed>screen_size[0]):
			return
		self.rect.x+=Paddle_Values.speed
		if self.rect.x + Paddle_Values.size_x > screen_size[0]:
			self.rect = screen_size[0] - Paddle_Values.size_x

