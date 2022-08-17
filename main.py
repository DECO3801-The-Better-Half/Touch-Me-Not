import cv2
from cvzone.FaceDetectionModule import FaceDetector
import matplotlib.pyplot as plt
from deepface import DeepFace
import time
import serial
import threading
from playsound import playsound
import os



def run():

    detector = FaceDetector(minDetectionCon=0.8)
    cap = cv2.VideoCapture(0)

    startTime = time.time()

    while True:
        success, frame = cap.read()

        currentTime = time.time()
        if currentTime > startTime + 0.75:
            startTime = time.time()
            result = DeepFace.analyze(frame, enforce_detection=False, actions = ['emotion'])
            #result = DeepFace.analyze(frame, enforce_detection=False)
            print(result['dominant_emotion'])
        frame, bboxs = detector.findFaces(frame)
        cv2.imshow("Original Video", frame)

        cv2.waitKey(1)



        #cv2.imshow("Image", img)


def get_serial():

        startTime = time.time()
        #sPort = '/dev/tty.usbmodem101'
        sPort = '/dev/cu.usbmodem101'

        ser = serial.Serial(sPort, 9600, timeout=1)

        state = False

        while True:

            if ser.inWaiting() > 0:
                data = ser.readline()
                parsed_data = data.decode().strip().replace("\n","").split(",")
                print(parsed_data)

                button1 = parsed_data[0]
                button2 = parsed_data[1]
                button3 = parsed_data[2]

                if button1 == '1' and state == False:
                    state = True
                    x = threading.Thread(target=playsound, args=('sounds/small-door-bell.wav',))
                    x.start()

                if button1 == '0' and state == True:
                    state = False



if __name__ == '__main__':
    print()
    #run()
    get_serial()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)

    #playsound('sounds/small-door-bell.wav')
    #playsound('sounds/small-door-bell.wav')
