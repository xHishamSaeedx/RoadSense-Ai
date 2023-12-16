from django.core.management.base import BaseCommand
from celery import shared_task
import requests
import base64
import numpy as np
import math
import pandas as pd 
from .models import *
import json
from PIL import Image
import io
from .myfunctions import *



def remove_punctuation(text):
    cleaned_text = text.replace(',', '').replace("'", '').replace('"', '').replace('.', '')
    return cleaned_text


@shared_task
def read_text():

    reader = easyocr.Reader(['en'])

    checkid = []
    
    while True:

        nohelmetdata = nohelmet_collection.find()
        redlightdata = redLight_collection.find()
        wrongsidedata = wrongside_collection.find()

        for nohelmet in redlightdata:
            Id = nohelmet['_id']
            if Id not in checkid:
                checkid.append(Id)

                plate_list = nohelmet["number_plate"]

                plate = None

                for number in plate_list:
                    decoded_image = base64.b64decode(number) 
                    nparr = np.frombuffer(decoded_image, np.uint8)


                    opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    plate = extract_plate(opencv_image)

                    if plate == None:
                        continue
                    
                    else:
                        break
                    
                if len(plate_list) == 0:

                    record = {
                            "vehicle": nohelmet["vehicle"],
                            "number_plate_img": [],
                            "number_plate": plate,
                            'Violation': "Red Light Signal Jumping"
                        }

                else:
                    record = {
                            "vehicle": nohelmet["vehicle"],
                            "number_plate_img": plate_list[-1],
                            "number_plate": plate,
                            'Violation': "Red Light Signal Jumping"
                        }


                ocr_collection.insert_one(record)



        for nohelmet in nohelmetdata:
            Id = nohelmet['_id']
            if Id not in checkid:
                checkid.append(Id)

                plate_list = nohelmet["number_plate"]

                plate = None

                for number in plate_list:
                    decoded_image = base64.b64decode(number) 
                    nparr = np.frombuffer(decoded_image, np.uint8)


                    opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    plate = extract_plate(opencv_image)

                    if plate == None:
                        continue
                    
                    else:
                        break
                    

                record = {
                        "vehicle": nohelmet["vehicle"],
                        "number_plate_img": plate_list[-1],
                        "number_plate": plate,
                        'Violation': "No Helmet Driving"
                    }

                ocr_collection.insert_one(record)

        
        for nohelmet in wrongsidedata:
            Id = nohelmet['_id']
            if Id not in checkid:
                checkid.append(Id)

                plate_list = nohelmet["number_plate"]
                plate = None    

                for number in plate_list:
                    decoded_image = base64.b64decode(number) 
                    nparr = np.frombuffer(decoded_image, np.uint8)


                    opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    plate = extract_plate(opencv_image)

                    if plate == None:
                        continue
                    
                    else:
                        break
                    
                if len(plate_list) == 0:

                    record = {
                            "vehicle": nohelmet["vehicle"],
                            "number_plate_img": [],
                            "number_plate": plate,
                            'Violation': "Wrong Side Driving"
                        }

                else:
                    record = {
                            "vehicle": nohelmet["vehicle"],
                            "number_plate_img": plate_list[-1],
                            "number_plate": plate,
                            'Violation': "Wrong Side Driving"
                        }


                ocr_collection.insert_one(record)

        print("done")




    
