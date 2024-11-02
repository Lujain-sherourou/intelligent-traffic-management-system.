# intelligent-traffic-management-system.
# Developed a system that relies on image analysis using cameras installed at traffic signals. The system counts the number of vehicles in each lane and determines the most congested lane to activate the green light based on traffic density. This project contributes to improving traffic management and reducing vehicle wait times.
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
    def Find_density():
    # Initialize a dictionary to store vehicle counts for each lane
    dict_lane = {'lane-1': 0, 'lane-2': 0}
    dict_lane['lane-1'] = car_count1  # Store the count of cars in lane 1
    dict_lane['lane-2'] = car_count2  # Store the count of cars in lane 2

    # Sort the lanes based on their vehicle count in descending order
    sorted_density = sorted(dict_lane.items(), key=lambda x: x[1], reverse=True)
    return sorted_density  # Return the sorted list of lanes and their counts

def DURATION():
    # Get the sorted density from Find_density function
    sorted_density = Find_density()
    max_density_lane = sorted_density[0]  # Get the lane with the maximum vehicle count

    # Check if the maximum vehicle count is zero
    if max_density_lane[1] == 0:
        print(f'{max_density_lane[0]} turns green for 0 sec!')  # No vehicles present
        return 0, max_density_lane[0]  # Return duration 0 and lane name

    else:
        # Calculate the duration for which the traffic light should remain green
        duration = min(round(max_density_lane[1] * 2), 50)  # Max duration capped at 50 seconds
        print(f'{max_density_lane[0]} turns green for {duration} sec!')
        return duration, max_density_lane[0]  # Return the calculated duration and lane name

# Call the functions
sorted_density = Find_density()  # Get sorted density of lanes
duration, max_density_lane = DURATION()  # Get the duration and lane with max density

# Define pin assignments for the first 7-segment display
SEG_PINS2 = [30, 31, 32, 33, 34, 35, 36]  # Pins for segments of the first display
COMMON_PIN2 = 5  # Common pin for the first display

# Define pin assignments for the second 7-segment display
SEG_PINS = [6, 7, 8, 9, 10, 11, 12]  # Pins for segments of the second display
COMMON_PIN = 13  # Common pin for the second display (assumed 13, can be changed if needed)

# Define patterns for numbers on the 7-segment displays
# Each list represents the segments (a, b, c, d, e, f, g) lit up for each number
NUMBERS2 = {
    0: [1, 1, 1, 1, 1, 1, 0],
    1: [0, 1, 1, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1],
    3: [1, 1, 1, 1, 0, 0, 1],
    4: [0, 1, 1, 0, 0, 1, 1],
    5: [1, 0, 1, 1, 0, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1],
    7: [1, 1, 1, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1],
}

# The following NUMBERS dictionary is a duplicate of NUMBERS2, which can be removed if not needed
NUMBERS = {
    0: [1, 1, 1, 1, 1, 1, 0],
    1: [0, 1, 1, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1],
    3: [1, 1, 1, 1, 0, 0, 1],
    4: [0, 1, 1, 0, 0, 1, 1],
    5: [1, 0, 1, 1, 0, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1],
    7: [1, 1, 1, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1],
    }
    # Define the pins as OUTPUT for the first 7-segment display
for pin in SEG_PINS2 + [COMMON_PIN2]:
    board.digital[pin].mode = pyfirmata2.OUTPUT  # Set each segment pin and common pin as OUTPUT

# Define the pins as OUTPUT for the second 7-segment display
for pin in SEG_PINS + [COMMON_PIN]:
    board.digital[pin].mode = pyfirmata2.OUTPUT  # Set each segment pin and common pin as OUTPUT

# Function to display a number on the first 7-segment display
def display_number1(number):
    # Get the segment configuration for the given number
    segments = NUMBERS.get(number, [0, 0, 0, 0, 0, 0, 0])

    # Iterate over the segment pins and write the segment states
    for i, pin in enumerate(SEG_PINS):
        board.digital[pin].write(segments[i])  # Set each segment according to the configuration
    board.digital[COMMON_PIN].write(0)  # Set common pin to LOW to enable the display

# Function to display a number on the second 7-segment display
def display_number2(number):
    # Get the segment configuration for the given number from the second dictionary
    segments = NUMBERS2.get(number, [0, 0, 0, 0, 0, 0, 0])

    # Iterate over the segment pins and write the segment states
    for i, pin in enumerate(SEG_PINS2):
        board.digital[pin].write(segments[i])  # Set each segment according to the configuration
    board.digital[COMMON_PIN2].write(0)  # Set common pin to LOW to enable the display

# Function for controlling the traffic light
def Ard_function():
    time1 = 1  # Set variable time1 to 1 second for timing purposes
    # Define the pin configuration for each lane's traffic lights
    pins = {
        'lane-2': {'green': 22, 'yellow': 23, 'red': 24},  # Pin assignments for lane 2 traffic lights
        'lane-1': {'green': 25, 'yellow': 26, 'red': 27}   # Pin assignments for lane 1 traffic lights
    }
    def control_lights():
    # Turn on the yellow LED lights for both lanes
    for pin in [23, 26]:  # Pins for yellow lights in lane 1 and lane 2
        board.digital[pin].write(1)  # Set both yellow lights to HIGH (on)
    time.sleep(time1)  # Keep the yellow lights on for the duration specified by time1

    # Turn off the yellow LED lights for both lanes
    for pin in [23, 26]:  # Pins for yellow lights in lane 1 and lane 2
        board.digital[pin].write(0)  # Set both yellow lights to LOW (off)
    
    # Turn on the green LED for the lane with the highest vehicle density
    board.digital[pins[max_density_lane]['green']].write(1)  # Set the green light for the max density lane to HIGH

    # Turn on the red LED for the other lane
    other_lane = 'lane-1' if max_density_lane == 'lane-2' else 'lane-2'  # Determine the other lane based on max_density_lane
    board.digital[pins[other_lane]['red']].write(1)  # Set the red light for the other lane to HIGH

    # Countdown function to display numbers on the 7-segment displays
    def countdown(start_number):
        for i in range(start_number, -1, -1):  # Count down from start_number to 0
            display_number1(i)  # Display the current count on the first 7-segment display
            display_number2(i)  # Display the current count on the second 7-segment display
            time.sleep(1)  # Wait for 1 second before the next count

    # Call the countdown function with a specified duration
    countdown(duration)  # Pass the duration variable to the countdown function

    # Turn off all LED lights after countdown
    for pin in [22, 23, 24, 25, 26, 27]:  # Pins for all LED lights in both lanes
        board.digital[pin].write(0)  # Set all lights to LOW (off)

# Call the control_lights function to manage LED light states
control_lights()  # Control LED lights based on the maximum density lane
Ard_function()  # Call the Ard_function to perform other operations defined previously
