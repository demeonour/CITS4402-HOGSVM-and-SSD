from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import datetime
import cv2
# Code mainly taken from pyimagesearch.com tutorial, with timer added
# https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
args = vars(ap.parse_args())

#create HOG and SVM
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the image path
for imagePath in paths.list_images(args["images"]):
	# loads the image and resizes it 
	image = cv2.imread(imagePath)
	image = imutils.resize(image, width=min(400, image.shape[1]))
	orig = image.copy()
	# detect people in the image and start the timer
	start = datetime.datetime.now()
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)
	#print the time it took for detection
	print("[INFO] detection took: {}s".format(
		(datetime.datetime.now() - start).total_seconds()))
	# draw the original bounding boxes
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
	# apply non-maxima suppression to the bounding boxes
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
	# draw the final bounding boxes
	for (x1, y1, x2, y2) in pick:
		cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
	# show the information on the number of bounding boxes before/after NMS
	filename = imagePath[imagePath.rfind("/") + 1:]
	print("[INFO] {}: {} original boxes, {} after suppression".format(
		filename, len(rects), len(pick)))
	# show the output images
	cv2.imshow("Before NMS", orig)
	cv2.imshow("After NMS", image)
	cv2.waitKey(0)
