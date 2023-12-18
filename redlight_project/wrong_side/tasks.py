# webcam/management/commands/capture_frames.py

from django.core.management.base import BaseCommand
from celery import shared_task
import requests
import base64
from ultralytics import YOLO
import cv2
import cvzone
import math
from .sort import *
import pandas as pd
from .models import person_collection , wrongside_collection
import base64
import random

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        # Read the image file and encode it as base64
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")
        # Create a JSON object containing the base64-encoded image
        image_json = {"image": encoded_image}
        return image_json

def resize_to_720p(img):
    # Read the image

    # Resize the image to 720p (1280x720)
    resized_img = cv2.resize(img, (1024, 768))

    return resized_img

def generate_random_id():
    return random.randint(100000, 999999)


@shared_task
def capture_frames2():

    check = 0
   
    filepath = 'C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\Videos\\shafaat.mp4'

    cap = cv2.VideoCapture(filepath)
    
    # cap = cv2.VideoCapture("C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\wrong_side\\Videos\\shafaat3.mp4")


    model = YOLO('C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\AiModels\\yolov8l.pt'
)
    npmodel = YOLO('C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\AiModels\\bestshafaat.pt'
)

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                "teddy bear", "hair drier", "toothbrush"
                ]
    #
    # mask = cv2.imread("mask.png")
    # tracking


    tracker  = Sort(max_age = 20, min_hits = 3 ,iou_threshold= 0.3)

    
    # limits2 = [0, 500, 480 , 500 ]
    # limits = [0, 425 , 480 , 425 ]

    limits = [0, 400 , 1024 , 400 ]
    limits2 = [0, 500 , 1024 , 500 ]

    totalCount = 0
    ids = []

    columns = ['Vehicle', 'number_plate', 'ID', "check", "wrongside"]
    temp_data = pd.DataFrame(columns=columns)

    columns = ['Vehicle', 'number_plate', 'ID']
    main_data = pd.DataFrame(columns=columns)


    while True:
        success, img = cap.read()
        

        # img = cv2.resize(img, (1920,1080))
        # imgRegion = cv2.bitwise_and(img, mask)
        

        # img = cv2.flip(img, 0)

        detections = np.empty((0, 5))
        if success == True:
            img = resize_to_720p(img)

            orifinal_frame = img.copy()
            results = model(img, stream = True)

            for r in results:
                boxes = r.boxes
                for box in boxes:

                    # #bounding box
                    # x1,y1,x2,y2 = box.xyxy[0]
                    # x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
                    # #cv2.rectangle(img, (x1, y1) , (x2,y2) ,(255,0, 255), 3 )
                    # w,h = x2-x1, y2-y1
                    #
                    # cvzone.cornerRect(img, (x1,y1,w,h), l = 9)
                    #
                    conf = math.ceil((box.conf[0]*100))/100

                    cls = box.cls[0]

                    currentClass = classNames[int(cls)]

                    if currentClass in ["car","truck" , "bus", "motorbike"] and conf > 0.3:
                        # bounding box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        # cv2.rectangle(img, (x1, y1) , (x2,y2) ,(255,0, 255), 3 )
                        w, h = x2 - x1, y2 - y1

                        #cvzone.cornerRect(img, (x1, y1, w, h), l=9 , rt = 5)
                        currentArray = np.array([x1,y1,x2,y2, conf])
                        detections = np.vstack((detections, currentArray))

            resultsTracker = tracker.update(detections)

            cv2.line(img, (limits[0] , limits[1]), (limits[2], limits[3]), (0,0,255), 5 )
            cv2.line(img, (limits2[0], limits2[1]), (limits2[2], limits2[3]), (0, 0, 255), 5)
            for results in resultsTracker:
                x1,y1,x2,y2, Id = results
                print(results)
                x1, y1, x2, y2 ,Id= int(x1), int(y1), int(x2), int(y2)  ,int(Id)
                w,h = x2 - x1 , y2-y1

                random_id = generate_random_id()

                if Id not in temp_data['ID'].values:
                    row = {'number_plate': [] , 'ID': Id, 'check' : True}
                    temp_data = temp_data.append(row, ignore_index=True)

                cvzone.cornerRect(img, (x1, y1, w, h), l=9 , rt = 2, colorR = (255,0,255))
                cvzone.putTextRect(img, f"{int(Id)}", (max(0, x1), max(35, y1)), scale=2, thickness=3,
                                   offset=10)

                cx,cy = x1+w//2, y1+h//2
                cv2.circle(img, (cx, cy), 5 , (255,0,255),cv2.FILLED)

                vehicle_img = orifinal_frame[y1:y2,x1:x2]

                if limits[0]< cx <limits[2] and limits[1]-20 < cy < limits[1]+20 and int(Id) :
                    temp_data.loc[temp_data['ID'] == Id, 'check'] = False
                    totalCount += 1
                    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0,255,0), 5)

                if limits2[0]< cx <limits2[2] and limits2[1]-20 < cy < limits2[1]+20 and int(Id) :
                    cv2.line(img, (limits2[0], limits2[1]), (limits2[2], limits2[3]), (0,255,0), 5)

                    if temp_data.loc[temp_data['ID'] == Id, 'check'].values[0] == True:
                        temp_data.loc[temp_data['ID'] == Id, 'wrongside'] = False

                    else:
                        temp_data.loc[temp_data['ID'] == Id, 'wrongside'] = True

                        
                        cv2.imwrite(f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\vehicle_pictures\\{Id}.jpg", vehicle_img)
                        temp_data.loc[temp_data['ID'] == Id, 'Vehicle'] = f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\vehicle_pictures\\{Id}.jpg"


                if temp_data.loc[temp_data['ID'] == Id, 'wrongside'].values[0] == True:
                    vehicle_img = np.ascontiguousarray(vehicle_img)
                    # #write a code to apply npmodel on the vehicle_img and get back the x1,y1,x2,y2 coords

                    
                    results2 = npmodel(vehicle_img, stream=True)
                    # #from results2 get the first x1,y1,x2,y2 coords and save it in a variable
                    npcoords = []
                    for t in results2:
                        boxes2 = t.boxes
                        for box2 in boxes2:
                            x12,y12,x22,y22 = box2.xyxy[0]
                            x12, y12, x22, y22 = int(x12),int(y12),int(x22),int(y22)
                            npcoord = [x12,y12,x22,y22]
                            npcoords.append(npcoord)

                    if len(npcoords)>0:
                        numberplate_coords = npcoords[0]
                        #write a code to crop the numberplate from the vehicle_img using the coords above and save it in a variable
                        numberplate_img = vehicle_img[int(numberplate_coords[1]):int(numberplate_coords[3]),int(numberplate_coords[0]):int(numberplate_coords[2])]
                        numberplate_img = np.ascontiguousarray(numberplate_img)

                        index_to_update = temp_data.index[temp_data['ID'] == Id].tolist()[0]


                        #write a code to save numberplate_img in number_plates folder with the name of the id
                        cv2.imwrite(f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\number_plates\\{random_id}.jpg", numberplate_img)
                        #write a code to find the row in main_data with Id , then update the numberplate column for that row 

                        temp_data.at[index_to_update, 'number_plate'].append(f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\number_plates\\{random_id}.jpg")

                        



                    cvzone.cornerRect(img, (x1, y1, w, h), l=9 , rt = 2, colorR = (255,0,255))
                    cvzone.putTextRect(img, f"{int(Id)}", (max(0, x1), max(35, y1)), scale=2, thickness=3,
                                    offset=10)


            cvzone.putTextRect(img, f"Count : {totalCount}", (50, 50))

            cv2.imshow("image5", img)


            _, buffer = cv2.imencode('.jpg', img)
            frame_bytes = buffer.tobytes()

            

            #Encode frame as base64 for transmission
            encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')

            # Send frame to Node.js server
            url = 'http://localhost:4000/receive_frame2'  # Replace with your Node.js server endpoint
            response = requests.post(url, data={'frame': encoded_frame})



        else: 
                
            if check ==0:
                filtered_rows = temp_data[(temp_data['wrongside'] == True) & 
                            temp_data['Vehicle'].notnull()
                            ]
                main_data = main_data.append(filtered_rows[columns], ignore_index=True)



                records = []
                for index, row in main_data.iterrows():
                    vehicle_path = row['Vehicle']
                    number_plate_paths = row['number_plate']
                    ID = row['ID']

                    with open(vehicle_path, 'rb') as vehicle_img_file:
                        vehicle_img = base64.b64encode(vehicle_img_file.read()).decode('utf-8')

                    number_plate_images = []
                    for plate_path in number_plate_paths:
                        with open(plate_path, 'rb') as plate_img_file:
                            number_plate_images.append(base64.b64encode(plate_img_file.read()).decode('utf-8'))


                    
                                
                    record = {
                        "vehicle": vehicle_img,
                        "number_plate": number_plate_images,
                        "ID": ID
                    }

                    records.append(record)

                for rcrd in records:    
                    wrongside_collection.insert_one(rcrd)

                check += 1

            main_data.to_csv("C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\wrong_side\\data.csv", index=False)
            
            main_data.drop(main_data.index, inplace=True)
            temp_data.drop(temp_data.index, inplace=True)

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        #cv2.imshow("imageregion", imgRegion )
        cv2.waitKey(1)
        











































    # print("helloooo 3333333333")
    # print("Starting capture_frames task...")

    # cap = cv2.VideoCapture('C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\motorbikes.mp4')   # Access the default webcam (change 0 if using multiple cameras)

    # while True:
    #     ret, frame = cap.read()

    #     if ret:
    #         print("helllodsfdsfdfdsf")

    #         cv2.imshow("image2", frame)
    

    #         _, buffer = cv2.imencode('.jpg', frame)
    #         frame_bytes = buffer.tobytes()

            

    #         #Encode frame as base64 for transmission
    #         encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')

    #         # Send frame to Node.js server
    #         url = 'http://localhost:4000/receive_frame'  # Replace with your Node.js server endpoint
    #         response = requests.post(url, data={'frame': encoded_frame})
            

    #     else: 
    #         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    #         continue





    #     cv2.waitKey(1)
