import pygame
import sys
import os
import time
from paddle import Paddle
from ball import Ball
from brick import *
from Config import * 
from GeneticAlgorithm import *

pygame.init()

## AI
generation = []
screen = pygame.display.set_mode(screen_size)
hits = 0
maxHits = 30
score = 0
PREVFITNESS = 0

if DIRECTORY not in os.listdir():
	os.mkdir(DIRECTORY)
	os.mkdir(DIRECTORY + "/best")
	os.mkdir(DIRECTORY + "/all")
	os.mkdir(DIRECTORY + "/winner")

def play(live,gen_id,BREED_FUNCTION):
	global lives, hits, PREVFITNESS
	for spec_id in range(SPECIMENS_PER_GEN):
		pygame.init()
		pygame.display.set_caption("Brick and Ball")

		all_sprites_list = pygame.sprite.Group()

		points = [0] # score of the game that we can achieve
		generation[spec_id].fitness = 0
		lives = live # number of lives we have in the game
		exit = True # true until the games end or the close button is pressed

		if VISUAL: 
			screen.fill(background_color)

		#Create a paddle
		paddle = Paddle()
		paddle.rect.x = Paddle_Values.x
		paddle.rect.y = Paddle_Values.y

		#Create a ball
		ball = Ball(2*Ball_Values.radius, 2*Ball_Values.radius)
		ball.rect.x =  random.randint(100,700) #Ball_Values.center[0] - Ball_Values.radius
		ball.rect.y = Ball_Values.center[1] - Ball_Values.radius

		#adding bricks
		levels = Brick_Values.columns
		maxLevel = levels
		all_brick = pygame.sprite.Group()
		
		# for y in range(Brick_Values.columns):
		#     for x in range(0, screen_size[0], int(Brick_Values.size_x)):
		#     	brick = Brick()
		#     	brick.rect.x = x + Brick_Values.margin
		#     	brick.rect.y = int(Brick_Values.size_y) * (y + Brick_Values.topMarginLayer) + Brick_Values.margin
		#     	brick.level = levels
		#     	all_sprites_list.add(brick)
		#     	all_brick.add(brick)
		#     levels -= 1

		createBricks(all_brick,all_sprites_list)
		all_sprites_list.add(paddle)
		all_sprites_list.add(ball)

		while exit:

		    #Handling user input
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT:
					exit = False
					return "QUIT"
		    #Moving a paddle
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
			 	paddle.move_left()
			if keys[pygame.K_RIGHT]:
				paddle.move_right()

			ball.walls()
			
			if generation[spec_id].output(getInputVector(ball, paddle)) > 0.5:
				paddle.move_right()
			else:
				paddle.move_left()

		    #Checking walls
			if ball.bottom_line():
				lives -= 1
				if lives == 0:
					# generation[spec_id].fitness = points[0] #+(800-min(abs(paddle.rect.x-ball.rect.x),abs(paddle.rect.x+Paddle_Values.size_x-ball.rect.x)))/8000
					print("Gen {} Spec {} Fitness = {}".format(gen_id, spec_id, points[0]))
					if spec_id == SPECIMENS_PER_GEN - 1:
						if BREED_FUNCTION == 0:
							breed(generation, gen_id)
							return
						elif BREED_FUNCTION == 1:
							PREVFITNESS = breedFunction(generation,gen_id,PREVFITNESS)
							return

					lives = 1
					exit = False
					continue
				

		    #Collision with Paddle
			if paddle.rect.colliderect(ball.rect):
				if ball.movement[1] < 0:
					ball.movement[1] *= -1
				hits += 1
				if hits == maxHits:
					print("Gen {} Spec {} Fitness = {} Max Hits Reached".format(gen_id, spec_id, points[0]))
					if spec_id == SPECIMENS_PER_GEN - 1:
						if BREED_FUNCTION == 0:
							breed(generation, gen_id)
							return
						elif BREED_FUNCTION == 1:
							PREVFITNESS = breedFunction(generation,gen_id,PREVFITNESS)
							return
					else:
						exit = False
						continue

		    #Collision with bricks
			cont = False
			brick_collison_list = pygame.sprite.spritecollide(ball, all_brick, False)
			for brick in brick_collison_list:
				if not (ball.rect.x + 5 < brick.rect.x + Brick_Values.size_x and ball.rect.x + 2*Ball_Values.radius - 5 > brick.rect.x):
					ball.movement[0] *= -1
				ball.movement[1] *= -1

				points[0] += brick.level
				generation[spec_id].fitness += brick.level

				if hits < maxHits:
					hits = 0
				
				brick.kill()

				# CHANGE
				if len(all_brick) < 40:
					hitsBottom = addLevel(all_brick,all_sprites_list,maxLevel)
					if hitsBottom:
						# game over
						print("Gen {} Spec {} Fitness = {}".format(gen_id, spec_id, points[0]))
						if spec_id == SPECIMENS_PER_GEN - 1:
							if BREED_FUNCTION == 0:
								breed(generation, gen_id)
								return
							elif BREED_FUNCTION == 1:
								PREVFITNESS = breedFunction(generation,gen_id,PREVFITNESS)
								return

						lives = 1
						exit = False
						continue
					maxLevel += 1

				#CHANGE
				if maxLevel%10 == 0:
					if maxLevel/10 != (100 - paddle.width)/10:
						xx, yy = paddle.rect.x, paddle.rect.y
						paddle.updatePaddleSize()
						paddle.rect.x = xx
						paddle.rect.y = yy

				#When the level is cleared
				if len(all_brick) == 0:

					print("Gen {} Spec {} Fitness = {}".format(gen_id, spec_id, points[0]), " WINNER")
					saveWeights(DIRECTORY + "/winner/" + str(gen_id) + str(spec_id) + ".pickle", np.array([generation[spec_id].l1_weights, generation[spec_id].out_weights, generation[spec_id].fitness]))
					
					if spec_id == SPECIMENS_PER_GEN - 1:
						if BREED_FUNCTION == 0:
							breed(generation, gen_id)
							return
						elif BREED_FUNCTION == 1:
							PREVFITNESS = breedFunction(generation,gen_id,PREVFITNESS)
							return
					else:
						exit = False
						continue
					
					if VISUAL:
						font = pygame.font.Font(None, 60)
						text = font.render("Score: " + str(points[0]), 1, black)
						screen.blit(text, (215, 250))

					counterEnd = 0
					while counterEnd <= FPS*3:
						counterEnd += 1
						for event in pygame.event.get(): 
							if event.type == pygame.QUIT:
								pygame.quit()
								sys.exit() 

		    #Updating to screen all changes
			all_sprites_list.update()

			if VISUAL:
				screen.fill(background_color)
				#Score
				font = pygame.font.Font(None, 40)
				text = font.render(str(points[0]), 1, white)
				screen.blit(text, (20, 7))

				text = font.render("Gen: {} Spec: {}".format(gen_id, spec_id), 1, white)
				screen.blit(text, (300, 7))

				#All sprites
				all_sprites_list.draw(screen)
				pygame.draw.line(screen, white, [0, 35], [800, 35], 2)
				pygame.display.flip()
		    
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
 
	# print("MAIN GAME3")
	# start = 0
	# for i in range(SPECIMENS_PER_GEN):
	# 	generation.append(Specimen(0, INP_SIZE, HIDDEN_SIZE))

	generation = loadAllSpecimen("Avg Crossover\\all\\allweights6.pickle")
	start = 3

	total_gen = 100
	
	# 0 : one point
	# 1 : uniform
	BREED_FUNCTION = 0
	VISUAL = 1
	for gen_id in range(start,total_gen):
		spec_id = 0
		QUIT = play(1,gen_id,BREED_FUNCTION)
		if QUIT == "QUIT":
			break