import cv2
import numpy as np
import math
import sys
from random import randint
from calc_ops import *
import time
import os

def main(argv):
	#Accepting the 2 images from the GUI
    image1 = cv2.imread(sys.argv[1],0)
    image2 = cv2.imread(sys.argv[2],0)
    cols,rows = image1.shape
    image3 = np.zeros((cols,rows,1),np.uint8)
    image4 = np.zeros((cols,rows,1),np.uint8)

	#Initialise a blank image with the dimensions of the source image
    final_image = np.zeros((cols,rows,1),np.uint8)

	#Initialise parameters
    count = 0
    entropy1 = 0
    entropy2 = 0
    joint_entropy = 0
    mi = 0
    temp_mi = 0
    angle = 0
    final_image = 0
    final_angle = 0
    final_x = 0
    final_y = 0
    count = 1
    limit = 2

    #Initially calculate the NMI of the two images
    mi = calc_mi(image1,image2)
    #If the NMI is 1.0, the two images are perfetly aligned with each other and a blank screen is obtained
    if mi==1.0:
        print 'Normalised Mutual Information = ',str(mi)
        print 'X-offset = ',str(final_x)
        print 'Y-Offset = ',str(final_y)
        print 'Angle of Rotation = ',str(final_angle)
        diff = cv2.absdiff(image1,image2)
        cv2.imshow("Source Image",image1)
        cv2.imshow("Template Image",image2)
        cv2.imshow("Transformed Image",image2)
        cv2.imshow("Aligned Image",diff)
        cv2.waitKey(0)

    #Genetic algorithm that repeats 10*limit number of times, lower the value of limit, faster is the execution but less accurate is the result
    while (count<=limit):
		#Find the best parent in the 1st cycle of iteration of the algorithm
        if count==1:
            parent = iterate(0,0,0,count)
        else:
		#Find the set of operations which yield maximum NMI on the selected parent set of operations
            parent = iterate(final_x,final_y,angle,count)
        for i in range(0,10):
            image3 = np.zeros((cols,rows,1),np.uint8)
			#Perform Translation
            image3 = calc_translation(image2,parent[i][0],parent[i][1],cols,rows)
            temp_mi = calc_mi(image1,image3)
            if temp_mi<mi:
				#Perform Rotation
                image3 = calc_rotation(image2,parent[i][2],cols,rows)
                temp_mi = calc_mi(image1,image3)
				#Is obtained NMI greater than current NMI, if so then, change the value of current MI to that of the obtained NMI
				#Record the offset values as well and accept the transformation
                if temp_mi>mi:
                    mi = temp_mi
                    final_image = image3
                    final_x = parent[i][0]
                    final_y = parent[i][1]
                    final_angle = parent[i][2]
            else:
                mi = temp_mi
                final_image = image3
                final_x = parent[i][0]
                final_y = parent[i][1]
                final_angle = parent[i][2]
                image3 = calc_rotation(image3,parent[i][2],cols,rows)
                temp_mi = calc_mi(image1,image3)
                if temp_mi>mi:
                    mi = temp_mi
                    final_image = image3
                    final_x+= parent[i][0]
                    final_y+= parent[i][1]
                    final_angle+= parent[i][2]
        count+=1

	#Display the result images and offset values as well as best NMI obtained
    print 'Normalised Mutual Information = ',str(mi)
    print 'X-offset = ',str(final_x)
    print 'Y-Offset = ',str(final_y)
    print 'Angle of Rotation = ',str(final_angle)
    diff = cv2.absdiff(image1,final_image)
    #Write the result images into a New Folder and write the metrics into a Metrics.txt file in the new folder and display the results
    timestr = time.strftime('%Y-%m-%d_%H:%M:%S')
    folder_name = "AlignedImage-"+timestr
    os.system('mkdir '+folder_name)
    cv2.imwrite("./"+folder_name+"/SourceImage.jpg",image1)
    cv2.imwrite("./"+folder_name+"/TemplateImage.jpg",image2)
    cv2.imwrite("./"+folder_name+"/TransformedImage.jpg",final_image)
    cv2.imwrite("./"+folder_name+"/AlignedImage.jpg",diff)
    f = open('./'+folder_name+'/Metrics.txt','a')
    f.write('Path of Source Image = '+sys.argv[1]+'\n')
    f.write('Path of Source Image = '+sys.argv[2]+'\n')
    f.write('X-Offset = '+str(final_x)+'\n')
    f.write('Y-Offset = '+str(final_y)+'\n')
    f.write('Angle of Rotation = '+str(final_angle)+'\n')
    f.write('Normalised Mutual Information = '+str(mi)+'\n')
    f.close()
    cv2.imshow("Source Image",image1)
    cv2.imshow("Template Image",image2)
    cv2.imshow("Transformed Image",final_image)
    cv2.imshow("Aligned Image",diff)
    cv2.waitKey(0)

if __name__ == "__main__":
    arg = sys.argv[1]
    main(arg)
