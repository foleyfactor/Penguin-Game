from tkinter import *
from time import *
from random import *
from math import *

#Variable initialization
score = 0
frame = 0
lose = False

icebergLen = 700
icebergHeight = 200

spacing = 100

master = Tk()
screen = Canvas(master, width=900, height=900, background='#99ffff')
master.wm_title('Penguin Game')
screen.pack()

whaleRight = PhotoImage(file='./penguinImage/whale.gif')
whaleLeft = PhotoImage(file='./penguinImage/whaleLeft.gif')
whaleImage = whaleRight
whaleStep = 1/150

playerRight = PhotoImage(file='./penguinImage/playerRight.gif')
playerLeft = PhotoImage(file='./penguinImage/playerLeft.gif')
penguinLeft = PhotoImage(file='./penguinImage/penguinLeft.gif')
penguinRight = PhotoImage(file='./penguinImage/penguinRight.gif')
numPenguins = 8

#class for the penguins
class Penguin:
	def __init__(self, num, player=False):
		self.num = num
		self.player = player
		self.velocity = [choice([-5,-4,-3,-2,-1,1,2,3,4,5]), 0]
		self.x = spacing+num*(icebergLen//numPenguins)
		self.win = True
		self.inAir = False
		
		#set the penguin's y co-ordinates based on the height of the image
		if player:
			self.y = 245
		else:
			self.y = 260

	def update(self):
		global score
		global lose

		if self.player:
			if self.y<245:
				self.velocity[1]+=0.5
			
			if self.velocity[1]>0:
				if not isFalling(0):
					if self.y>245:
						self.velocity[1]=0
						self.y = 245
						self.inAir = False
			
			if self.velocity[0]<0:
				self.image = playerLeft
			else:
				self.image = playerRight
			self.x += self.velocity[0]
			self.y += self.velocity[1]
			
			if not self.y>=450:
				return screen.create_image(self.x, self.y, tags="penguin", image=self.image)
			else:
				lose = True

		if not self.player:
			if self.velocity[0] < 0:
				self.image = penguinLeft
			else:
				self.image = penguinRight
			self.x += self.velocity[0]
			self.y += self.velocity[1]
			
			if not self.y >= 450:
				return screen.create_image(self.x, self.y, tags="penguin", image=self.image)
				self.win = True
			else:
				self.win = False
				score += 1

#function for replacing an old penguin with a new one
def newPenguin(oldPenguin):
	global penguins
	penguins[oldPenguin] = Penguin(oldPenguin, False)

#key event handlers
def key(key):
	sym = key.keysym
	if sym == "space":
		if not isFalling(0) and not penguins[0].inAir:
			penguins[0].velocity[1]-=12
			penguins[0].inAir = True

def left(key):
	sym = key.keysym
	if sym == "Left":
		if not isFalling(0) and not penguins[0].inAir:
			penguins[0].velocity[0] -= 0.4

def right(key):
	sym = key.keysym
	if sym == "Right":
		if not isFalling(0) and not penguins[0].inAir:
			penguins[0].velocity[0] += 0.4

#checks if two penguins are colliding
def colliding(a,b):
	oneVelocity = penguins[a].velocity[0]
	twoVelocity = penguins[b].velocity[0]

	if not (isFalling(a) or isFalling(b)):
		if not (penguins[a].y<=200 or penguins[b].y<=200):
			xCenterOne = penguins[a].x
			xCenterTwo = penguins[b].x
			length = sqrt((xCenterTwo-xCenterOne)**2)
			if length <= 50:
				return True
			else:
				return False
		else:
			return False
	else:
		return False

#checks for collisions between penguins and prevents infinite loops
def checkCollision():
	for i in range(len(penguins)):
		for x in range(len(penguins)):
			if i >= x:
				continue
			
			dist = fabs(penguins[i].x - penguins[x].x)
			
			if dist <= 25 and fabs(penguins[i].y - penguins[x].y) <= 16:
				if penguins[i].velocity[0]*penguins[x].velocity[0] >= 0:
					if fabs(penguins[i].velocity[0]) > fabs(penguins[x].velocity[0]):
						penguins[x].velocity[0] = penguins[i].velocity[0]
					else:
						penguins[i].velocity[0] = penguins[x].velocity[0]
				else:
					if penguins[i].x > penguins[x].x:
						penguins[i].x += (25-dist)/2
						penguins[x].x -= (25-dist)/2
					else:
						penguins[x].x += (25-dist)/2
						penguins[i].x -= (25-dist)/2

					penguins[i].velocity[0] *= -1
					penguins[x].velocity[0] *= -1

#check if the penguin should fall off of the iceberg
def isFalling(a):
	if penguins[a].x+25<spacing or penguins[a].x>spacing+icebergLen+25:
		return True

#if the penguin should be falling, increment its vertical velocity downward		
def checkFall():
	for i in range(len(penguins)):
		if isFalling(i):
			penguins[i].velocity[1]+=1
		
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

#spawns a new penguin at the old penguin's starting location
def penguinSpawn():
	for i in range(len(penguins)):
		if not penguins[i].win:
			newPenguin(i)

#check if there is only the player left
def checkWin():
	for i in range(1,len(penguins)):
		if penguins[i].win==True:
			return False
	return True

#check if two penguins are going in the same direction
def sameDirection(a,b):
	if penguins[a].velocity[0]/penguins[b].velocity[0] > 0:
		return True
	else:
		return False

#draw the beautiful scenery (extra credit to fish for the cool looking design)
def drawTheIceberg():

	sun = screen.create_oval(10, 10, 100, 100, fill='yellow', outline='yellow')
	
	#Draw some clouds
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
	
	for i in range(900):
		screen.create_rectangle(i, abs((14*sin(i/15)))+500, i+1, 900, fill="blue", outline="blue")

	for i in range(spacing, icebergLen+spacing):
		if i<450:
			screen.create_rectangle(i, 500+heightarray[i%450], i+1, abs((14*sin(i/15)))+500, fill="#008bfb", outline="#008bfb")
		else:
			screen.create_rectangle(i, 500+heightarray[(450-i)%450], i+1, abs((14*sin(i/15)))+500, fill="#008bfb", outline="#008bfb")

#keep track of the awesome killer whale who is looking for a snack
def whaleDraw():
	global frame
	global whaleTransition
	global whaleImage

	#delete old whale
	screen.delete('whale')
	angle = frame*whaleStep

	#check for whale's direction
	if 0.99 < abs(sin(angle)):
		whaleImage = whaleLeft
	elif -0.1 < sin(angle) < 0.1:
		whaleImage = whaleRight

	#draw that super whale
	screen.create_image(abs(sin(angle))*900, 700, image=whaleImage, tags='whale')

#bind keys to key event handlers
master.bind("<space>", key)
master.bind("<Left>", left)
master.bind("<Right>", right)

#create the penguins
penguins = [Penguin(numPenguins//2, True)]

for i in range(numPenguins):
	if i!=numPenguins//2:
		penguins.append(Penguin(i))

#draw the beautiful background
drawTheIceberg()

#main game loop
while not lose:
	screen.create_text(450, 12, font=('Times', 24), text=score, tags='score')
	
	if not frame % 3:
		whaleDraw()

	if not frame % 2:		
		screen.update()
		screen.delete("penguin", 'score')
	
		for penguin in penguins:
			penguin.update()
	
		checkFall()
		checkCollision()
		penguinSpawn()
	
	# if checkWin():
	# 	screen.delete(ALL)
	# 	screen.create_text(450, 450, anchor="center", font=("Times", 48), text="You win!")
	# 	screen.mainloop()
	
		sleep(0.01)
	frame += 1

#delete everything and tell the player that they lost (likely because they are bad)
screen.delete(ALL)
screen.create_text(450, 450, anchor="center", font=("Times", 48), text="You lose.\nYour score is " + str(score) + '.')
screen.mainloop()