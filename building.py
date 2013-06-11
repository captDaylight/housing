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
floorAmountMax = 30
cubeList = [[0,0,0],[cubeSide,0,0],[cubeSide,cubeSide,0],[0,cubeSide,0],[0,0,cubeHeight],[cubeSide,0,cubeHeight],[cubeSide,cubeSide,cubeHeight],[0,cubeSide,cubeHeight]]

def Building():
	x = 0
	while x < 10:
		y = 0
		while y < 10:
			sweeper = MakeFloor()
			building = ExtrudeFloor(sweeper)
			rs.MoveObjects(building, [x*move_dist,y*move_dist,0])
# 			floors = DuplicateFloors(floor)
# 			for f in floors:
# 				rs.MoveObjects(f, [x*move_dist,y*move_dist,0])
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
	lines = []
	floorTiles = []
	for l in lengths:
		count = 0
		while count < l:
			pts.append(rs.AddPoint((position[0],position[1],position[2])))
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

	# create the initial path from the points generated	
	lines.append(rs.AddPolyline(pts))


# 	for p in pts:
# 		rs.AddText('paul', p,20)

	rs.DeleteObjects(pts)
	#offset the newly generated line and create another
	lines.append(rs.OffsetCurve(lines[0],[0,0,0], cubeSide/2))
	lines.append(rs.OffsetCurve(lines[0],[0,0,0], -cubeSide/2))	
	# cap the two lines by getting their end points
	start_pts = [rs.CurveStartPoint(lines[2]), rs.CurveStartPoint(lines[1]) ]
	end_pts = [rs.CurveEndPoint(lines[2]), rs.CurveEndPoint(lines[1])]
 
	lines.append(rs.AddPolyline(start_pts))
	lines.append(rs.AddPolyline(end_pts))
	
	
# 	floor = rs.AddPlanarSrf(lines)
	rs.DeleteObjects(lines[0])
	lines.pop(0)
	
	sweeper = rs.JoinCurves(lines)
	
	sweep_segs = rs.CurvePoints(sweeper)

	found_end = False
	while found_end == False:
		count  = 0
		for x in sweep_segs:
			if count > 1:
				#check if sweeper segments are on the same line
				if (CheckPtsInLine(sweep_segs[count], sweep_segs[count-1], sweep_segs[count-2])):
					# if so, pop that point out
					sweep_segs.pop(count-1)
					break
			count = count + 1
			if count == len(sweep_segs):
				found_end = True
	
	#check to see if first and last point are in line
	if(CheckPtsInLine(sweep_segs[0], sweep_segs[1], sweep_segs[len(sweep_segs)-2])):
		#delete the first and last elements
		sweep_segs.pop(0)
		sweep_segs.pop(len(sweep_segs)-1)
		print 'here'
	else:
		sweep_segs.pop(len(sweep_segs)-1)
		
	
	count = 1
	for p in sweep_segs:
		rs.AddText(count, p, 20)
		count = count + 1
	rs.DeleteObjects(lines)
# 	paul = rs.AddLine((0,0,0),(0,0,100))
# 	rs.AddSweep1(paul,total)
	return sweeper

def CheckPtsInLine(pt1, pt2, pt3):
	if (pt1[0] == pt2[0] and pt1[0] == pt3[0]):
		return True
	elif (pt1[1] == pt2[1] and pt1[1] == pt3[1]):
		return True
	else:
		return False

		
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

def ExtrudeFloor(sweeper):
	floorAmount = random.randint(floorAmountMin,floorAmountMax)
	extrudeAmount = floor_height * floorAmount
	rail = rs.AddLine((0,0,0),(0,0,extrudeAmount))
	building = []
	building.append(rs.AddSweep1(rail, sweeper))
	floor = rs.AddPlanarSrf(sweeper)
	rs.MoveObject(floor, (0,0,extrudeAmount))
	rs.DeleteObjects([rail,sweeper])
	building.append(floor)
	return building

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
