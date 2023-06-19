import cv2
thres = 0.35 # Threshold to detect object

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4000)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,150)

classNames= []
classFile = "coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    success,img = cap.read()
    classIds, confs, bbox = net.detect(img,confThreshold=thres)

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            if classNames[classId-1] == "person" or classNames[classId-1] == "dog" or classNames[classId-1] == "hat" or classNames[classId-1] == "teddy bear" or classNames[classId-1] == "bear" or classNames[classId-1] == "backpack" or classNames[classId-1] == "umbrella" or classNames[classId-1] == "shoe": 
                cv2.rectangle(img,box,color=(0,0,255),thickness=2)
                cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)


    cv2.imshow("Output",img)
    cv2.waitKey(1)