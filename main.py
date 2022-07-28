import cv2
import numpy as np
import imutils
from PIL import Image as im
from io import StringIO
import PIL

from avgROI import averageGray

# https://flask.palletsprojects.com/en/1.1.x/api/
from flask import Flask, render_template, url_for, request, redirect

#create a Flask instance
app = Flask(__name__)

#connects default URL of server to a python function
@app.route('/')
def home():      
  
  data = {'imageData': [[0,0,0,0]], 'grayValue': 0, 'imgHeight': 1, 'imgWidth': 1}
  
  #function use Flask import (Jinja) to render an HTML template
  return render_template("index.html", display="", data=data)

@app.route("/add", methods=['GET','POST'],)
def addition():
  if request.method == 'POST':
    form = request.form
    xCoordStart = int(form['xCoordStart'])
    yCoordStart = int(form['yCoordStart'])
    width = int(form['width'])
    height = int(form['height'])
    startFrame = int(form['startFrame'])
    endFrame = int(form['endFrame'])
    videoInput = form['file']


    # data = {'imageData': list, 'grayValue': totalGrayValue, 'imgHeight': img2Height, 'imgWidth': img2Width}

    data = averageGray(xCoordStart, yCoordStart, width, height, startFrame, endFrame, videoInput)

    #print(data)
    
    #calc = xCoordStart + yCoordStart
    return render_template("index.html", data=data)    
          
  return redirect("/index")

if __name__ == "__main__":
    app.run(debug=True, port='3000', host='0.0.0.0')