import time
DIRECTORY = "avg" + str(int(time.time()))

INP_SIZE = 4
HIDDEN_SIZE = 6
SPECIMENS_PER_GEN = 80
numParents = 20

red	 = (255, 0, 0)
purple	= (255,	0, 255)
darkblue = (36,90,190)
yellow	= (255, 255, 0)
dark_yellow	 = (100, 100, 0)
white =	(255, 255, 255)
black = (0,	0, 0)
orange = (255, 100, 0)
blue = (0, 175, 240)
gray = (55, 55, 55)

screen_size = (width,height) = (800,600)
FPS = 60
background_color = gray
switch_color = 4

class Paddle_Values:
	size_x = 100
	size_y = 10
	color = blue
	speed = 5
	x = int((width-size_x)/2)
	y = int(height-height/8)

class Brick_Values:
	num_bricks = 10
	margin = 10
	columns = 6
	topMarginLayer = 2
	size_x = width/num_bricks
	size_y =  height/3/columns - margin
	color = orange

class Ball_Values:
	radius = 8
	center = [int((width-radius)/2) , int(2*height/4)]
	color = white
	speed = Paddle_Values.speed - 2