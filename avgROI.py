# import the necessary packages
import cv2
import numpy as np
import imutils
#from PIL import Image as im
from io import StringIO
#import PIL
import base64



# image = cv2.imread("repl.png")

# cv2.imshow("Repl", image)
# cv2.waitKey(0)

# convert it to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def averageGray(xCoordStart, yCoordStart, width, height, startFrame, endFrame, videoInput):
  print("one" + str(type(videoInput)))
  print("two" + videoInput)
  cap = cv2.VideoCapture("thermalVideo.mp4")
   
  # take first frame of the video
  ret,frame = cap.read()
   
  # setup initial location of window
  r,h,c,w = 250,90,400,125  # simply hardcoded the values
  track_window = (c,r,w,h)
   
  # set up the ROI for tracking
  roi = frame[r:r+h, c:c+w]
  hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
  roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
  cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
   
  # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
  term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
   
  while(1):
    ret ,frame = cap.read()
   
    if ret == True:
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
   
      # apply meanshift to get the new location
      #ret, track_window = cv2.meanShift(dst, track_window, term_crit)
  
      #xCoordStart = 430
      #yCoordStart = 470
      #width = 10
      #height = 10
        
      track_window = (xCoordStart, yCoordStart, width, height)
      #print(track_window)
          
      # Draw it on image
      x,y,w,h = track_window
      img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
      #cv2.imshow('img2',img2)
  
      totalGrayValue = 0
      pixels = 0
      
      for i in range(width):
        xCoord = i + xCoordStart
        for j in range(height):
          yCoord = j + yCoordStart
  
          colorNpArray = frame[xCoord, yCoord]
          colorValue = colorNpArray.tolist()
  
          pixels += 1
          
          for rgbValue in colorValue:
            totalGrayValue = totalGrayValue + rgbValue
  
      totalGrayValue = totalGrayValue / 3
      totalGrayValue = totalGrayValue / pixels
      totalGrayValue = int(totalGrayValue)
      print(str(totalGrayValue) + " is the average grayscale value of the selected region.")

      #data = im.fromarray(img2)

      
      #file_type = data.format
      #print(file_type)
      
      #data.save("converted.png", format="png")
      
      #converted = PIL.Image.open("converted.png")
      # file_type = converted.format
      # print(file_type)
      
      # img2 To Alpha
      img2Height = img2.shape[0]
      img2Width = img2.shape[1]
      img2Pixels = img2Height * img2Width
      alpha_data = []
      alpha_width = []
      #print(str(img2Height) + str(img2Width))

      for j in range(img2Width):
        alpha_width.append(255)
      for i in range(img2Height):
        alpha_data.append(alpha_width)
        

      #print(alpha_data)
      #print(len(alpha_data[0]))
      #print(len(alpha_data))
      
      rgba = cv2.cvtColor(img2, cv2.COLOR_RGB2RGBA)
      rgba[:, :, 3] = alpha_data

      img2 = rgba.tolist()
      list = img2

      singleList = []

      #print(len(list[0][0]))   4

      for sList in list:
        for tlist in sList:
          for value in tlist:
            singleList.append(value)

      #print(len(singleList))
      

      #file_type = type(img2)

      data = {'imageData': singleList, 'grayValue': totalGrayValue, 'imgHeight': img2Height, 'imgWidth': img2Width}
      
      #print(data)
      print(type(data))
      print(type(data["imageData"]))
            
      return data
  
          #a_tolist = a.tolist()
  
      cv2.waitKey(0)
   
      k = cv2.waitKey(60) & 0xff
      if k == 27:
        break
      else:
        cv2.imwrite(chr(k)+".jpg",img2)
   
    else:
      break
   
  cv2.destroyAllWindows()
  cap.release()