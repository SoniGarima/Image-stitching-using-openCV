from imutils import paths
import numpy as np
import argparse
import cv2
import imutils

### argparse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,
	help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,
	help="path to the output image")
args = vars(ap.parse_args())
###

imagePaths = sorted(list(paths.list_images(args["images"]))) #exp - [images/s1.png,images/s2.png,images/s3.png]
images = []

for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	images.append(image)

stitcher = cv2.Stitcher_create() 
(status, stitched) = stitcher.stitch(images)
    
stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
			cv2.BORDER_CONSTANT, (0, 0, 0))
gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)

mask = np.zeros(thresh.shape, dtype="uint8")
(x, y, w, h) = cv2.boundingRect(c)
cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

minRect = mask.copy()
sub = mask.copy()
while cv2.countNonZero(sub) > 0:
    minRect = cv2.erode(minRect, None)
    sub = cv2.subtract(minRect, thresh)
    
cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)
(x, y, w, h) = cv2.boundingRect(c)
stitched = stitched[y:y + h, x:x + w]


cv2.imwrite(args["output"], stitched)
cv2.imshow("Stitched", stitched)
cv2.waitKey(0)