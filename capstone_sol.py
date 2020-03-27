import numpy as np
import cv2



def av_pix(img,circles,size):
    av_value = []
    for coords in circles[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size,coords[0]-size:coords[0]+size])
        av_value.append(col)
    return av_value 

# get radius of all cercles 
def get_radius(circles):
    radius = []
    for coords in circles[0,:]:
        radius.append(coords[2])    
    return radius


img = cv2.imread('capstone_coins.png',cv2.IMREAD_GRAYSCALE)
# original_image = cv2.imread('capstone_coins.png',1)
img = cv2.medianBlur(img,5)
cimg = cv2.imread('capstone_coins.png',1)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,90,param1=50,param2=30,minRadius=30,maxRadius=115)

print(circles)

circles = np.uint16(np.around(circles))
count = 1
for i in circles[0,:]:
    print(i)
    
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    # cv2.putText(cimg, str(count),(i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count += 1


radii = get_radius(circles)
print(radii)

bright_values = av_pix(img,circles,20)
print(bright_values)


values = []
for a,b in zip(bright_values,radii):
    if a > 150 and b > 110:
        values.append(10)
    elif a > 150 and b <= 110:
        values.append(5)
    elif a < 150 and b > 110:
        values.append(2)
    elif a < 150 and b < 110:
        values.append(1)        
print(values)           
count_2 = 0
for i in circles[0,:]:
    
    cv2.putText(cimg, str(values[count_2]) + 'p',(i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count_2 += 1
cv2.putText(cimg, 'ESTIMATED TOTAL VALUE: ' + str(sum(values)) + 'p', (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 255)


cv2.imshow('Detected Coins',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
