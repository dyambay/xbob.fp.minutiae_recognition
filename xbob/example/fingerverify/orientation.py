import bob
import scipy.signal as sp
import math as m
np = bob.ip.numpy
pi = float('%.4f' %  m.pi)
pi2 = float('%.4f' % float(pi/2))

def orient(image, height, width):
#initial filtering and solving of gradient for calculating orientation
    imgN=len(image)
    #print(imgN)
    imgM=len(image[0])
    #print(imgM)
    img = sp.wiener(image,[3, 3])
    Gy, Gx = np.gradient(img)
    orientnum = sp.wiener(2*Gx*Gy,[3,3])
    orientden = sp.wiener((Gx**2) - (Gy**2),[3,3])
    W2 = max([len(image), len(image[0])])
    W = 8
    ll = 9
    orient = np.zeros((imgN/W+1,imgM/W+1))
    #print(orient.shape)
    snum = []
    sden = []
#calculates orientation
    for i in range(1,(imgN/W)*(imgM/W)+1):
        x = m.floor((i-1)/(imgM/W))*W
        y = ((i-1)%(imgN/W))*W
        numblock = orientnum[y:y+W,x:x+W]      
        denblock = orientden[y:y+W,x:x+W]
        somma_num=sum(sum(numblock))
        snum.append(somma_num)
        somma_denom=sum(sum(denblock))
        sden.append(somma_denom)
        if somma_denom != 0:
            inside = somma_num/somma_denom
            angle = 0.5*m.atan(inside)
        else:
            angle = pi2

        if angle < 0:
            if somma_num < 0:
                angle = angle + pi2
            else:
                angle = angle + pi
        else:
            if somma_num > 0:
                angle = angle + pi2
        orient[(y)/W+1][(x)/W+1] = angle
    
    return orient[1:len(orient)+1,1:len(orient[0])+1]
