import time
import pyfirmata2
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox

# Initialize connection to the Arduino Mega board on COM9
board = pyfirmata2.ArduinoMega('COM9')

while(True):
    # Video 1
    # Open the RTSP video stream from the first camera
    rtsp_link1 = 'rtsp://admin:admin12345@192.168.1.108:554/live'
    cap = cv2.VideoCapture(rtsp_link1)

    # Check if video capture was successful
    if not cap.isOpened():
        print("Error opening video file")
        exit()

    # Define the number of seconds to skip when starting the video
    skip_seconds = 1

    # Skip the specified number of seconds in the video
    cap.set(cv2.CAP_PROP_POS_MSEC, skip_seconds * 1000)

    # Read a frame from the video
    ret, frame = cap.read()

    # If frame is empty, it indicates that the video capture has finished
    if not ret:
        print("Error reading frame from video file")
        exit()

    # Detect common objects in the frame
    bbox, label, conf = cv.detect_common_objects(frame)

    # Count the number of cars detected in the frame
    car_count1 = label.count('car')

    # Draw bounding boxes around the detected objects in the frame
    output_image = draw_bbox(frame, bbox, label, conf)

    # Display the frame with bounding boxes around detected cars
    cv2.imshow('Cars Detected in Lane 1', output_image)
    cv2.waitKey(0)

    # Store the current frame in a variable for later use, if needed
    im = frame

    # Print the number of vehicles detected in lane 1
    print('Number of vehicles in lane 1 in the image is ', car_count1)


    # Video 2
    # Open the RTSP video stream from the second camera
    rtsp_link2 = 'rtsp://admin:admin12345@192.168.1.109:554/live'
    cap = cv2.VideoCapture(rtsp_link2)

    # Check if video capture was successful
    if not cap.isOpened():
        print("Error opening video file")
        exit()

    # Define the number of seconds to skip when starting the second video
    skip_seconds = 7

    # Skip the specified number of seconds in the video
    cap.set(cv2.CAP_PROP_POS_MSEC, skip_seconds * 1000)

    # Read a frame from the video
    ret, frame = cap.read()

    # If frame is empty, it indicates that the video capture has finished
    if not ret:
        print("Error reading frame from video file")
        exit()

    # Detect common objects in the frame
    bbox, label, conf = cv.detect_common_objects(frame)

    # Count the number of cars detected in the frame
    car_count2 = label.count('car')

    # Draw bounding boxes around the detected objects in the frame
    output_image = draw_bbox(frame, bbox, label, conf)

    # Display the frame with bounding boxes around detected cars
    cv2.imshow('Cars Detected in Lane 2', output_image)
    cv2.waitKey(0)

    # Store the current frame in a variable for later use, if needed
    im = frame

    # Print the number of vehicles detected in lane 2
    print('Number of vehicles in lane 2 in the image is ', car_count2)