import numpy as np
import cv2
import imutils
import random
import time

def drawCarOnRoad(principalFrame, car, centerWidth, centerHeight, width, height):
     roiCar = principalFrame[centerHeight:centerHeight+height, centerWidth:centerWidth+width]
     car2gray = cv2.cvtColor(car,cv2.COLOR_BGR2GRAY)
     ret, maskCar = cv2.threshold(car2gray, 10, 255, cv2.THRESH_BINARY)
     maskCarInv = cv2.bitwise_not(maskCar)   
     car_bg = cv2.bitwise_and(roiCar, roiCar, mask = maskCarInv)
     car_fg = cv2.bitwise_and(car, car, mask = maskCar)
     dstCar = cv2.add(car_bg, car_fg)
     principalFrame[centerHeight:centerHeight+height, centerWidth:centerWidth+width] = dstCar
     


cam = cv2.VideoCapture(0)

#Blue
#lowerBound = np.array([82,51,51])
#upperBound = np.array([133,255,255])

#Yellow
#lowerBound = np.array([56,100,50])
#upperBound = np.array([60,100,60])

#Green
lowerBound = np.array([25, 52, 72])
upperBound = np.array([102, 255, 255])
  
points = 0
width = 40
height = 70

road = cv2.imread("road.png")
road = cv2.resize(road, (500,600))

car = cv2.imread('car.png')
car = cv2.resize(car,(width,height))

redCar = cv2.imread('redCar.png')
redCar = cv2.resize(redCar,(width,height))

blueCar = cv2.imread('blueCar.png')
blueCar = cv2.resize(blueCar,(width,height))

yellowCar = cv2.imread('yellowCar.png')
yellowCar = cv2.resize(yellowCar,(width,height))

listCenter = []
listVelocity = []


for i in range(3):
    centerRandom = (random.randint(100,360), 0)
    listCenter.append(centerRandom)

    velocity = random.randint(3,8)
    listVelocity.append(velocity)
    
execute = True
while execute:
    
    return_value, roadFighter = cam.read()
    roadFighter = cv2.flip(roadFighter,1) 
    roadFighter = cv2.resize(roadFighter, (500,600))
    blurred_frame = cv2.GaussianBlur(roadFighter, (11,11), 0)          
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

           
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contorno = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contorno = imutils.grab_contours(contorno)
   
    if(len(contorno) > 0):
        c = max(contorno, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        centerOfWhiteCar = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
       
        #Add Road to the principal frame
        roiRoad = roadFighter[0:600, 0:500]  
        road2gray = cv2.cvtColor(road,cv2.COLOR_BGR2GRAY)
        ret, maskRoad = cv2.threshold(road2gray, 10, 255, cv2.THRESH_BINARY)
        maskRoadInv = cv2.bitwise_not(maskRoad)   
        road_bg = cv2.bitwise_and(roiRoad, roiRoad, mask = maskRoadInv)
        road_fg = cv2.bitwise_and(road, road, mask = maskRoad)
        dstRoad = cv2.add(road_bg,road_fg)
        roadFighter[0:600, 0:500] = dstRoad
            
        #Validate the center of white car to avoid get out of the road
        if(centerOfWhiteCar[0] < 100):
            centerOfWhiteCar = (100,500)
        #End if
        
        if(centerOfWhiteCar[0] > 360):
            centerOfWhiteCar = (360,500)
        #End if
        
        drawCarOnRoad(roadFighter, car, centerOfWhiteCar[0], 500, width, height)
        drawCarOnRoad(roadFighter, blueCar, listCenter[0][0], listCenter[0][1], width, height)
        drawCarOnRoad(roadFighter, redCar, listCenter[1][0], listCenter[1][1], width, height)
        drawCarOnRoad(roadFighter, yellowCar, listCenter[2][0], listCenter[2][1], width, height)
        
        for i in range(len(listCenter)):
            
            #If the car doesn't crash
            if(listCenter[i][1] > 500):
                listCenter[i] = (random.randint(100,360), 0)
                points += 15*listVelocity[i]
                listVelocity[i] = random.randint(3,15)

            else: 
                time.sleep(0.0016)
                listCenter[i] = (listCenter[i][0],listCenter[i][1]+listVelocity[i])
            #End if
        # End for
    #End if
    
        for i in range(len(listCenter)):
           if((-45 < centerOfWhiteCar[0] - listCenter[i][0] and centerOfWhiteCar[0] - listCenter[i][0] < 45) and listCenter[i][1] >= 430):
              
               while True:
                   gameover = cv2.imread('gameover.png')
                   gameover = cv2.resize(gameover,(400,400))
                   cv2.putText(gameover, "YOU GOT "+ str(points) + " POINTS", (50,350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2) 
                   cv2.imshow("Road Fighter",gameover)
                   
                   if cv2.waitKey(1) & 0xFF == ord('q'):
                       execute = False
                       break
                  #End if
                #End while
            #End if
        #End for
               
    cv2.putText(roadFighter, "POINTS: "+ str(points), (180,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2) 
    cv2.imshow('Road Fighter',roadFighter) 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #End if
#End while
    
cam.release()
cv2.destroyAllWindows()


