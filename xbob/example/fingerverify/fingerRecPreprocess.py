import bob
import math as m
import scipy.ndimage as sci
import scipy.signal as scis
np = bob.ip.numpy
sp=bob.sp
ip=bob.ip


##############################################################
##############################################################

#function that uses built-in bob function to perform histogram
#equalization. This is for image enhancement.
#returns enhanced image
def hist_equal(image):
	img = np.asarray(image, dtype='uint8')
	img = bob.ip.histogram_equalization(img)
	gauss = ip.Gaussian()
	imag = gauss(img)
	return np.asarray(imag,dtype='uint8')


####################################################################
####################################################################

#for processing steps the image needs to have both height and width
#divisible by 32 (requires 16x16 blocks but fft enhancing method requires 32x32 blocks). This function checks the size of the image and zeros pads the right and bottom of the image to make the image size divisible by 32
def img_size(image):
	#intial height and width of image. If image is right size, these values get returned
	height=len(image)
	width=len(image[0])
#checks height of image
	if (height%32)!=0:
#calculates how many pixels the image is off in height and creates a block of zeros with the missing pixels
		addheight = height%32
		hb = np.zeros((32-addheight, width))
#since in python white is 255, changes the zero block to 255 elements
		h_block = [x+255 for x in hb] 
#adds the block to the bottom of the original matrix
		image = np.concatenate((image,h_block),axis=0)
#saves new height of the image
		height = len(image)
#checks width of the image
	if (width%32)!=0:
#calculates how many pixels the image is off in width and creates a block of zeros with the missing pixels
		addwidth = width%32
		wb = np.zeros((height,32-addwidth))
#since in python white is 255, changes the zero block to 255 elements
		w_block = [x+255 for x in wb] 
#adds the block to the right of the original matrix
		image = np.concatenate((image,w_block),axis=1)
#saves new width of image
		width = len(image[0])
#returns values for future functions
	return image,height, width

#################################################################
#################################################################


#function to binarize the image
def bin_image(image,height,width):
#iterates through the image in 16x16 boxes
    for i in xrange(0,height-15,16):
        for j in xrange(0,width-15,16):
#creates a box of each 16x16 set of pixels
            box=image[i:i+16,j:j+16]
#calculates overall mean of that box
            box_mean = np.mean(box)
#iterates through each pixel inside of the box
            for k in range(0,np.size(box)):
#checks if the value of the pixel is greater or less than the mean and adjusts the pixel value to 0 if less than the mean and 255 if greater than the mean
                if box[int(m.floor((k)/16))][int(k%16)]<box_mean*.95:
                    image[i+int(m.floor((k)/16))][j+int(k%16)]=0
                elif box[int(m.floor((k)/16))][int(k%16)]>=box_mean*.95:
                    image[i+int(m.floor((k)/16))][j+int(k%16)]=255
#returns the image
    return np.asarray(image, dtype="uint8")


#################################################################
#################################################################

def orientation(I):
	I = np.asarray(I, dtype = 'float')
	np.savetxt('/remote/filer.gx/home.active/dyambay/Bob/FingerprintRec/I0.txt',I) 
	#size of smoothing filter
	fsize = 31

	#Sobel Operators
	fy = np.array([[-1, 0, -1], [-1, 0, -1], [-1, 0, -1]])
	fx = np.array([[-1, -1, -1],[0,0,0],[-1,-1,-1]])
	np.savetxt('/remote/filer.gx/home.active/dyambay/Bob/FingerprintRec/fx0.txt',fx)
	np.savetxt('/remote/filer.gx/home.active/dyambay/Bob/FingerprintRec/fy0.txt',fy)

	#filter image to get x and y gradients
	dy = scis.correlate(I,fy)
	dx = scis.correlate(I,fx)
	np.savetxt('/remote/filer.gx/home.active/dyambay/Bob/FingerprintRec/dy0.txt',dy)
	np.savetxt('/remote/filer.gx/home.active/dyambay/Bob/FingerprintRec/dx0.txt',dx)

	#compute orientation
	theta = np.arctan2( 2*dx*dy,dx**2 - dy**2 )

	#filter orientation
	#compute a continuous field from theta
	phix = np.cos(theta)
	phiy = np.sin(theta)

	#construct smoothing filter kernel
	filt = np.ones((fsize,fsize))/(fsize*fsize)

	#filter continuous field components
	phi2x = scis.correlate(phix,filt)
	phi2y = scis.correlate(phiy,filt)

	#computer filtered orientation
	orient = np.atan2( phi2y,phi2x)*.5
	return orient
    


