# USAGE
# python real_time_object_detection.py --image [Path-to-image]
# no [Path-to-image] uses camera instead
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import datetime
import cv2

#Code mainly taken from https://www.pyimagesearch.com/2017/09/18/real-time-object-detection-with-deep-learning-and-opencv/
# Args reduced, image path added and timers added
#parse the argument(s)
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to image")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASS = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
#colors for each classes for bounding boxes to be drawn
COLOR = np.random.uniform(0, 255, size=(len(CLASS), 3))

# load the caffe model
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")

if(args["image"] != None):
	vs = cv2.imread(args["image"])
else:
	vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
	
	#try videostream vs path to image
	try:
		frame = vs.read()
	except:
		frame = vs
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = imutils.resize(frame, width=400)

	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# pass the blob through the network
	# and get predictions/detections
	net.setInput(blob)
	start = datetime.datetime.now()
	detections = net.forward()
	print("[INFO] detection took: {}s".format(
		(datetime.datetime.now() - start).total_seconds()))
	# loop through detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence/probability associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		#filter out weak detections with confidence
		if confidence > args["confidence"]:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# draw the bounding box and text on the frame
			label = "{}: {:.2f}%".format(CLASS[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLOR[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR[idx], 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

fps.stop()
#cleanup
cv2.destroyAllWindows()
vs.stop()
