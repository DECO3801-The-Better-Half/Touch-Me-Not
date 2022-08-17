import cv2
from cvzone.FaceDetectionModule import FaceDetector
import matplotlib.pyplot as plt
from deepface import DeepFace
import time
import serial

def run():

    #img2 = cv2.imread('happy.jpg')
    #plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    #predictions = DeepFace.analyze(img2)
    #print(predictions)

    detector = FaceDetector(minDetectionCon=0.8)
    cap = cv2.VideoCapture(0)
    #DeepFace.stream()

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

        startTime = time.time()

        while True:
            currentTime = time.time()
            if currentTime > startTime + 0.75:
                startTime = time.time()

                if ser.inWaiting() > 0:
                    data = ser.readline()
                    parsed_data = data.decode().strip().replace("\n","").split(",")
                    print(parsed_data)

if __name__ == '__main__':
    run()
    #get_serial()

