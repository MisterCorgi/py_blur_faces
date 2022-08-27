#!/bin/env python
import cv2
import sys
import random

if (len(sys.argv) == 2):
    imagePath = sys.argv[1]
else:
    imagePath="./image1.jpeg"

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(cv2.data.haarcascades)
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
features = [
    cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
]
features = [feature.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(70, 70),
    flags = cv2.CASCADE_SCALE_IMAGE
)
    for feature in features
]
print ("Found {0} faces!".format(sum(len(feature) for feature in features)))
color_index=0
for feature in features:
    # Draw a rectangle around the features
    colors = [0,0,0]
    colors[color_index]=255
    color_index+=1
    if (color_index>1):
        color_index=0
    colors = tuple(colors)
    for (x, y, w, h) in feature:
        cv2.rectangle(image, (x, y), (x+w, y+h), colors, 2)
        # Part for blurring
        eye_coords = [int(x+w*2/13), int(y+h*5/16), int(w*9/13), int(h*2/12)]
        face_coords = [int(x+w*4/13), int(y+h*3/13), int(w*5/13), int(h*9/13)]
        ex,ey,ew,eh = eye_coords
        eye_ROI = image[ey:ey+eh, ex:ex+ew]
        eye_blur = cv2.GaussianBlur(eye_ROI, (51, 51), 0)
        image[ey:ey+eh, ex:ex+ew] = eye_blur

        ex,ey,ew,eh = face_coords
        face_ROI = image[ey:ey+eh, ex:ex+ew]
        face_blur = cv2.GaussianBlur(face_ROI, (51, 51), 0)
        image[ey:ey+eh, ex:ex+ew] = face_blur

cv2.imshow("Faces found", image)
cv2.waitKey(0)
