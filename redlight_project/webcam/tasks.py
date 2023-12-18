# webcam/management/commands/capture_frames.py

from django.core.management.base import BaseCommand
from celery import shared_task
import cv2
import requests
import base64
import numpy as np
from ultralytics import YOLO
import cvzone
import math
from .sort import *
import pandas as pd 
from .models import person_collection , redLight_collection
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


def image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def generate_random_id():
    return random.randint(100000, 999999)


@shared_task
def capture_frames():
    # cap = cv2.VideoCapture("C:\\Users\\m_his\\PycharmProjects\\OBJECTDETECT\\yolo with webcam\\shafaattest4.MOV") 
    cap = cv2.VideoCapture('C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\Videos\\shafaat3.mp4'
) # For Video

    #create a pandas dataframe to store vehicle image path , numberplate and id 
    columns = ['Vehicle', 'number_plate', 'ID']
    main_data = pd.DataFrame(columns=columns)

    model = YOLO('C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\AiModels\\yolov8l.pt'
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

    classNames2 = ["all"]

    npmodel = YOLO('C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\AiModels\\number_plate.pt'
)
    # Tracking
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

    limits =  [0,420,480,420]

    totalCount = []
    flag=False

    while True:
        success, img = cap.read()
        if success:
            # img = resize_to_720p(img)
            #imgRegion = cv2.bitwise_and(img, mask)

            #imgGraphics = cv2.imread("graphics.png", cv2.IMREAD_UNCHANGED)
            #img = cvzone.overlayPNG(img, imgGraphics, (0, 0))
            orifinal_frame = img.copy()

            cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

            if flag:
                results = model(img, stream=True)

                detections = np.empty((0, 5))

                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # Bounding Box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                        w, h = x2 - x1, y2 - y1

                        # Confidence
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        # Class Name
                        cls = int(box.cls[0])
                        currentClass = classNames[cls]

                        if currentClass == "car" or currentClass == "truck" or currentClass == "bus" \
                                or currentClass == "motorbike" and conf > 0.3:
                            # cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                            #                    scale=0.6, thickness=1, offset=3)
                            # cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                            currentArray = np.array([x1, y1, x2, y2, conf])
                            detections = np.vstack((detections, currentArray))

                resultsTracker = tracker.update(detections)

                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
                for result in resultsTracker:
                    x1, y1, x2, y2, Id = result
                    x1, y1, x2, y2 , Id = int(x1), int(y1), int(x2), int(y2) , int(Id)
                    print(result)
                    w, h = x2 - x1, y2 - y1
                    random_id = generate_random_id()

                    cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                    cvzone.putTextRect(img, f' {int(Id)}', (max(0, x1), max(35, y1)),
                                    scale=2, thickness=3, offset=10)

                    cx, cy = x1 + w // 2, y1 + h // 2
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                    if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)
                        #write a code to save the cropped image of orifinal_frame the coords of which r x1,y1,x2,y2
                        
                        vehicle_img = orifinal_frame[y1:y2,x1:x2]

                        if Id not in main_data['ID'].values:
                            cv2.imwrite(f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\vehicle_pictures\\{Id}.jpg", vehicle_img)
                            #write a code to append a row with in the main_data with this pathway above Vehicle column and Id for ID column
                            row = {'Vehicle': f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\vehicle_pictures\\{Id}.jpg", 'number_plate': [], 'ID': Id}
                            main_data = main_data.append(row, ignore_index=True)



                    if Id in main_data['ID'].values:
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
                           
                            numberplate_img = vehicle_img[int(numberplate_coords[1]):int(numberplate_coords[3]),int(numberplate_coords[0]):int(numberplate_coords[2])]

                            cv2.imwrite(f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\number_plates\\{random_id}.jpg", numberplate_img)
                            index_to_update = main_data.index[main_data['ID'] == Id].tolist()[0]
      
                            main_data.at[index_to_update, 'number_plate'].append(f"C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\number_plates\\{random_id}.jpg")

                        
                        

            

            cv2.imshow("Image", img)

            _, buffer = cv2.imencode('.jpg', img)
            frame_bytes = buffer.tobytes()

            

            #Encode frame as base64 for transmission
            encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')

            # Send frame to Node.js server
            url = 'http://localhost:4000/receive_frame2'  # Replace with your Node.js server endpoint
            response = requests.post(url, data={'frame': encoded_frame})


            # cv2.imshow("ImageRegion", imgRegion)

            # Capture key press events
            key = cv2.waitKey(1)

            if key == ord('w'):
                flag = not flag  # Toggle the value of the flag variable


            #convert main_data to csv file and store it in number_plates folder
            
        else:
                
            
            
            main_data = main_data[~(
                            (main_data['Vehicle'].isna()))]

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
                redLight_collection.insert_one(rcrd)

                
            main_data.to_csv("C:\\Users\\shafaat hussain\\RoadSense-Ai\\redlight_project\\webcam\\data.csv", index=False)

            
            main_data.drop(main_data.index, inplace=True)

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        







































    # print("helloooo 3333333333")
    # print("Starting capture_frames task...")

    # cap = cv2.VideoCapture('C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\motorbikes.mp4')   # Access the default webcam (change 0 if using multiple cameras)

    # while True:
    #     ret, frame = cap.read()

    #     if ret:
    #         print("helllodsfdsfdfdsf")

    #         cv2.imshow("image1", frame)
    

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





        # cv2.waitKey(1)
