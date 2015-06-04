from tkinter import *
from time import *
from random import *
from math import *
#from background import generateBackground

penguins = []
penguinAlive = []
playerIndex = None

arrowKeyPressed = []

icebergLen = 700
icebergHeight = 200

spacing = 100

master = Tk()
screen = Canvas(master, width=900, height=900, background='#99ffff')
screen.pack()

playerRight = PhotoImage(file='./penguinImage/playerRight.gif')
playerLeft = PhotoImage(file='./penguinImage/playerLeft.gif')
penguinLeft = PhotoImage(file='./penguinImage/penguinLeft.gif')
penguinRight = PhotoImage(file='./penguinImage/penguinRight.gif')

def spacePressed(event):
	arrowKeyPressed.append('up')

def spaceRelease(event):
	while 'up' in arrowKeyPressed:
		arrowKeyPressed.remove('up')

def rightPressed(event):
	arrowKeyPressed.append('right')

def rightRelease(event):
	while 'right' in arrowKeyPressed:
		arrowKeyPressed.remove('right')

def leftPressed(event):
	arrowKeyPressed.append('left')

def leftRelease(event):
	while 'left' in arrowKeyPressed:
		arrowKeyPressed.remove('left')

master.bind('<Left>', leftPressed)
master.bind('<KeyRelease-Left>', leftRelease)
master.bind('<space>', spacePressed)
master.bind('<KeyRelease-space>', spaceRelease)
master.bind('<Right>', rightPressed)
master.bind('<KeyRelease-Right>', rightRelease)

def generatePenguins(numberPenguins):
	global penguins
	global penguinAlive
	global playerIndex
	for i in range(numberPenguins):
		if i + 1 == ceil(numberPenguins/2):
			direction = choice(['r', 'l'])
			speed = 0
			location = [spacing + (icebergLen/numberPenguins)*i, icebergHeight+43]
			penguins.append([location, speed, direction, None, None, True])
			penguinAlive.append([True, True])
			playerIndex = i
		else:
			direction = choice(['r', 'l'])
			speed = randint(3,8)
			location = [spacing + (icebergLen/numberPenguins)*i, icebergHeight + 59]
			penguins.append([location, speed, direction, None, None, None])
			penguinAlive.append([True, True])

def create_cloud(fluffiness):
	#How many circles will cloud be coloured in by each iteration
	bubbles = randrange(3,8)

	#Where the starting point of the cloud is
	initial_x = randrange(900)
	initial_y = randrange(100)

	#The fluffiness just means how many times we draw in the cloud
	#It usually turns out that this makes the cloud fluffier (but not necessarily)
	for i in range(fluffiness):
		for i in range(bubbles):
			radius = randrange(20,40)
			#Make sure that the centre of the bubble isn't more than 1 radius away from the start
			x = initial_x + randrange(-1*radius, radius)
			y = initial_y + randrange(-1*radius, radius)
			screen.create_oval(x-radius, y-radius, x+radius, y+radius, fill="white", outline="white")

def drawTheIceberg():
	for i in range(8):
		create_cloud(5)
	iceberg = screen.create_polygon(spacing, 514, spacing, icebergHeight+118, spacing + icebergLen, icebergHeight + 118, spacing+icebergLen, 514, fill='white', outline='white')
	xStart = spacing
	while xStart<icebergLen+spacing:
		xStart += randint(0,100)
		xWidth = randint(0,100)
		if xStart+xWidth>icebergLen:
			break
		screen.create_rectangle(xStart, icebergHeight+118, xStart+xWidth, 514, fill="#F7FFFF", outline="#F7FFFF")
	height = 10
	heightarray = []
	for i in range(450):
		height+=randint(0,2)
		heightarray.append(height)
	print(heightarray)
	for i in range(900):
		screen.create_rectangle(i, abs((14*sin(i/15)))+500, i+1, 900, fill="blue", outline="blue")

	for i in range(spacing, icebergLen+spacing):
		if i<450:
			screen.create_rectangle(i, 500+heightarray[i%450], i+1, abs((14*sin(i/15)))+500, fill="#008bfb", outline="#008bfb")
		else:
			screen.create_rectangle(i, 500+heightarray[(450-i)%450], i+1, abs((14*sin(i/15)))+500, fill="#008bfb", outline="#008bfb")

def updateThePenguins():
	global penguins
	global penguinAlive
	checkPenguinCollision()
	for i in range(len(penguins)):
		print(penguinAlive[i])
		if penguinAlive[i][1] == False:
			continue
		else:
			if penguins[i][2] == 'r':
				penguins[i][0][0] += penguins[i][1]
			else:
				penguins[i][0][0] -= penguins[i][1]
			if not penguinAlive[i][0]:
				penguins[i][0][1] *= 1.075
			penguins[i][3] = screen.create_image(penguins[i][0], image=penguins[i][4])
	screen.update()
	sleep(0.05)
	for i in range(len(penguins)):
		screen.delete(penguins[i][3])

def checkPenguinCollision():
	global penguins
	global penguinAlive
	for i in range(len(penguins)):
		for x in range(len(penguins)):
			if i >= x:
				continue
			if fabs(penguins[i][0][0] - penguins[x][0][0]) <= 25 and fabs(penguins[i][0][1] - penguins[x][0][1]) <= 16:
				if penguins[i][2] == penguins[x][2]:
					if penguins[i][1] > penguins[x][1]:
						penguins [x][1] = penguins[i][1]
					else:
						penguins[i][1] = penguins[x][1]
				else:
					if penguins[i][2] == 'r':
						penguins[i][2] = 'l'
					else:
						penguins[i][2] = 'r'

					if penguins[x][2] == 'r':
						penguins[x][2] = 'l'
					else:
						penguins[x][2] = 'r'
		if penguins[i][0][0] - 25 >= icebergLen + spacing or penguins[i][0][0] + 25 <= spacing:
			penguinAlive[i][0] = False
		if penguins[i][0][1] + 43 >= 486:
			penguinAlive[i][1] = False
		if not penguins[i][5]:
			if penguins[i][2] == 'r':
				penguins[i][4] = penguinRight
			else:
				penguins[i][4] = penguinLeft
		else:
			if penguins[i][2] == 'r':
				penguins[i][4] = playerRight
			else:
				penguins[i][4] = playerLeft

def notAllPenguinsDead():
	alive = []
	global penguinAlive
	for i in penguinAlive:
		if not i[1]:
			alive.append('The penguinz iz ded')
	print(alive)
	if len(alive) == len(penguinAlive):
		return False
	else:
		return True

def inputHandler():
	if len(arrowKeyPressed):
		pass

def main(numberPenguins):
	#generateBackground()
	generatePenguins(numberPenguins)
	drawTheIceberg()
	while notAllPenguinsDead():
		updateThePenguins()

main(8)