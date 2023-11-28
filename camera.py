import cv2
import os
import sys
import datetime
from time import sleep

try:
	if len(sys.argv)==1:
		print('Error: parameter lost! ')
		sys.exit()
	elif len(sys.argv)>2:
		print('Error: too many parameters! ')
		sys.exit()
	time = sys.argv[1]

	cap_0 = cv2.VideoCapture(0)
	cap_0.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
	cap_0.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
	
	cap_1 = cv2.VideoCapture(1)
	cap_1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
	cap_1.set(cv2.CAP_PROP_FRAME_WIDTH, 320)

	cap_2 = cv2.VideoCapture(2)
	cap_2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
	cap_2.set(cv2.CAP_PROP_FRAME_WIDTH, 320)

	#cv2.namedWindow('cam_0', cv2.WINDOW_NORMAL)
	#cv2.namedWindow('cam_1', cv2.WINDOW_NORMAL)
	#cv2.namedWindow('cam_2', cv2.WINDOW_NORMAL)
	
	path_name_0 = './data/' + time + '/cam_0/'
	path_name_1 = './data/' + time + '/cam_1/'
	path_name_2 = './data/' + time + '/cam_2/'
	if not os.path.exists(path_name_0):
		print('Warning: main.py has not created path cam_0!')
		os.mkdir(path_name_0)
	if not os.path.exists(path_name_1):
		print('Warning: main.py has not created path cam_1!')
		os.mkdir(path_name_1)
	if not os.path.exists(path_name_2):	
		print('Warning: main.py has not created path cam_2!')
		os.mkdir(path_name_2)
	
	i = 0
	while cap_0.isOpened() and cap_1.isOpened() and cap_2.isOpened():
		ret_0, frame_0 = cap_0.read()
		ret_1, frame_1 = cap_1.read()
		ret_2, frame_2 = cap_2.read()
		if i == 0:
			print(frame_0.shape)
			print(frame_1.shape)
			print(frame_2.shape)
			i = 1
		#cv2.imshow('cam_0', frame_0)
		#cv2.imshow('cam_1', frame_1)
		#cv2.imshow('cam_2', frame_2)
		k = cv2.waitKey(1) & 0xFF
		if k==ord('q'):
			break
		#elif k==ord('s'):
		#	time = datetime.datetime.now()
		#	time = time.strftime('%Y-%m-%d-%H-%M-%S')
		#	cv2.imwrite('./data/'+time+'.jpg', frame)
		time = datetime.datetime.now()
		time = time.strftime('%Y-%m-%d-%H-%M-%S')	
		cv2.imwrite(path_name_0 + time + '.jpg', frame_0)
		cv2.imwrite(path_name_1 + time + '.jpg', frame_1)
		cv2.imwrite(path_name_2 + time + '.jpg', frame_2)
		sleep(1)
finally:
	cap_0.release()
	cap_1.release()
	cap_2.release()
	cv2.destroyAllWindows()
	print('camera shut down!')
