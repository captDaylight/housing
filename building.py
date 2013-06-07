import rhinoscriptsyntax as rs
import math
import random
# Test to draw a cube
start_location = [0,0,0]
max_dist = 4
min_dist = 1
move_dist = 800
floor_height = 30
cubeSide = 100
cubeHeight = 5
floorAmountMin = 4
floorAmountMax = 10
cubeList = [[0,0,0],[cubeSide,0,0],[cubeSide,cubeSide,0],[0,cubeSide,0],[0,0,cubeHeight],[cubeSide,0,cubeHeight],[cubeSide,cubeSide,cubeHeight],[0,cubeSide,cubeHeight]]

def Building():
	x = 0
	while x < 1:
		y = 0
		while y < 1:
			floor = MakeFloor()
			#floors = DuplicateFloors(floor)
			#for f in floors:
				#rs.MoveObjects(f, [x*move_dist,y*move_dist,0])
			y = y + 1
			print 'made a building'
		x = x + 1

	
# 	floors = ExtrudeFloors(floor)
# 	return floors
		
def MakeFloor():
	lengths = GenerateLengths()
	positive = True # whether the path is traveling positive or negative along the axis
	travelingX = True # whether the path is traveling along the x or y axis
	position = [0,0,0]
	pts = []
	floorTiles = []
	for l in lengths:
		count = 0
		while count < l:
			pts.append(rs.AddPoint((position[0],position[1],position[2])))
			#cube = rs.AddBox(cubeList)
			#floorTiles.append(cube)
			if(travelingX):
				if(positive):
					position[0] = position[0] + cubeSide
				else:
					position[0] = position[0] - cubeSide
			else:
				if(positive):
					position[1] = position[1] + cubeSide
				else:
					position[1] = position[1] - cubeSide
			#rs.MoveObject(cube, position)
			count = count + 1		
		# toggle axis
		travelingX = not travelingX
		# get a random direction on the axis
		positive = random.choice([True, False])
	
	rs.AddPolyline(pts)
	return floorTiles
			
def GenerateLengths():
	# maximum three segments
	segments = 0
	lengths = []
	while segments < 4:
		if(segments == 0):
			lengths.append(random.randint(min_dist, max_dist))
		else:
			# 3/4 chance of adding another length to the building
			if(random.random() < .75):
				lengths.append(random.randint(min_dist, max_dist))
		segments = segments + 1
	return lengths
	

def DuplicateFloors(floor):
	floorAmount = random.randint(floorAmountMin,floorAmountMax)
	count = 0
	floors = [floor]
	while count < floorAmount:
		new_floor = rs.CopyObjects(floor, [0,0,floor_height*(count+1)])
		floors.append(new_floor)
		count = count + 1
	return floors
	
# Check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if( __name__ == '__main__' ):
    #call function defined above
    Building()
