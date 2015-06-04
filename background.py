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

def generateBackground():
	screen.create_rectangle(0, 0, 900, 900, fill="#99ffff", outline="#99ffff")
	drawTheIceberg()