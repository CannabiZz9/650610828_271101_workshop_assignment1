import cv2
import mediapipe as mp
import time
import pyfirmata
time.sleep(2.0)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

board=pyfirmata.Arduino('COM'+'3')  
led_1=board.get_pin('d:13:o') #Set pin to output
led_2=board.get_pin('d:12:o')
led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')
led_5=board.get_pin('d:9:o')


def led(finger,led_1,led_2,led_3,led_4,led_5):#creat condition to controll digital out put 
    if finger[0]=="n":
        led_1.write(0)
    if finger[0] == "y":
        led_1.write(1)
    if finger[1]=="n":
        led_2.write(0)
    if finger[1] == "y":
        led_2.write(1)
    if finger[2]=="n":
        led_3.write(0)
    if finger[2] == "y":
        led_3.write(1)
    if finger[3]=="n":
        led_4.write(0)
    if finger[3] == "y":
        led_4.write(1)
    if finger[4]=="n":
        led_5.write(0)
    if finger[4] == "y":
        led_5.write(1)
    

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Initially set finger count to 0 for each cap
    fingernow = ""
    finger = ["n", "n", "n", "n", "n"]

    if results.multi_hand_landmarks:

      for hand_landmarks in results.multi_hand_landmarks:
        # Get hand index to check label (left or right hand)
        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
        handLabel = results.multi_handedness[handIndex].classification[0].label

        # Set variable to keep landmarks positions (x and y)
        handLandmarks = []

        # Fill list with x and y positions of each landmark
        for landmarks in hand_landmarks.landmark:
          handLandmarks.append([landmarks.x, landmarks.y])

        
        if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
          fingernow = "poong "
          finger[0] = "y"

        elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
          fingernow = "poong "
          finger[0] = "y"

        if handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
          fingernow += "chee "
          finger[1] = "y"
        if handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
          fingernow += "gang "
          finger[2] = "y"
        if handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
          fingernow += "nang "
          finger[3] = "y"
        if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
          fingernow += "koy "
          finger[4] = "y"
        

        # Draw hand landmarks 
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    led(finger,led_1,led_2,led_3,led_4,led_5)

    # Display finger count
    cv2.putText(image, str(fingernow), (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 5)

    # Display image
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()