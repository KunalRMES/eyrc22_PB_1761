'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
from re import S
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def label_nodes(centre_point):
	s=''
	if( (centre_point[0]==100)  |  ((centre_point[0]>90)&(centre_point[0]<110)) ):
			s=s+'A'
	elif( (centre_point[0]==200)  |  ((centre_point[0]>190)&(centre_point[0]<210)) ):
			s=s+'B'
	elif( (centre_point[0]==300)  |  ((centre_point[0]>290)&(centre_point[0]<310)) ):
			s=s+'C'
	elif( (centre_point[0]==400)  |  ((centre_point[0]>390)&(centre_point[0]<410)) ):
			s=s+'D'
	elif( (centre_point[0]==500)  |  ((centre_point[0]>490)&(centre_point[0]<510)) ):
			s=s+'E'
	elif( (centre_point[0]==600)  |  ((centre_point[0]>590)&(centre_point[0]<610)) ):
			s=s+'F'
	elif( (centre_point[0]==700)  |  ((centre_point[0]>690)&(centre_point[0]<710)) ):
			s=s+'G'
	s=s+str(int(centre_point[1]/100))
	return s

def get_shop(centre_point):
    s='Shop_'
    if((centre_point[0]>100) & (centre_point[0]<200)):
        s=s+'1'
    elif((centre_point[0]>200) & (centre_point[0]<300)):
        s=s+'2'
    elif((centre_point[0]>300) & (centre_point[0]<400)):
        s=s+'3'
    elif((centre_point[0]>400) & (centre_point[0]<500)):
        s=s+'4'
    elif((centre_point[0]>500) & (centre_point[0]<600)):
        s=s+'5'
    elif((centre_point[0]>600) & (centre_point[0]<700)):
        s=s+'6'
    return s

def break_down(Lines):
    for l in Lines:
        if(l[1]-l[0]>120):
            a=l[0]+100
            Lines.append((l[0],a))
            while(a+84<l[1]):
                Lines.append((a,a+100))
                a=a+100
            Lines.remove(l)
    return Lines
    
def label_missing_vertical_lines(Lines):
    ans=[]
    for line,gap in Lines.items():
        for g in gap:
            s1=label_nodes((line,g[0]+10))
            s2=label_nodes((line,g[1]+10))
            s=s1+'-'+s2
            ans.append(s)
    return ans
    
def  label_missing_horizontal_lines(Lines):
    ans=[]
    for line,gap in Lines.items():
        for g in gap:
            s1=label_nodes((g[0],line))
            s2=label_nodes((g[1],line))
            s=s1+'-'+s2
            ans.append(s)
    return ans
            
    
def get_road_points_horizontal(Lines):
    ans=[]
    for line,gap in Lines.items():
        gap.sort()
        l=[]
        i=gap[0][0]
        prev=gap[0][1]
        gapc=gap[1:]
        for p in gapc:
            l.append((prev,p[0]))
            prev=p[1]
        if(i>150):
            l.append((96,i))
        if(prev<650):
            l.append((prev,708))
        Lines[line]=break_down(l)
    ans=label_missing_horizontal_lines(Lines)
    ans.sort()
    return ans
    
    
def get_road_points_vertical(Lines):
    ans=[]
    for line,gap in Lines.items():
        gap.sort()
        l=[]
        i=gap[0][0]
        prev=gap[0][1]
        gapc=gap[1:]
        for p in gapc:
            l.append((prev,p[0]))
            prev=p[1]
        if(i>150):
            l.append((96,i))
        if(prev<650):
            l.append((prev,708))
        Lines[line]=break_down(l)
    ans=label_missing_vertical_lines(Lines)
    ans.sort()
    return ans


##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############
	#Converting the image into HSV
	hsv = cv2.cvtColor(maze_image,cv2.COLOR_BGR2HSV)
 
	#Defining the range of Red color
	red_lower=np.array([0,70,50])
	red_upper=np.array([10,255,255])
 
 	#Creating the mask
	mask = cv2.inRange(hsv, red_lower, red_upper)

 	#Detecting the red color
	res = cv2.bitwise_and(maze_image, maze_image, mask=mask)
 
	# using a findContours() function
	contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
	# Putting Values into list
	for contour in contours:
  
        # finding center point of shape
		M = cv2.moments(contour)
		t=()
		if M['m00'] != 0.0:
			x = int(M['m10']/M['m00'])
			y = int(M['m01']/M['m00'])
			t=(x,y)
		traffic_signals.append(label_nodes(t))
	traffic_signals.sort()
	##################################################
	
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	#  Convert image to grayscale
	gray = cv2.cvtColor(maze_image,cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
 
	# Detect horizontal lines
	horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
	detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
	cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	sets_of_lines={}
	for c in cnts:
		if(cv2.arcLength(c, True)<1200):
			sets_of_lines.setdefault(c[0][0][1], [])
			sets_of_lines[c[0][0][1]].append((c[0][0][0],c[3][0][0]))
	horizontal_roads_under_construction=get_road_points_horizontal(sets_of_lines)
	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	#  Convert image to grayscale
	gray = cv2.cvtColor(maze_image,cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
 
	# Detect vertical lines
	vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,20))
	detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
	cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	sets_of_lines={}
	for c in cnts:
		if(cv2.arcLength(c, True)<1200):
			sets_of_lines.setdefault(c[0][0][0], [])
			sets_of_lines[c[0][0][0]].append((c[0][0][1],c[1][0][1]))
	vertical_roads_under_construction=get_road_points_vertical(sets_of_lines)
	##################################################
	
	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages = []

	##############	ADD YOUR CODE HERE	##############
	# Converting into Grayscale
	gray = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
 
	# getting only shapes and setting threshold of gray image
	_, with_shapes = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
	_, without_shapes = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
	only_shapes = cv2.bitwise_xor(with_shapes,without_shapes)

	# using a findContours() function
	contours, _ = cv2.findContours(only_shapes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# here we are ignoring first coutours because
	# findcontour function detects whole image as shape
	contours =  contours[1:]
	'''
	# convert to hsv colorspace for color detection
	image_rgb = cv2.cvtColor(maze_image, cv2.COLOR_BGR2RGB)
	
	hsv = cv2.cvtColor(maze_image, cv2.COLOR_BGR2HSV)
	cv2.imshow("HSV",hsv)
	'''
	#define kernel size  
	kernel = np.ones((7,7),np.uint8)
	
	# lower bound and upper bound for Green color
	g_lower_bound = np.array([0, 250, 0])   
	g_upper_bound = np.array([5, 255, 5])
	green_mask = cv2.inRange(maze_image, g_lower_bound, g_upper_bound)
	# Remove unnecessary noise from mask
	green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
	green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
	g_segmented_img = cv2.bitwise_and(maze_image, maze_image, mask=green_mask)
	#cv2.imshow("Green",g_segmented_img)
 
	# lower bound and upper bound for Sky Blue color
	sb_lower_bound = np.array([250, 250, 0])   
	sb_upper_bound = np.array([255, 255, 5])
	skyblue_mask = cv2.inRange(maze_image, sb_lower_bound, sb_upper_bound)
	# Remove unnecessary noise from mask
	skyblue_mask = cv2.morphologyEx(skyblue_mask, cv2.MORPH_CLOSE, kernel)
	skyblue_mask = cv2.morphologyEx(skyblue_mask, cv2.MORPH_OPEN, kernel)
	sb_segmented_img = cv2.bitwise_and(maze_image, maze_image, mask=skyblue_mask)
	#cv2.imshow("Sky Blue",sb_segmented_img)
	
	# lower bound and upper bound for Orange color
	p_lower_bound = np.array([100, 0, 250])   
	p_upper_bound = np.array([200, 10, 255])
	pink_mask = cv2.inRange(maze_image, p_lower_bound, p_upper_bound)
	# Remove unnecessary noise from mask
	pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_CLOSE, kernel)
	pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_OPEN, kernel)
	p_segmented_img = cv2.bitwise_and(maze_image, maze_image, mask=pink_mask)
	#cv2.imshow("Pink",p_segmented_img)
 
	# lower bound and upper bound for Orange color
	o_lower_bound = np.array([0, 100, 250])   
	o_upper_bound = np.array([5, 130, 255])
	orange_mask = cv2.inRange(maze_image, o_lower_bound, o_upper_bound)
	# Remove unnecessary noise from mask
	orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel)
	orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)
	o_segmented_img = cv2.bitwise_and(maze_image, maze_image, mask=orange_mask)
	#cv2.imshow("Orange",o_segmented_img)
	
	# Putting Values into list
	for contour in contours:   
		
		# Ignoring the extra contours
		area = cv2.contourArea(contour)
		if area < 200:
			continue

		# finding Shape
		approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)
		
		# if the shape is a triangle, it will have 3 vertices
		if (len(approx) == 3):
			shape = 'Triangle'

		# if the shape has 4 vertices, it is a square
		elif (len(approx) == 4):
			shape = 'Square'

		# otherwise, we assume the shape is a circle
		else:
			shape = 'Circle'
   
		# finding center point of shape
		M = cv2.moments(contour)
		t=()
		if M['m00'] != 0.0:
			x = int(M['m10']/M['m00'])
			y = int(M['m01']/M['m00'])
		t=(x,y)
  
		# finding color
		color=""
		if(p_segmented_img[x,y].any()):
			color="Pink"
		elif(o_segmented_img[x,y].any()):
			color="Orange"
		elif(sb_segmented_img[x,y].any()):
			color="Skyblue"
		elif(g_segmented_img[x,y].any()):
			color="Green"
		'''
		b, g, r= maze_image[x, y]
		color = str((b,g,r))
		# for sky blue 
		if ((b>250) & (g>250) & (r<5)):
			color="Skyblue"
		# for pink 
		elif ((b<5) & (g<150) & (r>250)):
			color="Pink"
		# for orange
		elif ((b<200) & (g<5) & (r>250)):
			color="Orange"
		# for green 
		elif ((b<5) & (g>250) & (r<5)):
			color="Green"
		'''
		# finding shop number
		shop=get_shop(t)

		# Add to list
		medicine_packages.append([shop,color,shape,t])
	medicine_packages.sort()
	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena_parameters={'traffic_signals':detect_traffic_signals(maze_image), 'horizontal_roads_under_construction':detect_horizontal_roads_under_construction(maze_image), 'vertical_roads_under_construction':detect_vertical_roads_under_construction(maze_image),'medicine_packages_present':detect_medicine_packages(maze_image)}
	##################################################
	
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()