import cv2
import numpy as np
import math
from random import randint

#To generate 2 random integers between the range (mini,maxi)
def gen_rand(mini,maxi):
	return randint(mini,maxi)

#To generate (x,y) value for rotation where each value lies between (-10,10)
def gen_translation():
	return gen_rand(-10,10),gen_rand(-10,10)

#To generate the angle of rotation value which is between (-50,0)
def gen_rotation():
	return gen_rand(-50,0)

#To generate random points (x,y) in order to find the Affine or Perspective Transformation
def gen_points(cols,rows):
	points = []
	for i in range(0,4):
		pt_list = [gen_rand(0,cols),gen_rand(0,rows)]
		points.append(pt_list)
	return np.float32(points)

#To find the histogram of an image
def calc_histogram(image):
	hist = cv2.calcHist([image],[0],None,[16],[0,256])
	return hist

#To find the histogram and the entropy of an image
def calc_entropy(image):
	entropy = 0
	size = image.size
	hist = cv2.calcHist([image],[0],None,[16],[0,256])
	for i in range(0,15):
		p = hist[i]/size
		if p!=0:
			entropy-=p*math.log(p,2)
	return entropy

#To find the joint histogram of two images
def calc_joint_histogram(image1,image2):
	joint_entropy = 0
	joint_mat = np.ndarray((16,16))
	joint_mat.fill(0)
	size = image1.size
	for i in range(0,image1.shape[0]):
		for j in range(0,image1.shape[1]):
			inten1 = image1[i][j]/16
			inten2 = image2[i][j]/16
			joint_mat[inten1][inten2]+=1
	return joint_mat,size

#Given the Joint Histogram, to find the Joint Entropy of the two images
def calc_joint_entropy(joint_mat,size):
	joint_entropy = 0
	for i in range(0,15):
		for j in range(0,15):
			p = joint_mat[i][j]/size
			if p!=0:
				joint_entropy-=p*math.log(p,2)
	return joint_entropy

#To perform translation operation on an image, given it's dimensions and (x,y) co-ordinates to translate it by
def calc_translation(image,x,y,cols,rows):
	new_image = np.zeros((cols,rows,1),np.uint8)
	M = np.float32([[1,0,x],[0,1,y]])
	new_image = cv2.warpAffine(image,M,(rows,cols))
	return new_image

#To perform rotation operation on an image, given it's dimensions and angle of rotation to rotate it by
def calc_rotation(image,angle,cols,rows):
	new_image = np.zeros((cols,rows,1),np.uint8)
	M = cv2.getRotationMatrix2D((cols/2,rows/2),float(angle),1.0)
	new_image = cv2.warpAffine(image,M,(rows,cols))
	return new_image

#Given the Joint Entropy and separate Entropies of the two images, NMI is found
def calc_mi(image1,image2):
	entropy1 = calc_entropy(image1)
	entropy2 = calc_entropy(image2)
	joint_mat,size = calc_joint_histogram(image1,image2)
	joint_entropy = calc_joint_entropy(joint_mat,size)
	mi = math.sqrt(2-(2*joint_entropy/(entropy1+entropy2)))
	return mi

#To check if the obtained value of NMI is greater than current NMI and if it is true, record the current offset values
def check_mi(mi,temp_mi,image,x,y,angle):
	if temp_mi>mi:
		final_image = image
		final_angle = angle
		final_y = y
		final_x = x
	return mi,final_image,final_x,final_y,final_angle

#Used to generate random parameters for translation and rotation (x,y,0) in order to perform these operations on a parent set of operations
def iterate(x,y,angle,count):
	parent=np.ndarray((10,3))
	if count==1:
		for i in range(0,10):
			for j in range(0,3):
				if j<2:
					parent[i][j]=randint(-10,10)
				else:
					parent[i][j]=randint(-40,40)

	else:
		parent[1][0]=randint(-5,5)
		parent[1][1]=0
		parent[1][2]=0
		parent[2][0]=-randint(-5,5)
		parent[2][1]=0
		parent[2][2]=0
		parent[3][0]=randint(-5,5)
		parent[3][1]=randint(-5,5)
		parent[3][2]=randint(-5,5)
		parent[4][0]=-randint(-5,5)
		parent[4][1]=-randint(-5,5)
		parent[4][2]=-randint(-5,5)
		parent[5][0]=randint(-5,5)
		parent[5][1]=-randint(-5,5)
		parent[5][2]=0
		parent[6][0]=-randint(-5,5)
		parent[6][1]=randint(-5,5)
		parent[6][2]=0
		parent[7][0]=randint(-5,5)
		parent[7][1]=randint(-5,5)
		parent[7][2]=0
		parent[8][0]=-randint(-5,5)
		parent[8][1]=-randint(-5,5)
		parent[8][2]=0
		parent[9][0]=0
		parent[9][1]=0
		parent[9][2]=randint(-5,5)
		parent[0][0]=0
		parent[0][1]=0
		parent[0][2]=-randint(-5,5)
	return parent

#To perform an Affine Transformation by accepting an image, it's dimensions and the points (x1,y1) and (x2,y2) to apply transformation to it
def calc_affine(image,pts1,pts2,cols,rows):
	new_image = np.zeros((cols,rows,1),np.uint8)
	M = cv2.getAffineTransform(pts1,pts2)
	new_image = cv2.warpAffine(image,M,(rows,cols))
	return new_image

#To perform an Perspective Transformation by accepting an image, it's dimensions and the points (x1,y1) and (x2,y2) to apply transformation to it
def calc_perspective(image,pts1,pts2,cols,rows):
	new_image = np.zeros((cols,rows,1),np.uint8)
	M = cv2.getPerspectiveTransform(pts1,pts2)
	new_image = cv2.warpPerspective(image,M,(rows,cols))
	return new_image
