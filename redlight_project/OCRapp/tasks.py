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
                decoded_image = base64.b64decode(nohelmet["number_plate"]) 
                nparr = np.frombuffer(decoded_image, np.uint8)


                opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                plate = extract_plate(opencv_image)
                

                record = {
                        "vehicle": nohelmet["vehicle"],
                        "number_plate_img": nohelmet["number_plate"],
                        "number_plate": plate,
                    }

                ocr_collection.insert_one(record)

        for nohelmet in nohelmetdata:
            Id = nohelmet['_id']
            if Id not in checkid:
                checkid.append(Id)
                decoded_image = base64.b64decode(nohelmet["number_plate"]) 
                nparr = np.frombuffer(decoded_image, np.uint8)


                opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                plate = extract_plate(opencv_image)
                

                record = {
                        "vehicle": nohelmet["vehicle"],
                        "number_plate_img": nohelmet["number_plate"],
                        "number_plate": plate,
                    }

                ocr_collection.insert_one(record)

        
        for nohelmet in wrongsidedata:
            Id = nohelmet['_id']
            if Id not in checkid:
                checkid.append(Id)
                decoded_image = base64.b64decode(nohelmet["number_plate"]) 
                nparr = np.frombuffer(decoded_image, np.uint8)


                opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                plate = extract_plate(opencv_image)
                

                record = {
                        "vehicle": nohelmet["vehicle"],
                        "number_plate_img": nohelmet["number_plate"],
                        "number_plate": plate,
                    }

                ocr_collection.insert_one(record)




    
