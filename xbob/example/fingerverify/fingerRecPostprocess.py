import bob
import math as m
import fingerTemplate as ft
np=bob.ip.numpy

def minutiaCheck(image,height,width, name,orient, galDic, probeDic, dict_type):
    #converts the image to integers for use with scaling and inverting
    img = np.asarray(image,dtype='float')
    #goes through the image in 13x13 blocks finding minutia points
    for i in xrange(2,height-14,1):
        for j in xrange(2,width-14,1):
            #creates 13x13 boxes
            box=((img[i:i+13,j:j+13]/255)-1)*-1
            
            #ridge ending
            #ridge ending
            box = np.around(box,decimals = 1)
            #if box[6][6]>0:
                #print(box[6][6])
            if box[6][6] == .5:
                #print(box)
                #creates a check marker to know when the point is finished with processing before further work
                check=0
                #changes the minutia point value
                box[6][6]=.9
                #creates 3x3 box with the minutia point in the center
                box2=box[5:8,5:8]
                #iterates through the 3x3 block to find pixels that are part of the fingeprint and edit them to a 2 in order to check for 2 to 0 transitions after the bigger block is processed
                for k in range(0,np.size(box2)):
                    if box2[int(m.floor((k)/4))][int(k%3)] == 1 or box2[int(m.floor((k)/4))][int(k%3)] == .5 or box2[int(m.floor((k)/4))][int(k%3)] == .7:
                        box[5+int(m.floor((k)/4))][5+int(k%3)]=2
                        #marks the location of a changed pixel to be used as the new center block for the next box moving along the fingerprint ridge changing the values
                        #loc 1 is the row number
                        loc1 = 5+int(m.floor((k)/4))                        
                        #loc 2 is the column number
                        loc2 = 5+int(k%3)
                if 'loc1' in locals():
                    pass
                else:
                    img[i+6][j+6] == 0
                    loc1 = 6
                    loc2 = 6               
                        
                split_loc = []
                #creates a loop to follow the fingerprint ridge and change all ridge pixels to 2 until no more pixels are adjacent to the pixel
                while check==0:
                    #Looks to see if the center point is against the outside rim of the box and thus cannot create a 3x3 box and creates a 2x2 2x3 oe 3x2 box. If it isn't against the outside rim then a 3x3 box is created
                    if loc2==0:
                        side = 2
                        if loc1==0:
                            box2 = box[loc1:loc1+2,loc2:loc2+2]
                            r_size = 2
                            c_size = 2
                            
                        elif 0<loc1<12:
                            box2 = box[loc1-1:loc1+2,loc2:loc2+2]
                            r_size = 2
                            c_size = 2
                        
                        elif loc1==12:
                            box2 = box[loc1-1:loc1+1,loc2:loc2+2]
                            r_size = 2
                            c_size = 2
                        
                    elif 0<loc2<12:
                        side = 0
                        if loc1==0:
                            box2 = box[loc1:loc1+2,loc2-1:loc2+2]
                            r_size = 3
                            c_size = 3
                            side = 1
                        elif loc1==12:
                            box2 = box[loc1-1:loc1+1,loc2-1:loc2+2]
                            r_size = 3
                            c_size = 3
                        else:
                            box2 = box[loc1-1:loc1+2,loc2-1:loc2+2]
                            r_size = 3
                            c_size = 3
                    elif loc2==12:
                        side = 0
                        if loc1==0:
                            box2 = box[loc1:loc1+2,loc2-1:loc2+1]
                            r_size = 2
                            c_size = 2
                            side = 1
                        elif 0<loc1<12:
                            box2 = box[loc1-1:loc1+2,loc2-1:loc2+1]
                            r_size = 2
                            c_size = 2
                        elif loc1==12:
                            box2 = box[loc1-1:loc1+1,loc2-1:loc2+1]
                            r_size = 2
                            c_size = 2
                    count = 0
                    count2 = 0
                    for k in range(0,np.size(box2)):
                        """print('locations')
                        print(loc1)
                        print(loc2)
                        print(k)
                        print(box2[int(m.floor(k/r_size))][int(k%c_size)])
                        raw_input("Press Enter to continue...")"""
                        if box2[int(m.floor(k/r_size))][int(k%c_size)] == 1 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .5 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .7:
                            #a pixel can have up to 4 neighboring pixels that are 1 and 1 of them is already changed to a 2 based on the principle that the boxes are following the ridge so there needs to be a potential 3 checks.
                            if side == 0: 
                                if count == 0:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    loc3 = loc1-1+int(m.floor((k)/r_size))
                                    loc4 = loc2-1+int(k%c_size)
                                    count += 1
                                elif count == 1:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1
                                elif count == 2:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1
                            ########################        
                            elif side == 1: 
                                if count == 0:
                                    box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    loc3 = loc1+int(m.floor((k)/r_size))
                                    loc4 = loc2-1+int(k%c_size)
                                    count += 1
                                elif count == 1:
                                    box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                    split_loc.append(loc1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1
                                elif count == 2:
                                    box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    split_loc.append(loc1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1  
                            ######################
                            elif side == 2:
                                if count == 0:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                    loc3 = loc1-1+int(m.floor((k)/r_size))
                                    loc4 = loc2+int(k%c_size)
                                    count += 1
                                elif count == 1:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                    #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2+int(k%c_size))
                                    count += 1
                                elif count == 2:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2+int(k%c_size))
                                    count += 1            
                    #print(count)                                
                    loc1 = loc3
                    loc2 = loc4                        
                    #if no pixels are found to be changed then it sets the check variable to 1 to exit the while loop                
                    if count == 0:
                        check = 1
                check = 0
                while check==0 :
                    #Moves to the saved locations and begins to check again based on same logic as above and if it hits another intersection the new location is saved and then checked the next time this is reached
                    check2 = 0
                    while check2 == 0:
                        
                        split_size = len(split_loc)
                        for n in xrange(0,len(split_loc)-1,2):
                            """print(box)
                            print('pre locations')
                            print(split_loc[n])
                            print(split_loc[n+1])"""
                            #print(n)
                            if split_loc[n+1]==0:
                                side = 2
                                if split_loc[n]==0:
                                    box2 = box[split_loc[n]:split_loc[n]+2,split_loc[n+1]:split_loc[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                elif 0<split_loc[n]<12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+2,split_loc[n+1]:split_loc[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                elif split_loc[n]==12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+1,split_loc[n+1]:split_loc[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                            elif 0<split_loc[n+1]<12:
                                side = 0
                                if split_loc[n]==0:
                                    box2 = box[split_loc[n]:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                    side = 1
                                elif split_loc[n]==12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+1,split_loc[n+1]-1:split_loc[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                else:
                                    #creates new 3x3 box off of the changed pixel from above
                                    box2 = box[split_loc[n]-1:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                            elif split_loc[n+1]==12:
                                side = 0
                                if split_loc[n]==0:
                                    box2 = box[split_loc[n]:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                    side = 1
                                elif 0<split_loc[n]<12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                elif split_loc[n]==12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+1,split_loc[n+1]-1:split_loc[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                            count2 = 0
                            loc1 = split_loc[n]
                            loc2 = split_loc[n+1]
                            #print(box2)
                            for k in range(0,np.size(box2)):
                                """print('locations')
                                print(loc1)
                                print(loc2)
                                print(k)
                                print(box2[int(m.floor(k/r_size))][int(k%c_size)])
                                raw_input("Press Enter to continue...")"""
                                if box2[int(m.floor((k)/r_size))][int(k%c_size)] == 1 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .5 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .7:
                                    if side == 0: 
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                    ########################        
                                    elif side == 1: 
                                        if count2 == 0:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            loc3 = loc1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            split_loc.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1  
                                    ######################
                                    elif side == 2:
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2+int(k%c_size))
                                            count2 += 1  
                        if len(split_loc)==split_size:
                            check2=1
                    if count2 == 0:
                        check = 1
            #created a blank list and 4 variables representing the outside rim of the 13x13 box.
                box_ar = np.asarray(box,dtype='int')
                a_box = []
                box_1st = box_ar[0]
                box_2nd = box_ar[:,12]
                box_3rd = box_ar[12][::-1]
                box_4th = box_ar[:,0][::-1]
                #goes along the outside rim of the box and subtracts each value from the next value
                for i1 in xrange(0,len(box_1st)-2,1):
                    a_box.append(box_1st[i1]-box_1st[i1+1])
                for i2 in xrange(0,len(box_2nd)-2,1):
                    a_box.append(box_2nd[i2]-box_2nd[i2+1])
                for i3 in xrange(0,len(box_3rd)-2,1):
                    a_box.append(box_3rd[i3]-box_3rd[i3+1])
                for i4 in xrange(0,len(box_4th)-2,1):
                    a_box.append(box_4th[i4]-box_4th[i4+1])
                #currently checking 2 to 0 transitions so all other values need to be 0'd out
                a_box2 = a_box
                a_box2 = [0 if x==-2 else x for x in a_box2]
                a_box2 = [0 if x==1 else x for x in a_box2]
                a_box2 = [0 if x==-1 else x for x in a_box2]
                a_box2 = [1 if x==2 else x for x in a_box2]
                if sum(a_box2) != 1:
                    img[i+6][j+6] == 0
                    del loc1
                    del loc2
                else:
                    pass
                    del loc1
                    del loc2
                    #orientation = orient[i+6][j+6]
                    #galDic,probeDic = ft.savetoDic(name, i+6, j+6,img[i+6][j+6], orientation ,dict_type, galDic, probeDic, value)
#############################################
#############################################
            #ridge bifurcation
            if box[6][6] == .7:
                #creates a check marker to know when the point is finished with processing before further work
                check=0
                #changes the minutia point value
                box[6][6]=.9
                #creates 3x3 box with the minutia point in the center
                box2=box[5:8,5:8]
                split_loc = []
                split_loc3 = []
                split_loc4 = []
                count = 0
                #iterates through the 3x3 block to find pixels that are part of the fingeprint and edit them to a 2 in order to check for 2 to 0 transitions after the bigger block is processed
                for k in range(0,np.size(box2)):
                    if box2[int(m.floor((k)/3))][int(k%3)] == 1 or box2[int(m.floor((k)/3))][int(k%3)] == .5 or box2[int(m.floor((k)/3))][int(k%3)] == .7:
                        if count == 0:
                            box[5+int(m.floor((k)/3))][5+int(k%3)]=2
                            #marks the location of a changed pixel to be used as the new center block for the next box moving along the fingerprint ridge changing the values
                            #loc 1 is the row number
                            loc1 = 5+int(m.floor((k)/3))                        
                            #loc 2 is the column number
                            loc2 = 5+int(k%3)
                            count += 1
                        elif count == 1:
                            box[5+int(m.floor((k)/3))][5+int(k%3)]=3
                            split_loc3.append(loc1-1+int(m.floor((k)/3)))
                            split_loc3.append(loc2-1+int(k%3))
                            count += 1
                        elif count == 2:
                            box[5+int(m.floor((k)/3))][5+int(k%3)]=4
                            split_loc4.append(loc1-1+int(m.floor((k)/3)))
                            split_loc4.append(loc2-1+int(k%3))
                            count += 1
                if 'loc1' in locals():
                    pass
                else:
                    img[i+6][j+6] == 0
                    loc1 = 6
                    loc2 = 6            
                #creates a loop to follow the fingerprint ridge and change all ridge pixels to 2 until no more pixels are adjacent to the pixel
                while check==0:
                    #Looks to see if the center point is against the outside rim of the box and thus cannot create a 3x3 box and creates a 2x2 2x3 oe 3x2 box. If it isn't against the outside rim then a 3x3 box is created
                    if loc2==0:
                        side = 2
                        if loc1==0:
                            box2 = box[loc1:loc1+2,loc2:loc2+2]
                            r_size = 2
                            c_size = 2
                        elif 0<loc1<12:
                            box2 = box[loc1-1:loc1+2,loc2:loc2+2]
                            r_size = 2
                            c_size = 2
                        elif loc1==12:
                            box2 = box[loc1-1:loc1+1,loc2:loc2+2]
                            r_size = 2
                            c_size = 2
                    elif 0<loc2<12:
                        side = 0
                        if loc1==0:
                            box2 = box[loc1:loc1+2,loc2-1:loc2+2]
                            r_size = 3
                            c_size = 3
                            side = 1
                        elif loc1==12:
                            box2 = box[loc1-1:loc1+1,loc2-1:loc2+2]
                            r_size = 3
                            c_size = 3
                        else:
                            box2 = box[loc1-1:loc1+2,loc2-1:loc2+2]
                            r_size = 3
                            c_size = 3
                    elif loc2==12:
                        side = 0
                        if loc1==0:
                            box2 = box[loc1:loc1+2,loc2-1:loc2+1]
                            r_size = 2
                            c_size = 2
                            side = 1
                        elif 0<loc1<12:
                            box2 = box[loc1-1:loc1+2,loc2-1:loc2+1]
                            r_size = 2
                            c_size = 2
                        elif loc1==12:
                            box2 = box[loc1-1:loc1+1,loc2-1:loc2+1]
                            r_size = 2
                            c_size = 2
                    count = 0
                    count2 = 0
                    for k in range(0,np.size(box2)):
                        '''print('locations')
                        print(loc1)
                        print(loc2)'''
                        if box2[int(m.floor((k)/r_size))][int(k%c_size)] == 1 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .5 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .7:
                            #a pixel can have up to 4 neighboring pixels that are 1 and 1 of them is already changed to a 2 based on the principle that the boxes are following the ridge so there needs to be a potential 3 checks.
                            if side == 0: 
                                if count == 0:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    loc3 = loc1-1+int(m.floor((k)/r_size))
                                    loc4 = loc2-1+int(k%c_size)
                                    count+= 1
                                elif count == 1:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                        #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1
                                elif count == 2:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1
                                ########################        
                            elif side == 1: 
                                if count == 0:
                                    box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    loc3 = loc1+int(m.floor((k)/r_size))
                                    loc4 = loc2-1+int(k%c_size)
                                    count += 1
                                elif count == 1:
                                    box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                        #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                    split_loc.append(loc1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1
                                elif count == 2:
                                    box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                    split_loc.append(loc1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2-1+int(k%c_size))
                                    count += 1  
                                ######################
                            elif side == 2:
                                if count == 0:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                    loc3 = loc1-1+int(m.floor((k)/r_size))
                                    loc4 = loc2+int(k%c_size)
                                    count += 1
                                elif count == 1:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                        #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2+int(k%c_size))
                                    count += 1
                                elif count == 2:
                                    box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                    split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                    split_loc.append(loc2+int(k%c_size))
                                    count += 1                     
                    loc1 = loc3
                    loc2 = loc4                        
                    #if no pixels are found to be changed then it sets the check variable to 1 to exit the while loop                
                    if count == 0:
                        check = 1

                check = 0
                while check==0 :
                    #Moves to the saved locations and begins to check again based on same logic as above and if it hits another intersection the new location is saved and then checked the next time this is reached
                    check2 = 0
                    while check2 == 0:
                        split_size = len(split_loc)
                        for n in xrange(0,len(split_loc)-1,2):
                            if split_loc[n+1]==0:
                                side = 2
                                if split_loc[n]==0:
                                    box2 = box[split_loc[n]:split_loc[n]+2,split_loc[n+1]:split_loc[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                elif 0<split_loc[n]<12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+2,split_loc[n+1]:split_loc[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                elif split_loc[n]==12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+1,split_loc[n+1]:split_loc[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                            elif 0<split_loc[n+1]<12:
                                side = 0
                                if split_loc[n]==0:
                                    box2 = box[split_loc[n]:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                    side = 1
                                elif split_loc[n]==12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+1,split_loc[n+1]-1:split_loc[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                else:
                                    #creates new 3x3 box off of the changed pixel from above
                                    box2 = box[split_loc[n]-1:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                            elif split_loc[n+1]==12:
                                side = 0
                                if split_loc[n]==0:
                                    box2 = box[split_loc[n]:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                    side = 1
                                elif 0<split_loc[n]<12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+2,split_loc[n+1]-1:split_loc[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                elif split_loc[n]==12:
                                    box2 = box[split_loc[n]-1:split_loc[n]+1,split_loc[n+1]-1:split_loc[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                            count2 = 0
                            loc1 = split_loc[n]
                            loc2 = split_loc[n+1]
                            for k in range(0,np.size(box2)):
                                '''print('locations')
                                print(loc1)
                                print(loc2)'''
                                if box2[int(m.floor((k)/r_size))][int(k%c_size)] == 1 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .5 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .7:
                                    if side == 0: 
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                    ########################        
                                    elif side == 1: 
                                        if count2 == 0:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            loc3 = loc1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=2
                                            split_loc.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2-1+int(k%c_size))
                                            count2 += 1  
                                    ######################
                                    elif side == 2:
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=2
                                            split_loc.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc.append(loc2+int(k%c_size))
                                            count2 += 1  
                        if len(split_loc)==split_size:
                            check2=1
                    if count2 == 0:
                        check = 1
                #creates the number 3's
                check = 0
                while check==0 :
                    #Moves to the saved locations and begins to check again based on same logic as above and if it hits another intersection the new location is saved and then checked the next time this is reached
                    check2 = 0
                    while check2 == 0:
                        split_size = len(split_loc3)
                        for n in xrange(0,len(split_loc3)-1,2):
                            if split_loc3[n+1]==0:
                                side = 2
                                if split_loc3[n]==0:
                                    box2 = box[split_loc3[n]:split_loc3[n]+2,split_loc3[n+1]:split_loc3[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                elif 0<split_loc3[n]<12:
                                    
                                    box2 = box[split_loc3[n]-1:split_loc3[n]+2,split_loc3[n+1]:split_loc3[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                    
                                elif split_loc3[n]==12:
                                    box2 = box[split_loc3[n]-1:split_loc3[n]+1,split_loc3[n+1]:split_loc3[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                            elif 0<split_loc3[n+1]<12:
                                side = 0
                                if split_loc3[n]==0:
                                    box2 = box[split_loc3[n]:split_loc3[n]+2,split_loc3[n+1]-1:split_loc3[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                    side = 1
                                elif split_loc3[n]==12:
                                    box2 = box[split_loc3[n]-1:split_loc3[n]+1,split_loc3[n+1]-1:split_loc3[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                else:
                                    #creates new 3x3 box off of the changed pixel from above
                                    box2 = box[split_loc3[n]-1:split_loc3[n]+2,split_loc3[n+1]-1:split_loc3[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                            elif split_loc3[n+1]==12:
                                side = 0
                                if split_loc3[n]==0:
                                    box2 = box[split_loc3[n]:split_loc3[n]+2,split_loc3[n+1]-1:split_loc3[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                    side = 1
                                elif 0<split_loc3[n]<12:
                                    box2 = box[split_loc3[n]-1:split_loc3[n]+2,split_loc3[n+1]-1:split_loc3[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                elif split_loc3[n]==12:
                                    box2 = box[split_loc3[n]-1:split_loc3[n]+1,split_loc3[n+1]-1:split_loc3[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                            count2 = 0
                            loc1 = split_loc3[n]
                            loc2 = split_loc3[n+1]
                            for k in range(0,np.size(box2)):
                                '''print('locations')
                                print(loc1)
                                print(loc2)'''
                                if box2[int(m.floor((k)/r_size))][int(k%c_size)] == 1 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .5 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .7:
                                    if side == 0: 
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc3.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc3.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            split_loc3.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc3.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                    ########################        
                                    elif side == 1: 
                                        if count2 == 0:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            loc3 = loc1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc3.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc3.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            split_loc3.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc3.append(loc2-1+int(k%c_size))
                                            count2 += 1  
                                    ######################
                                    elif side == 2:
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=3
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=3
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc3.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc3.append(loc2+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=3
                                            split_loc3.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc3.append(loc2+int(k%c_size))
                                            count2 += 1  
                        if len(split_loc3)==split_size:
                            check2=1
                    if count2 == 0:
                        check = 1
                #creates the number 4's
                check = 0
                while check==0 :
                    #Moves to the saved locations and begins to check again based on same logic as above and if it hits another intersection the new location is saved and then checked the next time this is reached
                    check2 = 0
                    while check2 == 0:
                        split_size = len(split_loc4)
                        for n in xrange(0,len(split_loc4)-1,2):
                            if split_loc4[n+1]==0:
                                side = 2
                                if split_loc4[n]==0:
                                    box2 = box[split_loc4[n]:split_loc4[n]+2,split_loc4[n+1]:split_loc4[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                elif 0<split_loc4[n]<12:
                                    box2 = box[split_loc4[n]-1:split_loc4[n]+2,split_loc4[n+1]:split_loc4[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                                elif split_loc4[n]==12:
                                    box2 = box[split_loc4[n]-1:split_loc4[n]+1,split_loc4[n+1]:split_loc4[n+1]+2]
                                    r_size = 2
                                    c_size = 2
                            elif 0<split_loc4[n+1]<12:
                                side = 0
                                if split_loc4[n]==0:
                                    box2 = box[split_loc4[n]:split_loc4[n]+2,split_loc4[n+1]-1:split_loc4[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                    side = 1
                                elif split_loc4[n]==12:
                                    box2 = box[split_loc4[n]-1:split_loc4[n]+1,split_loc4[n+1]-1:split_loc4[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                                else:
                                    #creates new 3x3 box off of the changed pixel from above
                                    box2 = box[split_loc4[n]-1:split_loc4[n]+2,split_loc4[n+1]-1:split_loc4[n+1]+2]
                                    r_size = 3
                                    c_size = 3
                            elif split_loc4[n+1]==12:
                                side = 0
                                if split_loc4[n]==0:
                                    box2 = box[split_loc4[n]:split_loc4[n]+2,split_loc4[n+1]-1:split_loc4[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                    side = 1
                                elif 0<split_loc4[n]<12:
                                    box2 = box[split_loc4[n]-1:split_loc4[n]+2,split_loc4[n+1]-1:split_loc4[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                                elif split_loc4[n]==12:
                                    box2 = box[split_loc4[n]-1:split_loc4[n]+1,split_loc4[n+1]-1:split_loc4[n+1]+1]
                                    r_size = 2
                                    c_size = 2
                            count2 = 0
                            loc1 = split_loc4[n]
                            loc2 = split_loc4[n+1]
                            for k in range(0,np.size(box2)):
                                '''print('locations')
                                print(loc1)
                                print(loc2)'''
                                if box2[int(m.floor((k)/r_size))][int(k%c_size)] == 1 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .5 or box2[int(m.floor((k)/r_size))][int(k%c_size)] == .7:
                                    if side == 0: 
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc4.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc4.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            split_loc4.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc4.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                    ########################        
                                    elif side == 1: 
                                        if count2 == 0:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            loc3 = loc1+int(m.floor((k)/r_size))
                                            loc4 = loc2-1+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc4.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc4.append(loc2-1+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1+int(m.floor((k)/r_size))][loc2-1+int(k%c_size)]=3
                                            split_loc4.append(loc1+int(m.floor((k)/r_size)))
                                            split_loc4.append(loc2-1+int(k%c_size))
                                            count2 += 1  
                                    ######################
                                    elif side == 2:
                                        if count2 == 0:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=3
                                            loc3 = loc1-1+int(m.floor((k)/r_size))
                                            loc4 = loc2+int(k%c_size)
                                            count2 += 1
                                        elif count2 == 1:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=3
                                            #appends any addition neighboring 1s to a list to be checked later The code will continue along one ridge and then move to other ridges based on saved locations
                                            split_loc4.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc4.append(loc2+int(k%c_size))
                                            count2 += 1
                                        elif count2 == 2:
                                            box[loc1-1+int(m.floor((k)/r_size))][loc2+int(k%c_size)]=3
                                            split_loc4.append(loc1-1+int(m.floor((k)/r_size)))
                                            split_loc4.append(loc2+int(k%c_size))
                                            count2 += 1 
                        if len(split_loc4)==split_size:
                            check2=1
                    if count2 == 0:
                        check = 1
            #created a blank list and 4 variables representing the outside rim of the 13x13 box.
                box_ar = np.asarray(box,dtype='int')
                a_box = []
                box_1st = box_ar[0]
                box_2nd = box_ar[:,12]
                box_3rd = box_ar[12][::-1]
                box_4th = box_ar[:,0][::-1]
                #goes along the outside rim of the box and subtracts each value from the next value
                for i1 in xrange(0,len(box_1st)-2,1):
                    a_box.append(box_1st[i1]-box_1st[i1+1])
                for i2 in xrange(0,len(box_2nd)-2,1):
                    a_box.append(box_2nd[i2]-box_2nd[i2+1])
                for i3 in xrange(0,len(box_3rd)-2,1):
                    a_box.append(box_3rd[i3]-box_3rd[i3+1])
                for i4 in xrange(0,len(box_4th)-2,1):
                    a_box.append(box_4th[i4]-box_4th[i4+1])
                #currently checking 2 to 0 transitions so all other values need to be 0'd out
                a_box2 = a_box
                a_box2 = [0 if x==-2 else x for x in a_box2]
                a_box2 = [0 if x==1 else x for x in a_box2]
                a_box2 = [0 if x==-1 else x for x in a_box2]
                a_box2 = [0 if x==-3 else x for x in a_box2]
                a_box2 = [0 if x==3 else x for x in a_box2]
                a_box2 = [0 if x==-4 else x for x in a_box2]
                a_box2 = [0 if x==4 else x for x in a_box2]
                a_box2 = [1 if x==2 else x for x in a_box2]
                #currently checking 3 to 0 transitions so all other values need to be 0'd out
                a_box3 = a_box
                a_box3 = [0 if x==-3 else x for x in a_box3]
                a_box3 = [0 if x==1 else x for x in a_box3]
                a_box3 = [0 if x==-1 else x for x in a_box3]
                a_box3 = [0 if x==-2 else x for x in a_box3]
                a_box3 = [0 if x==2 else x for x in a_box3]
                a_box3 = [0 if x==-4 else x for x in a_box3]
                a_box3 = [0 if x==4 else x for x in a_box3]
                a_box3 = [1 if x==3 else x for x in a_box3]
                #currently checking 4 to 0 transitions so all other values need to be 0'd out
                a_box4 = a_box
                a_box4 = [0 if x==-4 else x for x in a_box4]
                a_box4 = [0 if x==1 else x for x in a_box4]
                a_box4 = [0 if x==-1 else x for x in a_box4]
                a_box4 = [0 if x==-2 else x for x in a_box4]
                a_box4 = [0 if x==2 else x for x in a_box4]
                a_box4 = [0 if x==-3 else x for x in a_box4]
                a_box4 = [0 if x==3 else x for x in a_box4]
                a_box4 = [1 if x==4 else x for x in a_box4]

                if sum(a_box2)!= 1 and sum(a_box3)!= 1 and sum(a_box4)!= 1:
                    img[i+6][j+6] == 0
                    del loc1
                    del loc2
                else:
                    pass
                    del loc1
                    del loc2
                    #orientation = orient[i+6][j+6]
                    #galDic,probeDic = ft.savetoDic(name, i+6, j+6,img[i+6][j+6],orientation,dict_type, galDic, probeDic)
    return np.asarray(img,dtype='uint8')#, galDic, probeDic
