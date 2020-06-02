# -*-coding:Latin-1 -*
import os
import math
import random
import time

def ReadPointsDatas(FileName):
	"""
	Function which download datas for a text file and return the donwloaded file split by line
	"""
	with open('datas/Points/%s.txt' %FileName, 'r') as PointsData:
		paramLines = PointsData.read().splitlines()
		pointsList = []

		for param in paramLines:
			name = param.split()[2]
			x = param.split('[')[2].split(']')[0].split(',')[0]
			y = param.split('[')[2].split(']')[0].split(', ')[1]
			z = param.split('[')[2].split(']')[0].split(', ')[2]
			point = [name, x, y, z, [], [], []]  # point = [name, x, y, z, [List_next], [List_cost], [List_prev]]
			pointsList.append(point)

	return pointsList



def ReadRobotParam(fileName):
	"""
	Function which read robot params and return a structured list of robot params
	"""
	with open('datas/%s.txt' %fileName, 'r') as robotDataFile:
		robotData = robotDataFile.read().splitlines()

		x = robotData[0].split('[')[2].split(']')[0].split(',')[0]
		y = robotData[0].split('[')[2].split(']')[0].split(',')[1]
		z = robotData[0].split('[')[2].split(']')[0].split(',')[2]
		r = robotData[1].split()[2]
		sr = robotData[2].split()[2]
		angle = int(robotData[3].split()[2])/180

		robotParam = [x,y,z,r,sr,angle]

	return(robotParam)
	
	
def ReadObstaclesParam(fileName):
	"""
	Function which read robot params and return a structured list of robot params
	"""
	with open('datas/Obstacles/%s.txt' %fileName, 'r') as obstaclesDataFile:
		obstaclesData = obstaclesDataFile.read().splitlines()
		obstaclesList = []

		for obstacle in obstaclesData:
			x1x = obstacle.split('\t')[1].split('[')[1].split(']')[0].split(',')[0]
			x1y = obstacle.split('\t')[1].split('[')[1].split(']')[0].split(',')[1]
			x1z = obstacle.split('\t')[1].split('[')[1].split(']')[0].split(',')[2]
			
			x2x = obstacle.split('\t')[2].split('[')[1].split(']')[0].split(',')[0]
			x2y = obstacle.split('\t')[2].split('[')[1].split(']')[0].split(',')[1]
			x2z = obstacle.split('\t')[2].split('[')[1].split(']')[0].split(',')[2]
			
			x3x = obstacle.split('\t')[3].split('[')[1].split(']')[0].split(',')[0]
			x3y = obstacle.split('\t')[3].split('[')[1].split(']')[0].split(',')[1]
			x3z = obstacle.split('\t')[3].split('[')[1].split(']')[0].split(',')[2]
			
			x4x = obstacle.split('\t')[4].split('[')[1].split(']')[0].split(',')[0]
			x4y = obstacle.split('\t')[4].split('[')[1].split(']')[0].split(',')[1]
			x4z = obstacle.split('\t')[4].split('[')[1].split(']')[0].split(',')[2]
			
			height = obstacle.split('\t')[5]
			obstacletoadd = [[x1x,x1y,x1z],[x2x,x2y,x2z],[x3x,x3y,x3z],[x4x,x4y,x4z], height]
			obstaclesList.append(obstacletoadd)

	return(obstaclesList)



def ReadRealPaverTemplate(templateName):
	"""
	Function which download a template for the file generation and return the donwloaded file split by line
	"""
	with open('RealPaver/Templates/%s.txt' %templateName, 'r') as templateFile:
		return templateFile.read().splitlines()



def WriteLinkBtwPoints(ListOfPoints, File_name):
	with open('datas/Csv_files/%s.csv' %File_name, 'w') as rapidDataFiles:
		max_cost = 0
		
		for point in ListOfPoints:
			#print("\n")
			#print(point[0])
			
			followPointStr = ""
			predecPointStr = ""
			costStr = ""
			max_cost_node = [0]
			
			for nextpoint in point[4]:
				followPointStr += nextpoint + ";"
				pointCost = []
				pointCostMax = [0]
				NextPointData = LookupPoints(ListOfPoints, nextpoint)
				
				if len(point[6]) == 0:
					#print(nextpoint),print("Longueur 0")
					cost = CostCalculation(point, NextPointData, False)
					pointCost.append(cost)
					pointCostMax.append(cost)
				else: 
					for precpoint in point[6]:
						if nextpoint != precpoint:
							PrevPointData = LookupPoints(ListOfPoints, precpoint)
							cost = CostCalculation(point, NextPointData,PrevPointData)	
							pointCost.append(cost)
							pointCostMax.append(cost)
				
				max_cost_node.append(max(pointCostMax))
				
				if len(pointCost) == 0:
					costStr += ";"
				elif len(pointCost) == 1:
					costStr += str(pointCost[0]) + ";"
				else:
					costStr += "["
					for tmpcost in pointCost:
						costStr += str(tmpcost) + ";"
					costStr = costStr[:-1] + "];"
			
			max_cost += max(max_cost_node)
			
			for precpoint in point[6]:
				predecPointStr += precpoint + ";"

			#print('%s,"%s","%s","%s"\n' %(point[0],followPointStr[:-1],costStr[:-1],predecPointStr[:-1]))
			#rapidDataFiles.write('"%s" \n' %str(costStr[:-1]))
			rapidDataFiles.write('%s,"%s","%s","%s"\n' %(point[0],followPointStr[:-1],costStr[:-1],predecPointStr[:-1]))
		
		print('Maximal cost : %s' %(max_cost))


def LookupPoints(ListOfPoints, PointToFind):
	for Points in ListOfPoints:
		if Points[0] == PointToFind:
			PointsData = Points
			break
	return(PointsData)

def CostCalculation(Point, NextPoint, PrevPoint):
	"""
	Function which calculate the cost of a motion between A and B
	"""
	dist_next = math.sqrt(((int(NextPoint[1]) - int(Point[1])) * (int(NextPoint[1]) - int(Point[1]))) + 
												((int(NextPoint[2]) - int(Point[2])) * (int(NextPoint[2]) - int(Point[2]))) + 
												((int(NextPoint[3]) - int(Point[3])) * (int(NextPoint[3]) - int(Point[3]))))
	
	distance = dist_next
	if PrevPoint != False:											
		dist_prev = math.sqrt(((int(PrevPoint[1]) - int(Point[1])) * (int(PrevPoint[1]) - int(Point[1]))) + 
													((int(PrevPoint[2]) - int(Point[2])) * (int(PrevPoint[2]) - int(Point[2]))) + 
													((int(PrevPoint[3]) - int(Point[3])) * (int(PrevPoint[3]) - int(Point[3]))))
													
		dist_prev_next = math.sqrt(((int(PrevPoint[1]) - int(NextPoint[1])) * (int(PrevPoint[1]) - int(NextPoint[1]))) + 
													((int(PrevPoint[2]) - int(NextPoint[2])) * (int(PrevPoint[2]) - int(NextPoint[2]))) + 
													((int(PrevPoint[3]) - int(NextPoint[3])) * (int(PrevPoint[3]) - int(NextPoint[3]))))
													
		angle = math.acos(((dist_next*dist_next)+(dist_prev*dist_prev)-(dist_prev_next*dist_prev_next))/(2*dist_next*dist_prev))
		
		distance += 50*math.fabs(math.cos(angle/2))
		
	return round(distance)


def CreateRealPaverModel(robotParam, pointA, pointB, Obstacle, template, fileName):
	"""
	Function which complete the model template with robot params
	"""
	with open('RealPaver/Models/%s.txt' %fileName, 'w') as newTemplate:
		for tempLine in template:
			if '/* Angle given in degree */' in tempLine:
				newTemplate.write("%s\n" %tempLine)
				newTemplate.write("angle = %s*@pi,\n" %robotParam[5])
			elif '/* Robot parameters */' in tempLine:
				newTemplate.write("%s\n" %tempLine)
				newTemplate.write("x0 = %s,\n" %robotParam[0])
				newTemplate.write("y0 = %s,\n" %robotParam[1])
				newTemplate.write("z0 = %s,\n" %robotParam[2])
				newTemplate.write("r = %s,\n" %robotParam[3])
				newTemplate.write("sr = %s,\n" %robotParam[4])
			elif '/* Point A and Point B */' in tempLine:
				newTemplate.write("%s\n" %tempLine)
				newTemplate.write("xa = %s, ya = %s, za = %s,\n" %(pointA[1], pointA[2], pointA[3]))
				newTemplate.write("xb = %s, yb = %s, zb = %s,\n" %(pointB[1], pointB[2], pointB[3]))
			elif '/* Point X1, X2, x3 and X4 to define the object */' in tempLine:
				newTemplate.write("%s\n" %tempLine)
				newTemplate.write("X1x = %s, X1y = %s, X1z = %s,\n" %(Obstacle[0][0],Obstacle[0][1],Obstacle[0][2]))
				newTemplate.write("X2x = %s, X2y = %s, X2z = %s,\n" %(Obstacle[1][0],Obstacle[1][1],Obstacle[1][2]))
				newTemplate.write("X3x = %s, X3y = %s, X3z = %s,\n" %(Obstacle[2][0],Obstacle[2][1],Obstacle[2][2]))
				newTemplate.write("X4x = %s, X4y = %s, X4z = %s,\n" %(Obstacle[3][0],Obstacle[3][1],Obstacle[3][2]))
				newTemplate.write("Hight = %s,\n" %Obstacle[4])
			else:
				newTemplate.write("%s\n" %tempLine)



def AnalyseRealPaverResult(fileName):
	"""
	Function which analyse the result of the realpaver execution
	"""
	with open('RealPaver/Results/%s.txt' %fileName, 'r') as result:
		isSolution = 1
		for line in result:
			#print(line)
			if ("OUTER BOX") in line:	# If this line is present -> A and B are not reachable
				isSolution = 0
			elif ("INNER BOX") in line:
				isSolution = 0

	return(isSolution)



def RunRealPaver(modelName, splitActivated):
	"""
	Function which launch thhe execution of a model on realpaver
	"""
	realpaverPath = "C:\\\"Program Files\"\\Realpaver\\realpaver.exe"
	modelDirectory = "RealPaver\\Models\\"
	resultDirectory = "RealPaver\\Results\\"
	resultName = "Realpaver_out"

	# Creation of the command line for realpaver
	if (splitActivated):
		fileLocation  = realpaverPath + " " + modelDirectory + modelName + ".txt" + " > " + resultDirectory + resultName + ".txt"
	else:
		fileLocation  = realpaverPath + " " + modelDirectory + modelName + ".txt" + " -nosplit > " + resultDirectory + resultName + ".txt"

	# execution
	os.system(fileLocation)

	# Analyse
	return(AnalyseRealPaverResult(resultName))



def CheckAccessibilityRealPaver(listOfPoints, robotParam, ListOfObstacles, modelType):
	"""
	Function which create link between cloud of points
	"""
	# templates reading
	tempWorking = ReadRealPaverTemplate(modelType + "_working_zone")
	tempUnreach = ReadRealPaverTemplate(modelType + "_unreachable_zone")
	tempForbid = ReadRealPaverTemplate(modelType + "_forbidden_zone")
	cpt_edges = 0
	
	for indexA in range(len(listOfPoints)):
		#print(indexA)
		#print(" ")
		for indexB in range(indexA+1,len(listOfPoints)):
			#if indexB%10 == 0:
				#print(indexB)
			start = time.time()
			CreateRealPaverModel(robotParam, listOfPoints[indexA], listOfPoints[indexB], ListOfObstacles, tempWorking, modelType + "_working_zone")
			isReachable = RunRealPaver(modelType + "_working_zone", 1)
			end = time.time()
			totaltime = (end-start)*1000
			print("working time is %.3f ms" %totaltime)
			#print(isReachable)
			if(isReachable):
				start = time.time()
				CreateRealPaverModel(robotParam, listOfPoints[indexA], listOfPoints[indexB], ListOfObstacles, tempUnreach, modelType + "_unreachable_zone")
				isReachable = RunRealPaver(modelType + "_unreachable_zone", 0)
				end = time.time()
				totaltime = (end-start)*1000
				print("Unreach time is %.3f ms" %totaltime)
				#print(isReachable)
				if (isReachable):
					for indexObstcle in range(len(list(ListOfObstacles))):	
						start = time.time()
						CreateRealPaverModel(robotParam, listOfPoints[indexA], listOfPoints[indexB], ListOfObstacles[indexObstcle], tempForbid, modelType + "_forbidden_zone")
						isReachable = RunRealPaver(modelType + "_forbidden_zone", 0)
						end = time.time()
						totaltime = (end-start)*1000
						print("Obstacles time is %.3f ms" %totaltime)
						#print(isReachable)
						#print("")
						if isReachable == 0:
							#print("Break")
							break
					if (isReachable):
						#cost = CostCalculation(listOfPoints[indexA], listOfPoints[indexB])
						if (indexA == 0):
							cpt_edges += 1
							listOfPoints[indexA][4].append(listOfPoints[indexB][0])
							#listOfPoints[indexA][5].append(cost)
							listOfPoints[indexB][6].append(listOfPoints[indexA][0])
						elif (indexB == len(listOfPoints)-1):
							cpt_edges += 1
							listOfPoints[indexA][4].append(listOfPoints[indexB][0])
							#listOfPoints[indexA][5].append(cost)
							listOfPoints[indexB][6].append(listOfPoints[indexA][0])
						else:
							cpt_edges += 2
							listOfPoints[indexA][4].append(listOfPoints[indexB][0])
							#listOfPoints[indexA][5].append(cost)
							listOfPoints[indexA][6].append(listOfPoints[indexB][0])
							listOfPoints[indexB][4].append(listOfPoints[indexA][0])
							#listOfPoints[indexB][5].append(cost)
							listOfPoints[indexB][6].append(listOfPoints[indexA][0])
			#print("\n")
	print("#edges : %s" %cpt_edges)
	density = (100*cpt_edges) / (len(listOfPoints)*(len(listOfPoints)-1))
	print("density : %s" %density)
	return(listOfPoints)



def diagramGeneration(Point_file_name, Outputfilename, Obstacle_file_name):
	"""
	Function which generate a diagram and write csv file
	"""
	robotParam = ReadRobotParam("Robot")
	points = ReadPointsDatas(Point_file_name)
	
	if Obstacle_file_name == "0_obstacles":
		obstacles = []
	else:	
		obstacles = ReadObstaclesParam(Obstacle_file_name)
		
	listLinked = CheckAccessibilityRealPaver(points, robotParam, obstacles, "3D")
	"""for i in range(0, len(points)):
		print(listLinked[i])"""
	WriteLinkBtwPoints(listLinked, Outputfilename)


"""
	EXECUTION

 if __name__ == "__main__" :
 	diagramGeneration()
"""