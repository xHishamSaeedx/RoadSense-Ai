# webcam/management/commands/capture_frames.py

from django.core.management.base import BaseCommand
from celery import shared_task
import cv2
import requests
import base64
from .models import person_collection 
from ultralytics import YOLO
import cv2
import cvzone
import math

from .sort import *

from .myfunctions import *

import random

def generate_random_id():
    return random.randint(100000, 999999)


@shared_task
def capture_frames3():
    source = 'C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\Videos\\shafaat2.mp4'

    cap = cv2.VideoCapture(source)

    model = YOLO("C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\AiModels\\best.pt")


    columns = ['Rider', 'number_plate', 'helmet', 'timestamp', 'ID']
    temp_data = pd.DataFrame(columns=columns)

    columns2 = ['Rider', 'number_plate', "ID"]
    nohelmet_data = pd.DataFrame(columns=columns2)

    classNames = ["NoHelmet", "PlateNumber" , "Rider" , "WithHelmet"]


    tracker  = Sort(max_age = 20, min_hits = 3 ,iou_threshold= 0.3)

    rider_ids = []
    plate_ids = []

    # classNames = ["all"]

    while(cap.isOpened()):
        success, frame = cap.read()
        if success:
            orifinal_frame = frame.copy()
            #frame = cv2.bitwise_and(frame, mask)
            results = model(frame, stream = True)
            detections = np.empty((0, 5))

            rider_list = []
            number_list = []
            nohelmet_list = []
            helmet_list = []

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    conf = math.ceil((box.conf[0] * 100)) / 100

                    cls = int(box.cls[0])

                    currentClass = classNames[int(cls)]
                    if conf > 0.3:
                        
                        if cls == 2:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            rider_list.append(r)
                            currentArray = np.array([x1,y1,x2,y2,conf])
                            detections = np.vstack((detections, currentArray))
                        elif cls == 1:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            numberplate_row = [x1,y1,x2,y2]
                            number_list.append(numberplate_row)

                        elif cls == 0:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            nohelmet_row = [x1,y1,x2,y2]
                            nohelmet_list.append(nohelmet_row)

                        elif cls == 3:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            helmet_row = [x1,y1,x2,y2]
                            helmet_list.append(helmet_row)

            resultsTracker = tracker.update(detections)
            for rdr in resultsTracker:
                x1r, y1r, x2r, y2r, Id = rdr
                x1r, y1r, x2r,y2r, Id = int(x1r), int(y1r), int(x2r), int(y2r), int(Id)
                current_time = datetime.datetime.now()
                time_stamp = int(current_time.second)
                # Generate a random 6-digit ID
                random_id = generate_random_id()

                if Id not in temp_data['ID'].values:
                    row  = {'helmet': True, 'timestamp': time_stamp,'ID': Id}
                    temp_data = temp_data.append(row, ignore_index=True)
                    
                    
        
                wr,hr = x2r - x1r , y2r-y1r
                cvzone.cornerRect(frame, (x1r, y1r, wr, hr), l=9 , rt = 2, colorR = (255,0,255))
                cvzone.putTextRect(frame, f"{int(Id)}", (max(0, x1r), max(35, y1r)), scale=2, thickness=3,
                                offset=10)

                rider_img = orifinal_frame[y1r:y2r , x1r:x2r]
                rider_coords = [x1r,y1r,x2r,y2r]
                helmet_present = img_classify(rider_coords, helmet_list , nohelmet_list)

                if helmet_present[0] == False: # if helmet absent 
                    temp_data.loc[temp_data['ID'] == Id, 'helmet'] = False

                    for hd in nohelmet_list:
                        x1hd, y1hd, x2hd, y2hd = hd
                        x1hd, y1hd, x2hd, y2hd = int(x1hd), int(y1hd), int(x2hd), int(y2hd)
                        w,h = x2hd - x1hd , y2hd-y1hd
                        if inside_box([x1r,y1r,x2r,y2r], [x1hd,y1hd,x2hd,y2hd]):
                            cvzone.cornerRect(frame, (x1hd, y1hd, w, h), l=9 , rt = 2, colorR = (255,0,255))
                            cvzone.putTextRect(frame, f"NO HELMET", (max(0, x1hd), max(35, y1hd)), scale=2, thickness=3,
                                            offset=10)

                for num in number_list:
                    x1_num, y1_num, x2_num, y2_num = num
                    if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):

                        # if pd.isnull(temp_data.loc[temp_data['ID'] == Id, 'number_plate'].values[0]):
                        try:
                            num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                            cv2.imwrite(f'C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\number_plates\\{random_id}.jpg', num_img)
                            temp_data.loc[temp_data['ID'] == Id, 'number_plate'] = f'C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\number_plates\\{random_id}.jpg'
                        except:
                            print('could not save number plate')

                # if pd.isnull(temp_data.loc[temp_data['ID'] == Id, 'Rider'].values[0]):
                try:
                    cv2.imwrite(f'C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\riders_pictures\\{random_id}.jpg', rider_img)
                    temp_data.loc[temp_data['ID'] == Id, 'Rider'] = f'C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\riders_pictures\\{random_id}.jpg'
                    
                        
                except:
                    print('could not save rider')
                    

            cv2.imshow("image", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        
        else:
            break

        nohelmet_data = extract_and_add_rows(temp_data, nohelmet_data)
        nohelmet_data.to_csv('C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\riders_pictures\\nohelmet_data.csv', index=False)
        


        
    cap.release()
    cv2.destroyAllWindows()
            

    































# @shared_task
# def capture_frames3():

#     print("helloooo 3333333333")
#     print("Starting capture_frames task...")

#     cap = cv2.VideoCapture('C:\\Users\\m_his\\OneDrive\\Pictures\\Documents\\GitHub\\Roadsense_django\\redlight_project\\nohelmetapp\\motorbikes.mp4')   # Access the default webcam (change 0 if using multiple cameras)

#     while True:
#         ret, frame = cap.read()

#         if ret:
#             print("helllodsfdsfdfdsf")

#             cv2.imshow("image3", frame)
    

#         #     _, buffer = cv2.imencode('.jpg', frame)
#         #     frame_bytes = buffer.tobytes()

            

#         #     # #Encode frame as base64 for transmission
#         #     # encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')

#         #     # # Send frame to Node.js server
#         #     # url = 'http://localhost:4000/receive_frame'  # Replace with your Node.js server endpoint
#         #     # response = requests.post(url, data={'frame': encoded_frame})
            
#         cv2.waitKey(1)

#     cap.release()






