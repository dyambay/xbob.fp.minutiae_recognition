import bob
np = bob.ip.numpy

################################################
################################################

def finger_thin(img,height, width):
#iterates through the image in 32x32 boxes
#It iterates multiple times, odd_even keeps track of whether it is an odd or even iteration. Different logic is used for odd and even iterations
	odd_even=1
	pixel_del = 1
	while pixel_del==1:
		pixel_del=0
		status = 'iteration ' +str(odd_even)
		print(status)
		for i in xrange(0,height-2,1):
			for j in xrange(0,width-2,1):
	#creates a box of each 3x3 set of pixels
				box=np.asarray(((img[i:i+3,j:j+3]/255)-1)/255, dtype = 'int') 
				#print(box)
				#sets each pixel to a specific point for ease of use for later logic
				P2 = box[0][1]
				P3 = box[0][2]
				P4 = box[1][2]
				P5 = box[2][2]
				P6 = box[2][1]
				P7 = box[2][0]
				P8 = box[1][0]
				P9 = box[0][0]
				#a_box represents the values gotten from going around the outside rim of the box and subtracting the pixel value from the next value to find the number of 1 to 0 transitions
				a_box=[]
				#lays out the box in one row
				box_sum = box[0]+box[1]+box[2]
				#print('Center Pixel is ' + str(box[1][1]))
				#since this method just deletes the center pixel, if the center pixel does not have a value then it doesn't need to be deleted and you can skip that
				if box[1][1] == 1:
					#print('The sum of the box is ' + str(sum(box_sum)))
					#we only care if the center pixel has 2 to 6 neighboring 1s
					if 3<=sum(box_sum)<=7:
						a_box.append(P2-P3)
						a_box.append(P3-P4)
						a_box.append(P4-P5)
						a_box.append(P5-P6)
						a_box.append(P6-P7)
						a_box.append(P7-P8)
						a_box.append(P8-P9)
						a_box.append(P9-P2)
						#alters 0-1 interactions from -1 to 0 so that it doesn't interfere with the summation of 1s
						a_box = [0 if x==-1 else x for x in a_box]
						#print(a_box)
						#print('The number of 1 to 0 transitions is ' + str(sum(a_box)))
						#Only if the number of 1 to 0 transitions is 1 or 2 do you look at deleting the center pixel
						if sum(a_box)==1:
							if odd_even%2 == 1:
								#print('P2xP4xP8 = ' + str(P2*P4*P8))
								#print('P4xP6xP8 = ' + str(P4*P6*P8))
								if P2*P4*P8==0 & P4*P6*P8==0:
									img[i+1][j+1]=255
									pixel_del=1
									#print('pixel deleted')
							if odd_even%2 == 0:
								if P2*P4*P8==0 & P2*P6*P8==0:
									img[i+1][j+1]=255
									pixel_del=1
									#print('pixel deleted')
#						if sum(a_box)==2:
#							if odd_even%2 == 1:
#								if P4*P6==1 & P9==0:
#									img[i+1][j+1]=255
#									pixel_del
									#print('pixel deleted')
#								if P4*P2==1 & P3+P7+P8==0:
#									img[i+1][j+1]=255
#									pixel_del=1
									#print('pixel deleted')
#							if odd_even%2 == 0:
#								if P2*P8==1 & P5==0:
#									img[i+1][j+1]=255
#									pixel_del=1
									#print('pixel deleted')
#								if P6*P8==1 & P3+P7+P4==0:
#									img[i+1][j+1]=255
#									pixel_del=1
									#print('pixel deleted')
		odd_even += 1
	return np.asarray(img,dtype='uint8')

############################################################################
############################################################################

def extract(image, height, width):
#	new_img = bob.ip.gray_to_rgb(image)
	for i in xrange(11,height-11,1):
		for j in xrange(11,width-11,1):
			#creates a box of each 3x3 set of pixels
			box=np.asarray(((image[i:i+3,j:j+3]/255)-1)/255, dtype = 'int') 
			#sets each pixel to a specific point for ease of use for later logic
			P2 = box[0][1]
			P3 = box[0][2]
			P4 = box[1][2]
			P5 = box[2][2]
			P6 = box[2][1]
			P7 = box[2][0]
			P8 = box[1][0]
			P9 = box[0][0]
			a_box=[]
			if box[1][1] == 1:
				#lays out the box in one row
				#box_sum = box[0]+box[1]+box[2]
				a_box.append(P2-P3)
				a_box.append(P3-P4)
				a_box.append(P4-P5)
				a_box.append(P5-P6)
				a_box.append(P6-P7)
				a_box.append(P7-P8)
				a_box.append(P8-P9)
				a_box.append(P9-P2)
				a_box = [1 if x==-1 else x for x in a_box]
				CN = 0.5*sum(a_box)
				#we only care if the center pixel has 0,1,3, or 4 neighboring 1s
				#represents an isolated point
				#if CN==0:
				#	image[i+1][j+1] = 127
				#represents a ridge ending point
				if CN==1:
					image[i+1][j+1] = 128
				#represents a bifurcation point
				elif CN==3:
					image[i+1][j+1] = 76
				#represents a crossing point
				#elif CN==1:
				#	image[i+1][j+1] = 130
	return image

#################################################################
#################################################################

#calculates the average interridge width of the fingerprint
def calc_D(image, height, width):
	img=np.asarray(((image/255)-1)/255, dtype = 'int') 
	imgR = np.rot90(img)
	x_counter = 0
	y_counter = 0
	row_avg = float(0)
	col_avg=float(0)
	for i in xrange(int((height/2)*.75),int((height/2)*1.25),1):
		find_first = 0
		find_last = 0
		loc_f = 0
		loc_l = len(img[i])-1
		while find_first==0:			
			if img[i][loc_f]==1:
				find_first = 1
			else:
				loc_f +=1
		while find_last == 0:
			if img[i][loc_l]==1:
				find_last = 1
			else:
				loc_l -=1
#		print('##')
#		print(sum(img[i][loc_f:loc_l+1]))
#		print(len(img[i][loc_f:loc_l+1]))
#		print(float(sum(img[i][loc_f:loc_l+1]))/float(len(img[i][loc_f:loc_l+1])))
		row_avg = row_avg + (float(len(img[i][loc_f:loc_l+1]))/float(sum(img[i][loc_f:loc_l+1])))
		y_counter += 1
	for j in xrange(int((width/2)*.75),int((width/2)*1.25),1):
		find_first = 0
		find_last = 0
		loc_f = 0
		loc_l = len(imgR[j])-1
		while find_first==0:			
			if imgR[j][loc_f]==1:
				find_first = 1
			else:
				loc_f +=1
		while find_last == 0:
			if imgR[j][loc_l]==1:
				find_last = 1
			else:
				loc_l -=1
		col_avg = col_avg + (float(len(imgR[j][loc_f:loc_l+1]))/float(sum(imgR[j][loc_f:loc_l+1])))
		x_counter += 1
	average_row_D = ((row_avg/y_counter)+(col_avg/x_counter))/2
	return average_row_D 
