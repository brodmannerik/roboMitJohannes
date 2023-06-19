
import cv2
import serial

import pyttsx3
import random 
import json
import time


#eriks zeugs

engine = pyttsx3.init()

with open('wisdom.json') as f:
    data = json.load(f)
    #print(data)

sentences = data['sentences']

random.shuffle(sentences)

message = sentences[random.randint(0, len(sentences) - 1)]['message']

##voice

voices = engine.getProperty('voices')

for voice in voices:
    print(voice.name)
    engine.setProperty('voice', voice.id)

##rate

rate = engine.getProperty('rate')
print (rate)
engine.setProperty('rate', 125)

##volume

volume = engine.getProperty('volume')
print(volume)
engine.setProperty('volume', 1.0)


#johannes zeugs

ser = serial.Serial("COM5", 9600, timeout=0.050)  
print (ser.portstr)   




capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
#cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)



classNames= []
with open("cv2detection/coco.names","rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

net = cv2.dnn_DetectionModel("cv2detection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt", "cv2detection/frozen_inference_graph.pb")
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def calcSteps(y):

    MAXSTEPS = 680000
    LENSTEPS = 720000


    print("STEPS:")
    print(y)
    steps = (1920 - y) * int(LENSTEPS / 1920)
    steps = int(steps*(((1920 - y)**2) / (1920**2)))
    print(steps)
    if steps > MAXSTEPS:
        print("MAXTESTPS!!!!!!!!!!!!!!!!!!!")
        return str(MAXSTEPS)+"\n"
    elif steps < 0:
        return "0\n"
    else:
        return str(steps) + "\n"

go = True
while True:


    #go = False
    _, image = capture.read()
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    classIds, confs, bbox = net.detect(image ,confThreshold=.4)
    if len(classIds) != 0:
        det = False
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            # if self.classNames[classId-1] == "person" or self.classNames[classId-1] == "dog" or self.classNames[classId-1] == "hat" or self.classNames[classId-1] == "teddy bear" or self.classNames[classId-1] == "bear" or self.classNames[classId-1] == "backpack" or self.classNames[classId-1] == "umbrella" or self.classNames[classId-1] == "shoe": 
            if classNames[classId-1] == "person" or classNames[classId-1] == "dog" or classNames[classId-1] == "hat" or classNames[classId-1] == "teddy bear" or classNames[classId-1] == "bear": 
                cv2.rectangle(image,box,color=(0,0,255),thickness=2)
                #cv2.rectangle(image,[0,0,100,100],color=(200,0,255),thickness=2)
                cv2.putText(image, classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.putText(image,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)


                if(go):
                    go = False
                    print("FALSE")
                    ser.write(bytes(calcSteps(box[1]), 'utf-8'))
                else: 
                    get = ser.readline().decode('utf-8')
                    print(get)
                    if(get == "ok\r\n"):

                        #time.sleep(15)

                        engine.say(message)
                        engine.runAndWait()

                        print("TRUE")
                        go = True




    showImg = cv2.resize(image, (400, 600))
    cv2.imshow("Cam", showImg)
    if cv2.waitKey(1) == ord("q"):
        break
    


capture.release()
cv2.destroyAllWindows()






# import cv2
# import serial


# ser = serial.Serial("COM5", 9600, timeout=0.050)  
# print (ser.portstr)   




# capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# #cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")

# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)



# classNames= []
# with open("cv2detection/coco.names","rt") as f:
#     classNames = f.read().rstrip("\n").split("\n")

# net = cv2.dnn_DetectionModel("cv2detection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt", "cv2detection/frozen_inference_graph.pb")
# net.setInputSize(320,320)
# net.setInputScale(1.0/ 127.5)
# net.setInputMean((127.5, 127.5, 127.5))
# net.setInputSwapRB(True)

# def calcSteps(y):

#     MAXSTEPS = 680000
#     LENSTEPS = 720000
#     CHANGESTEPS = -15000


#     print("STEPS:")
#     print(y)
#     steps = (1920 - y) * int(LENSTEPS / 1920)
#     steps = int(steps*(((1920 - y)**2) / (1920**2)))
#     steps = steps + (CHANGESTEPS * (1-(((1920 - y)**2) / (1920**2))))
#     print(steps)
#     if steps > MAXSTEPS:
#         print("MAXTESTPS!!!!!!!!!!!!!!!!!!!")
#         return str(MAXSTEPS)+"\n"
#     elif steps < 0:
#         return "0\n"
#     else:
#         return str(steps) + "\n"

# go = True
# while True:


#     #go = False
#     _, image = capture.read()
#     image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
#     classIds, confs, bbox = net.detect(image ,confThreshold=.4)
#     if len(classIds) != 0:
#         det = False
#         for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
#             # if self.classNames[classId-1] == "person" or self.classNames[classId-1] == "dog" or self.classNames[classId-1] == "hat" or self.classNames[classId-1] == "teddy bear" or self.classNames[classId-1] == "bear" or self.classNames[classId-1] == "backpack" or self.classNames[classId-1] == "umbrella" or self.classNames[classId-1] == "shoe": 
#             if classNames[classId-1] == "person" or classNames[classId-1] == "dog" or classNames[classId-1] == "hat" or classNames[classId-1] == "teddy bear" or classNames[classId-1] == "bear": 
#                 cv2.rectangle(image,box,color=(0,0,255),thickness=2)
#                 #cv2.rectangle(image,[0,0,100,100],color=(200,0,255),thickness=2)
#                 cv2.putText(image, classNames[classId-1].upper(),(box[0]+10,box[1]+30),
#                 cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
#                 cv2.putText(image,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
#                 cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)


#                 if(go):
#                     go = False
#                     print("FALSE")
#                     ser.write(bytes(calcSteps(box[1]), 'utf-8'))
#                 else: 
#                     get = ser.readline().decode('utf-8')
#                     print(get)
#                     if(get == "ok\r\n"):

#                         print("TRUE")
#                         go = True




#     showImg = cv2.resize(image, (400, 600))
#     cv2.imshow("Cam", showImg)
#     if cv2.waitKey(1) == ord("q"):
#         break
    


# capture.release()
# cv2.destroyAllWindows()