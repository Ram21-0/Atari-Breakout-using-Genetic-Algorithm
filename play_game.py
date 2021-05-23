import pygame
import sys
import os
import time
from paddle import Paddle
from ball import Ball
from brick import *
from Config import *
from GeneticAlgorithm import *

def make_video(screen):
	_image_num = 0
	while True:
		_image_num += 1
		str_num = "000" + str(_image_num)
		file_name = "image" + str_num[-4:] + ".jpg"
		pygame.image.save(screen, file_name)
		print("In generator ", file_name)  # delete, just for demonstration
		pygame.time.wait(1000)  # delete, just for demonstration
		yield

## AI

screen = pygame.display.set_mode(screen_size)
hits = 0
maxHits = 30
score = 0
highScore = 0

# ouch = pygame.mixer.Sound('wee.ogg')

def playLoaded(live,runWithWeights=False):
	global lives, highScore, hits
	pygame.init()
	pygame.display.set_caption("Brick and Ball")

	all_sprites_list = pygame.sprite.Group()

	points = [0] 
	lives = live 
	exit = True 
	
	screen.fill(background_color)

	paddle = Paddle()
	paddle.rect.x = Paddle_Values.x
	paddle.rect.y = Paddle_Values.y

	ball = Ball(2*Ball_Values.radius, 2*Ball_Values.radius)
	# ball.rect.x = random.randint(100,700) #Ball_Values.center[0] - Ball_Values.radius
	ball.rect.x = 522
	# print("rect x = ",ball.rect.x)
	ball.rect.y = Ball_Values.center[1] - Ball_Values.radius

	#adding bricks
	levels = Brick_Values.columns
	maxLevel = levels
	all_brick = pygame.sprite.Group()

	createBricks(all_brick,all_sprites_list)
	all_sprites_list.add(paddle)
	all_sprites_list.add(ball)

	make_video(screen)

	while exit:
		
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				exit = False
				return "QUIT"
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			paddle.move_left()
		if keys[pygame.K_RIGHT]:
			paddle.move_right()

		ball.walls()
		
		if runWithWeights:
			if specimen.output(getInputVector(ball, paddle)) > 0.5:
				paddle.move_right()
			else:
				paddle.move_left()

		if ball.bottom_line():
			print("score = ",points)
			lives -= 1
			if lives == 0:
				return
				
		if paddle.rect.colliderect(ball.rect):
			if ball.movement[1] < 0:
				ball.movement[1] *= -1
				# m1 = paddle.rect.x + Paddle_Values.size_x/2 + 
			hits += 1
			if hits == maxHits:
				return

		brick_collison_list = pygame.sprite.spritecollide(ball, all_brick, False)
		for brick in brick_collison_list:

			#CHANGE

			# if ball.rect.x + 5 < brick.rect.x + Brick_Values.size_x and ball.rect.x + 2*Ball_Values.radius - 5 > brick.rect.x:
				# if ball.movement[1] > 0:
				# 	ball.movement[1] *= -1
			# else:
			# 	ball.movement[0] *= -1

			if not (ball.rect.x + 5 < brick.rect.x + Brick_Values.size_x and ball.rect.x + 2*Ball_Values.radius - 5 > brick.rect.x):
				ball.movement[0] *= -1
			ball.movement[1] *= -1

			points[0] += brick.level
			
			# pygame.mixer.Sound.play(ouch)
			
			if hits < maxHits:
				hits = 0
			
			brick.kill()
			# CHANGE
			if len(all_brick) < 40:
				hitsBottom = addLevel(all_brick,all_sprites_list,maxLevel)
				if hitsBottom:
					# game over
					print("score = ",points)
					return
				maxLevel += 1

			#CHANGE
			if maxLevel%10 == 0:
				if maxLevel/10 != (100 - paddle.width)/10:
					xx, yy = paddle.rect.x, paddle.rect.y
					paddle.updatePaddleSize()
					paddle.rect.x = xx
					paddle.rect.y = yy

			if len(all_brick) == 0:

				screen.fill(background_color)
				font = pygame.font.Font(None, 74)
				text = font.render("LEVEL COMPLETE", 1, black)
				screen.blit(text, (135, 165))

				font = pygame.font.Font(None, 60)
				highScore = max(points[0], highScore)
				text = font.render("Score: " + str(points[0]), 1, black)
				screen.blit(text, (215, 250))
				counterEnd = 0
				while counterEnd <= FPS*3:
					counterEnd += 1
					for event in pygame.event.get(): 
						if event.type == pygame.QUIT:
							pygame.quit()
							sys.exit() 

				return

		all_sprites_list.update()
		screen.fill(background_color)

		font = pygame.font.Font(None, 40)
		text = font.render(str(points[0]), 1, white)
		screen.blit(text, (20, 7))

		highScore = max(highScore,points[0])
		text = font.render("High Score {} Level {}".format(highScore,maxLevel), 1, white)
		screen.blit(text, (300, 7))

		all_sprites_list.draw(screen)
		pygame.draw.line(screen, white, [0, 35], [800, 35], 2)

		pygame.display.flip()
        
	pygame.quit()
	sys.exit()


runWithWeights = 1
specimen = loadBestSpecimen("C:\\Users\\RAM\\Desktop\\ATARI\\Shrinking size + Infinite\\Two Point\\best\\gen64.pickle")
while playLoaded(1,runWithWeights) != "QUIT":
	pass