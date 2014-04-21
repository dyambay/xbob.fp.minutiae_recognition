import ImageLoader as IL
import cropping as cr
import orientation as ori
import fingerRecPreprocess as frp
import fingerRecPostprocess as frpost
import fingerTemplate as ft
import bob
import os
import minutia_extract as me
np = bob.ip.numpy

size = 256
errors = []
fingerfile = '/remote/filer.gx/home.active/dyambay/Bob/FingerprintRec/CrossmatchTrain_Live2.txt'
f = open(fingerfile, 'r')
data_files = f.readlines()
galnames = data_files[0:2]
probenames = data_files[2:4]
galDic,probeDic = ft.createDic(galnames, probenames)
#for x in range(1):
for x in range(0,1):
#for x in range(len(data_files)):
    if x<=1:
        dict_type = 1
    elif x>1:
        dict_type = 2
    toLoad = data_files[x][0:len(data_files[x])-1]
	#loads selected image into an array
    loadedImage, height, width = IL.loadImage(toLoad)
        
    #Crops image around center point
    size = size+16
    CroppedPrint, errors = cr.crop(height, width, loadedImage, errors, toLoad, size)
    cropped = np.asarray(CroppedPrint, dtype='uint8')
    #savetxt = '/idiap/home/dyambay/Bob/Saved Images/CropImage'+str(x)+'.jpg'
    #bob.io.save(cropped,savetxt)
    
	#takes binary image and calculates the orientation field and then extracts ROI based on it
    orientation = frp.orientation(CroppedPrint)
    np.savetxt('/remote/filer.gx/home.active/dyambay/Bob/FingerprintRec/orient' + str(x) +'.txt',orientation)

    '''#uses histogram equalization to enhance the fingerprint image
    enhancedImage = frp.hist_equal(CroppedPrint)
    #savetxt = '/idiap/home/dyambay/Bob/Saved Images/enhanceImage'+str(x)+'.jpg'
    #bob.io.save(enhancedImage,savetxt)

	#takes the resized image and processes it to make the image a binary array of 0 and 255 values
    binaryImage = frp.bin_image(enhancedImage,size,size)
    #savetxt = '/idiap/home/dyambay/Bob/Saved Images/BinImage'+str(x)+'.jpg'
    #bob.io.save(binaryImage,savetxt)

	#takes the binarized image and thins it to single pixel lines
    thinImage = me.finger_thin(binaryImage,size, size)

	#takes the thinned image and marks minutia
    markedImage = me.extract(thinImage,size,size)

	#takes the marked image and removes false minutia
    procImage = frpost.minutiaCheck(markedImage,size,size, data_files[x],orientation, galDic, probeDic, dict_type)
    #savetxt = '/idiap/home/dyambay/Bob/Saved Images/ProcImage'+str(x)+'.jpg'
    #bob.io.save(procImage,savetxt)'''


print('Gallery of minutia points')
print(galDic)
print('Probe of minutia points')
print(probeDic)
