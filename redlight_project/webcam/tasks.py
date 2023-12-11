# webcam/management/commands/capture_frames.py

from django.core.management.base import BaseCommand
from celery import shared_task
import cv2
import requests
import base64

@shared_task
def capture_frames():

    print("helloooo")
    print("Starting capture_frames task...")

    cap = cv2.VideoCapture(1)  # Access the default webcam (change 0 if using multiple cameras)

    while True:
        ret, frame = cap.read()

        if ret:

            cv2.imshow("image", frame)
    

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            

            # #Encode frame as base64 for transmission
            # encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')

            # # Send frame to Node.js server
            # url = 'http://localhost:4000/receive_frame'  # Replace with your Node.js server endpoint
            # response = requests.post(url, data={'frame': encoded_frame})
            
        cv2.waitKey(1)

    cap.release()
